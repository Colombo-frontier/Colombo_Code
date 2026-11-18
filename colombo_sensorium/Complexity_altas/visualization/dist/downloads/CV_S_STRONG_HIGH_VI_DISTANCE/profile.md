# Higher-order strongly monotone root finding: complete jets and solution distance.

**Setting ID.** `CV_S_STRONG_HIGH_VI_DISTANCE`

Variational inequalities

$$
F(z^\star)=0,\quad z^\star\in\mathbb{R}^d.
$$

**Status.** Bounds missing

**TASK tags.** solution concept: Solution distance; task family: Variational inequality

**MODEL tags.** initialization: Initialization; monotonicity: Strong monotonicity; monotonicity: Strongly monotone

**ORACLE tags.** feedback quality: Exact; interface family: Complete operator jet; operation: Operator complete jet; operator derivative order: Parameterized order p−1 (see exact operation binding); public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Distance

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N operator jet; setup: Initialization included

## 1. Setting specification

### Task

$$
F(z^\star)=0,\quad z^\star\in\mathbb{R}^d.
$$

### Admissible model

Assume $F\in C^{p-1}(\mathbb{R}^d;\mathbb{R}^d)$ and global $\mu$-strong monotonicity, with a zero known to exist. Fix an integer $p\ge2$,

$$
\|\mathrm{D}^{p-1}F(z)-\mathrm{D}^{p-1}F(w)\|_{\rm op}\le L_p\|z-w\|_2.
$$

No separate bound on lower-order derivatives or $\|F\|$ is supplied. The public initial point satisfies $\|z_0-z^\star\|_2\le R_0$.

### Oracle interface

Public inputs comprise the dimension $d$ and parameters $L_p$, $R_0$, $\varepsilon$, $\mu$, and $p$, together with the stated initial point and feasible-set information. Analytic descriptions of hidden functions, operators, and matrices are not supplied.

$$
z\in\mathbb{R}^d\longmapsto(F(z),\mathrm{D}F(z),\ldots,\mathrm{D}^{p-1}F(z)).
$$

Each call returns the complete exact derivative bundle. Solving models from returned coefficients and projecting onto the known ball are internal operations.

### Output

Return $\widehat{z}\in\mathbb{R}^d$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|\widehat{z}-z^\star\|_2
$$

Strong monotonicity gives $\mu\|z-z^\star\|_2\le\|F(z)\|_2$. The reverse conversion requires an additional lower-order smoothness bound.

### Resource accounting

Each complete operator jet counts once in $N_{\rm jet}$, including every nested call to the unknown operator.

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

$L_p$: Lipschitz upper bound for the operator's order-(p-1) Fréchet derivative in the Euclidean induced tensor norm **Domain:** Positive real number.

$\|\mathrm D^{p-1}F(z)-\mathrm D^{p-1}F(w)\|_{\rm op}\le L_p\|z-w\|_2$

$R_0$: Euclidean distance bound from the public initial point to the same solution promised by the model; not the entire domain diameter **Domain:** A nonnegative real.

$\|z_0-z^\star\|_2\le R_0$

$\chi_p$: Ratio of the higher-order initial scale to strong monotonicity **Domain:** A nonnegative real.

$\chi_p=L_pR_0^{p-1}/\mu$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: Euclidean distance tolerance to the unique solution; the mean-square contract targets squared distance $\varepsilon^2$. **Domain:** Positive real number.

$\mu$: A strong-monotonicity lower bound for the full operator. **Domain:** Positive real number.

$\langle F(u)-F(v),u-v\rangle\ge\mu\|u-v\|_2^2$

$p$: Fix the operator order parameter. One jet query returns the complete bundle from F through $\mathrm D^{p-1}F$. **Domain:** Fixed integer at least $2$.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$F$: The unknown operator is single-valued. Monotonicity, strong monotonicity, or weak Minty properties use the specification’s explicit inequalities. **Domain:** A vector map from the declared query domain into $\mathbb R^d$.

