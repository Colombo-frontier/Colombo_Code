# Ball-simplex matrix games: arbitrary randomized two-sided matrix-vector queries

**Setting ID.** `CV_S_MG_RANDOM_BALL`

Minimax optimization

$$
\min_{x\in X}\max_{y\in\Delta_m}y^\top Ax,\quad A\in\mathbb{R}^{m\times n}.
$$

**Status.** Bounds missing

**TASK tags.** task family: Matrix computation; task family: Minimax

**MODEL tags.** geometry: Ball simplex; geometry: Compact geometry

**ORACLE tags.** feedback quality: Exact; interface family: Two sided real queries; operation: Two sided matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Saddle-point gap

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N matvec pair; setup: Initialization included

## 1. Setting specification

### Task

$$
\min_{x\in X}\max_{y\in\Delta_m}y^\top Ax,\quad A\in\mathbb{R}^{m\times n}.
$$

### Admissible model

Assume $A\in\mathbb R^{m\times n}$, $B_2^n=\{x\in\mathbb R^n:\|x\|_2\le1\}$, and $\Delta_m=\{y\in\mathbb R^m:y_i\ge0,\ \mathbf1^\top y=1\}$. Also $X=B_2^n$, with each row satisfying $\|A_{i,:}\|_2\le1$.

The dimensions $m,n$ are public and the matrix is hidden. Both strategy domains are compact and convex, ensuring a saddle point.

### Oracle interface

Public inputs include matrix dimensions $m,n$ and tolerance $\varepsilon$, together with the declared initial point and feasible-set information. The hidden function, operator, or matrix has no disclosed analytic representation.

$$
(x,y)\in\mathbb{R}^n\times\mathbb{R}^m\longmapsto(Ax,A^\top y)
$$

A pair of left and right matrix products forms one bundled call. Responses are exact, and query vectors need not belong to the strategy domains.

### Output

Return $(\widehat{x},\widehat{y})\in X\times\Delta_m$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\max_{v\in\Delta_m}v^\top A\widehat{x}-\min_{u\in X}\widehat{y}^\top Au
$$

The global gap is finite and nonnegative, and at most $2$ on the normalized class.

### Resource accounting

A bundled two-sided call costs $N_{\rm matvec}$. A single right or transpose product can be simulated by setting the other input to zero.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\max_{v\in\Delta_m}v^\top A\widehat{x}-\min_{u\in X}\widehat{y}^\top Au\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$\varepsilon$: Target tolerance for the complete weak-VI gap or global saddle gap, in the units of that gap. **Domain:** Positive real number.

$\varepsilon_0$: A sufficiently small accuracy threshold for the randomized matrix lower bound. **Domain:** Universal positive constant.

$m$: Number of matrix rows, or equivalently coordinates of the maximizing strategy **Domain:** Positive integer.

$n$: The number of matrix columns and minimizing-strategy coordinates. **Domain:** Positive integer.

$q$: This integer scale comes from the source randomized hard-instance construction. It is selected through $\varepsilon$ to specify the dimension window, not an additional oracle budget. **Domain:** Positive integer.

$q\asymp\varepsilon^{-2/3}$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm matvec}$: Number of bundled exact two-sided matrix-vector product calls **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\log,\ln,\log_+$: Natural logarithm and its nonnegative truncation **Domain:** Arguments of log and ln are positive; the argument of $\log_+$ may be zero.

$\log_+(t)=\log(\max\{1,t\})$

$A$: The hidden payoff matrix has maximizing strategies as rows and minimizing strategies as columns. **Domain:** $A\in\mathbb R^{m\times n}$.

$x,y$: Minimization variable and maximization strategy; query vectors need not satisfy strategy constraints **Domain:** $x\in\mathbb R^n,\ y\in\mathbb R^m$.

$X$: The public strategy set of the minimizing variable. **Domain:** $B_2^n$.

$\Delta_k,\mathbf1$: $k$-dimensional probability simplex and the all-ones vector of the corresponding dimension **Domain:** $k\ge1$.

$\Delta_k=\{u\in\mathbb R^k:u_j\ge0,\ \mathbf1^\top u=1\}$

$\operatorname{Gap}$: The displayed global saddle gap maximizes and minimizes over the output strategy domains. **Domain:** Nonnegative real number; not a gradient norm.

$B_2^k$: Closed k-dimensional Euclidean unit ball **Domain:** $k\ge1$.

$B_2^k=\{u\in\mathbb R^k:\|u\|_2\le1\}$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.** output: domain: B_2^n x Delta_m; postprocessing: arbitrary measurable transcript-based output unless algorithm restriction expressly states otherwise; metric: max_i(A xhat)_i + ||A^T yhat||_2; guarantee: One algorithm family chosen from public inputs satisfies for every legal instance and oracle law: Pr(max_i(A xhat)_i + ||A^T yhat||_2<=epsilon)>=2/3.

**Resource contract.** budget: fixed worst-case cap on every transcript; primary: N_matvec_pair; unit: one declared oracle call; auxiliary: projection/internal model solves separately retained, never counted as hidden oracle

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

#### Q2 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm matvec}(\mathcal A,I,\omega)
$$

**Scope.** The instancewise guarantee uses the same contract; dimension obeys the specification and theorem region.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - The sufficiently-large-dimension window.