$z,u,v$: The operator argument and comparison point in the inequality. **Domain:** The ambient space is $\mathbb R^d$. Formulas constrained by $K$ require the corresponding point to lie in $K$.

$\mathrm D^jF$: The jth Fréchet derivative of operator F. One interface call returns every tensor in the bundle. **Domain:** For $0\le j\le p-1$, the interface takes $j$ vectors in $\mathbb R^d$ and returns one vector in $\mathbb R^d$.

$\mathrm D^0F=F$

$\|\cdot\|_{\rm op}$: Matrix or multilinear tensor norm induced by the Euclidean norm **Domain:** Matrix and derivative tensors used in this profile.

$\|T\|_{\rm op}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}\|T[u_1,\ldots,u_j]\|_2$

$z_0,z^\star$: Public initial point and the same solution appearing in the model assumption **Domain:** Feasible domain of this profile; the distance bound refers to the same solution.

$\widehat z$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** $\mathbb R^d$.

$N_{\rm jet}$: Number of complete operator-jet calls through the stated derivative order. **Domain:** Nonnegative integer count; expected work is its expectation.

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
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I N_{\rm jet}(\mathcal A,I)
$$

**Scope.** The instancewise guarantee uses the same contract; dimension obeys the specification and theorem region.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - Positive initialization-radius regime

**Region.** Fix $R_0>0$ and $p\ge2$; assume $L_p,\mu,\varepsilon>0$.

**Quantity.** Q1

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O_p\!\left(1+\chi_p^{2/(3p-1)}+\log_+(R_0/\varepsilon)\right)
$$

**Comparison argument.** This is an explicitly implementable upper bound, without a claim of global optimality among existing strongly monotone high-order methods. A matching lower bound is still missing.

### R2 - Zero-radius regime

**Region.** $R_0=0$.

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

**Comparison argument.** Nonnegative cost.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle mapping.** All primitive information operations are charged; see the specification and method description.

**Guarantee mapping.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource mapping.** Complete query budget of a single algorithm

### B1 - Strong-monotonicity restart of the higher-order tangential-residual algorithm

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Apply geometric restarting to a deterministic exact-operator residual method. Public parameters determine every restart threshold.

$$
O_p\!\left(1+\chi_p^{2/(3p-1)}+\log_+(R_0/\varepsilon)\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.23557v1)

**Conditions.** Apply the higher-order monotone VI upper bound on a known ball of radius $2R$ whose center is within $R$ of a root. Strong monotonicity bounds distance by the tangent residual divided by $\mu$. Halve $R$ at each stage. The stage cost is $O_p(1+(L_pR^{p-1}/\mu)^{2/(3p-1)})$; summing the geometric series gives the stated bound.

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Local argument.** A1

### B2 - Return the known root z0.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** In this region, the witness returns the public initial point or known root, deterministically and without querying.

$$
0
$$

**Conditions.** Zero initial distance means $z_0=z^\star$.

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Local argument.** A2

## 5. Local arguments

### A1 - Strong-monotonicity restart of the higher-order tangential-residual algorithm

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Apply the higher-order monotone VI upper bound on a known ball of radius $2R$ whose center is within $R$ of a root. Strong monotonicity bounds distance by the tangent residual divided by $\mu$. Halve $R$ at each stage. The stage cost is $O_p(1+(L_pR^{p-1}/\mu)^{2/(3p-1)})$; summing the geometric series gives the stated bound.

**Sources.** [1](https://arxiv.org/pdf/2609.23557v1)

### A2 - Return the known root z0.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

If $R_0=0$, the initialization promise forces $z_0=z^\star$. Return $z_0$ without querying. Both distance and the true root residual are zero, and no smaller query cost is possible.

## References

[1] Xinliang Zhang; Lesi Chen; Linxuan Pan; Chengchang Liu; Junchi Yang; Jingzhao Zhang. Optimal High-Order Methods for Solving Monotone Variational Inequalities. 2026. arXiv:2609.23557v1, 2026-09-20.

https://arxiv.org/pdf/2609.23557v1