**Region.** $0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}$, $m\ge4q,n\ge2q+1$.

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B2

$$
\widetilde{O}(\varepsilon^{-2/3})
$$

**Comparison argument.** The deterministic upper bound applies to a setting allowing randomization. The current randomized lower-bound candidate is excluded from the confirmed bracket because its authors explicitly mark the central proof as unverified. A near-optimal label is therefore unwarranted.

### R2 - The coarse-accuracy zero-query region.

**Region.** $\varepsilon\ge2$.

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B4

$$
0
$$

**Comparison argument.** Cost is nonnegative.

### R3 - The bound’s native applicability window.

**Region.** Require $m,n\ge1$ and $\varepsilon>0$. Only calls to the two matrix-product channels are counted. Once the matrix is recovered, internal exact solution is free.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

## 4. Bounds and supporting evidence

### B1 - Fixed random hard-matrix distribution and adaptive-transcript lower bound

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** lower

**Witness or lower-bound scope.** Witness type not certified

**Algorithm-scope qualification.** The authors claim an arbitrary-randomized lower bound but state that its core proof remains to be verified. It is excluded from the certified bracket; a claimed scope is not a verified theorem scope.

$$
\Omega\!\left(\frac{\varepsilon^{-2/3}}{\log^{2}(1/\varepsilon)\log\log(1/\varepsilon)}\right)
$$

**Sources.** [2](https://arxiv.org/pdf/2610.02095v2)

**Conditions.** Source Section 8 explicitly leaves verification of the central adaptive proof unresolved. This record reports the source statement without claiming an independent verification of that proof.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [2](https://arxiv.org/pdf/2610.02095v2) Definition3.1; Theorem3.2; Corollary3.3; Lemma3.4; Section8

Randomized two-sided matvec lower statements in ball/simplex and simplex/simplex geometries.

Full-space query vectors, feasible pair output, full saddle gap, fixed cap and success2/3. Dimensions grow with epsilon and are explicit. Paper itself flags adaptive-core proof verification in Section8; theorem statement audit is NOT certification of that proof.

### B2 - Deterministic matrix-vector method of Karmarkar–O’Carroll–Sidford

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The Karmarkar–O’Carroll–Sidford upper-bound method is deterministic. It also supplies an upper bound when randomization is allowed.

$$
\widetilde{O}(\varepsilon^{-2/3})
$$

**Sources.** [1](https://arxiv.org/pdf/2601.02347v3)

**Conditions.** The deterministic ball–simplex algorithm of Karmarkar et al. gives the upper bound, with hidden logarithms in $m,n,1/\varepsilon$. It is also available in the randomized algorithm class.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** log m; log n; $\log(1/\varepsilon)$

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) Theorems1.1–1.2; Section7.1–7.2

Deterministic matvec upper tilde O(epsilon^(-2/3)) for both normalized game geometries.

Queries in strategy domain form subset of unrestricted real vectors. Same full saddle gap. One pair of directional matvecs is at most constant overhead in our bundled operation. Logs may depend on m,n and epsilon; no arithmetic/runtime optimality.

### B3 - See the cited theorem

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Recover the hidden matrix with fixed basis queries and solve internally, or return public feasible strategies. Neither procedure randomizes.

$$
\min\{m,n\}
$$

**Sources.** [2](https://arxiv.org/pdf/2610.02095v2)

**Conditions.** Standard basis vectors recover the full matrix in at most $\min\{m,n\}$ two-sided calls. The resulting explicit matrix then defines an exactly solvable convex optimization problem.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [2](https://arxiv.org/pdf/2610.02095v2) Definition3.1; Theorem3.2; Corollary3.3; Lemma3.4; Section8

Randomized two-sided matvec lower statements in ball/simplex and simplex/simplex geometries.

Full-space query vectors, feasible pair output, full saddle gap, fixed cap and success2/3. Dimensions grow with epsilon and are explicit. Paper itself flags adaptive-core proof verification in Section8; theorem statement audit is NOT certification of that proof.

### B4 - Return any publicly known feasible strategy

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Recover the hidden matrix with fixed basis queries and solve internally, or return public feasible strategies. Neither procedure randomizes.

$$
0
$$

**Conditions.** Matrix normalization and the two strategy domains imply the global bound $\operatorname{Gap}\le2$.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Local argument.** A1

## 5. Local arguments

### A1 - Return any public feasible strategy

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Under the declared matrix normalization and strategy domains, every feasible bilinear payoff lies in $[-1,1]$. The difference between its maximum against a fixed minimizing strategy and its minimum against a fixed maximizing strategy is therefore at most two. Return any publicly specified feasible strategy pair without querying. It meets every tolerance $\varepsilon\ge2$ deterministically. Nonnegativity of query cost certifies exact zero cost.

## References

[1] Ishani Karmarkar; Liam O'Carroll; Aaron Sidford. Solving Matrix Games with Near-Optimal Matvec Complexity. 2026. arXiv:2601.02347v3, 2026-06-22.

https://arxiv.org/pdf/2601.02347v3

[2] Wendao Wu; Cong Fang. Randomized Matvec Lower Bounds for Simplex-Based Matrix Games. 2026. arXiv:2610.02095v2, 2026-10-19.

https://arxiv.org/pdf/2610.02095v2
