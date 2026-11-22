# Ball-simplex matrix games: arbitrary randomized two-sided matrix-vector queries

**Setting ID.** `CV_S_MG_RANDOM_BALL`

Minimax optimization

Normalized ball-simplex matrix games with arbitrary randomized two-sided matvec queries. Exact zero and one-query endpoints are established by local proofs; the high-dimensional epsilon-dependent randomized lower remains excluded. A full-domain KOS v3 upper is combined with exact reconstruction under the randomized target quantity.

**Status.** Polynomial gap present

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

The complete gap can be as large as 2 for an arbitrary pair, but the public choice $x=0$ gives gap at most 1 for every matrix. The exact zero-query threshold for this randomized target is therefore $\varepsilon=1$.

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

$\eta$: Public target accuracy used to run the KOS witness; clamping avoids nonpositive precision logarithms. **Domain:** Real number in (0,1/2].

$\eta=\min\{\varepsilon,1/2\}$

$\ell_{\mathrm{KOS}}$: Positive dimension and precision logarithm dominating the polylogarithmic factors in KOS v3. **Domain:** Positive real number.

$\ell_{\mathrm{KOS}}=1+\log(2mn/\eta)$

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

### R1 - Exact zero-query region

**Region.** $m,n\ge1$ and $\varepsilon\ge1$.

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B7

$$
0
$$

**Upper bound.** B6

$$
0
$$

**Gap or comparison.** Exact zero, including epsilon=1.

**Comparison argument.** Exact short proof of both sides of the zero-query threshold.

### R2 - Exact one-query regime

**Region.** $\min\{m,n\}=1$ and $0<\varepsilon<1$.

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B8

$$
1
$$

**Upper bound.** B9

$$
1
$$

**Gap or comparison.** Exact one bundled query.

**Comparison argument.** One-query reconstruction matches a randomized zero-query impossibility.

### R3 - High-dimensional source window with a proved elementary lower

**Region.** $0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}$, $m\ge4q,n\ge2q+1$. Additionally $\varepsilon<1$.

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Polynomial gap

**Lower bound.** B8

$$
1
$$

**Upper bound.** B10, B5

$$
\min\{\min(m,n),\widetilde O(\varepsilon^{-2/3})\}
$$

**Gap or comparison.** At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

**Comparison argument.** The new complete KOS v3-to-q2 proof gives a deterministic pathwise cap in every positive dimension, independent of the source lower-bound window H. Take the minimum with the separately proved q2 basis-reconstruction cap. Explicitly the integer envelope is min{min(m,n),ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS))}. The displayed tilde form is valid on this row because 0<epsilon<2; eta=min{epsilon,1/2}. This changes only the upper side and leaves all lower exclusions and endpoint predicates intact.

### R4 - Other positive-cost dimensions

**Region.** $\min\{m,n\}\ge2$, $0<\varepsilon<1$, and not the complete high-dimensional source-window predicate H.

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Polynomial gap

**Lower bound.** B8

$$
1
$$

**Upper bound.** B10, B5

$$
\min\{\min(m,n),\widetilde O(\varepsilon^{-2/3})\}
$$

**Gap or comparison.** At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

**Comparison argument.** The new complete KOS v3-to-q2 proof gives a deterministic pathwise cap in every positive dimension, independent of the source lower-bound window H. Take the minimum with the separately proved q2 basis-reconstruction cap. Explicitly the integer envelope is min{min(m,n),ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS))}. The displayed tilde form is valid on this row because 0<epsilon<2; eta=min{epsilon,1/2}. This changes only the upper side and leaves all lower exclusions and endpoint predicates intact.

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

**Conditions.** Source Section 8 explicitly leaves verification of the central adaptive proof unresolved. This record reports the source statement without claiming an independent verification of that proof.; 2026-11-22 source check still finds v2 as the latest discoverable version. Its Section 8 final paragraph retains the adaptive-core proof-verification qualification; the new local endpoint proofs do not resolve that argument.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [2](https://arxiv.org/pdf/2610.02095v2) Definition3.1; Theorem3.2; Corollary3.3; Lemma3.4; Section8

Randomized two-sided matvec lower statements in ball/simplex and simplex/simplex geometries.

Full-space query vectors, feasible pair output, full saddle gap, fixed cap and success2/3. Dimensions grow with epsilon and are explicit. Paper itself flags adaptive-core proof verification in Section8; theorem statement audit is NOT certification of that proof.

### B2 - Deterministic matrix-vector method of Karmarkar–O’Carroll–Sidford

**Admission.** Eligible evidence; not selected in the displayed bracket

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

**Admission.** Eligible evidence; not selected in the displayed bracket

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

**Admission.** Eligible evidence; not selected in the displayed bracket

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

### B5 - Basis reconstruction and exact internal solution

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\min\{m,n\}
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** A2

**Source location.**  section: Complete local proof CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122; theorem: Exact reconstruction under the target query budget

Analyst-derived argument is kept separate from published/preprint evidence.

### B6 - Return x=0 and any public feasible y

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** A3

**Source location.**  section: Complete local proof CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122; theorem: Ball-simplex exact zero-query threshold and thin-dimension endpoint

Analyst-derived argument is kept separate from published/preprint evidence.

### B7 - Nonnegative pathwise query count

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** A3

**Source location.**  section: Complete local proof CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122; theorem: Ball-simplex exact zero-query threshold and thin-dimension endpoint

Analyst-derived argument is kept separate from published/preprint evidence.

### B8 - Two fixed opposite rank-one matrices

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** A3

**Source location.**  section: Complete local proof CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122; theorem: Ball-simplex exact zero-query threshold and thin-dimension endpoint

Analyst-derived argument is kept separate from published/preprint evidence.

### B9 - One call reconstructs a one-row or one-column matrix

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** A2

**Source location.**  section: Complete local proof CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122; theorem: Exact reconstruction under the target query budget

Analyst-derived argument is kept separate from published/preprint evidence.

### B10 - KOS v3 Theorem 1.2 with accuracy clamping; exact reconstruction for singleton dimensions

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\left\lceil C_{\mathrm{KOS}}\eta^{-2/3}\ell_{\mathrm{KOS}}^{p_{\mathrm{KOS}}}\right\rceil
$$

**Sources.** [1](https://arxiv.org/pdf/2601.02347v3)

**Conditions.** All finite positive integer m,n and every epsilon>0 in the normalized target class; no source lower-bound window H is imposed.

**Dimension conditions.** All positive dimensions; singleton-side instances are covered by the explicit reconstruction branch.

**Oracle correspondence.** Each source pair query is one legal target bundled query; separately requested directional products each cost at most one bundled query.

**Guarantee conversion.** A deterministic complete-gap eta-solution is an epsilon-solution with success probability one, hence at least 2/3.

**Resource conversion.** Deterministic worst-case integer cap; no conversion from expected cost and no division by two of sequential directional products.

**Constants.** C_KOS>=1 and p_KOS>=0 are fixed universal constants from the KOS v3 theorem and the displayed oracle convention map, independent of m,n,epsilon.

**Logarithmic factors.** $\ell_{\mathrm{KOS}}^{p_{\mathrm{KOS}}}$ with $\ell_{\mathrm{KOS}}=1+\log(2mn/\min\{\varepsilon,1/2\})$; no polynomial dimension factor is suppressed.

**Local argument.** A4

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) section: Complete local proof CV_S_MG_RANDOM_BALL__main__proof_kos_full_target_20261122; theorem: Full-domain KOS-to-q2 transfer and integer envelope

The target transfer is distinct from the primary theorem and from the historical q1 source-scoped metric/resource record.

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) section: Section 1 (problem and oracle definition; Footnote 3) and Section 7.2 (proof of main results); theorem: Theorem 1.2; proof of Theorems 1.1 and 1.2; equations: (1)

The source explicitly counts matrix-vector products and hides only polylogarithmic factors in m,n,epsilon^(-1).

Primary HTML and the source main theorem definitions were re-read on 2026-11-22.

## 5. Local arguments

### A1 - Return any public feasible strategy

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Under the declared matrix normalization and strategy domains, every feasible bilinear payoff lies in $[-1,1]$. The difference between its maximum against a fixed minimizing strategy and its minimum against a fixed maximizing strategy is therefore at most two. Return any publicly specified feasible strategy pair without querying. It meets every tolerance $\varepsilon\ge2$ deterministically. Nonnegativity of query cost certifies exact zero cost.

### A2 - Exact reconstruction under the target query budget

The target randomized accuracy complexity is at most min(m,n).

If n<=m, query (e\_j,0) for j=1,...,n; each bundled response contains the j-th column A e\_j. If m<n, query (0,e\_i) for i=1,...,m and read each row from A^T e\_i. Each is a legal arbitrary-real-vector query and costs exactly one bundled call. The full matrix is then known. A saddle point exists by compact convex strategy sets and bilinearity; exact internal solution is uncharged in this oracle model. The returned feasible pair has gap zero on every instance and every execution, so it meets the target per-instance probability 2/3 for all positive tolerances with pathwise cap min(m,n). This is a direct derivation for q2, not an assertion that the legacy source-scoped q1 is definitionally the same quantity.

### A3 - Ball-simplex exact zero-query threshold and thin-dimension endpoint

N\*=0 for epsilon>=1; N\*>=1 for 0<epsilon<1; if min(m,n)=1 then N\*=1 for 0<epsilon<1.

For any normalized A and any y in Delta\_m, choose x=0. The full saddle gap is max\_i (A x)\_i-min\_{||u||<=1} y^T A u=||A^T y||<=sum\_i y\_i ||A\_i||<=1. Thus zero queries suffice for epsilon>=1, deterministically, in all positive dimensions.
For necessity, fix a unit vector a=e\_1 in R^n. Let A\_+ have every row a^T and A\_-=-A\_+. Every feasible output (x,y) has gaps 1+a^T x and 1-a^T x respectively. When epsilon<1, their success events are disjoint. A zero-query randomized algorithm has the same output law under both fixed matrices. Consequently the two success probabilities sum to at most one, so at least one is at most 1/2<2/3. This proves N\*>=1 for any fixed pathwise cap below one. At epsilon=1 the output x=0 succeeds for both and for the whole class; the boundary is closed on the zero side. If min(m,n)=1, the preceding reconstruction proof uses one call and exactly solves every instance. Hence the endpoint complexity is exactly one below 1 and zero at or above 1. No epsilon^(-2/3) lower bound is inferred.

### A4 - Full-domain KOS v3 witness transfer to the randomized target quantity

For every positive integer m,n and every epsilon>0, the exact target q2 satisfies N\*(epsilon)<=min{min(m,n),K\_KOS}, where eta=min{epsilon,1/2}, ell\_KOS=1+log(2mn/eta), and K\_KOS=ceil(C\_KOS eta^(-2/3) ell\_KOS^(p\_KOS)) for universal C\_KOS>=1 and p\_KOS>=0. No lower-bound dimension window is required.

Source premise: Karmarkar--O'Carroll--Sidford, arXiv:2601.02347v3, Theorem 1.2, states a deterministic algorithm for every normalized game of this type with tilde-O(eta^(-2/3)) matvecs. Section 1 defines an eta-solution by the complete saddle gap, and its oracle returns the pair (A^T y,Ax). Footnote 3 limits the hidden factors to polylogarithms in m,n,eta^(-1). The source's Section 7.2 proof establishes this theorem without a lower bound on dimension depending on eta.

Class/output/metric map: the source class X=B\_2^n, Y=Delta\_m and max\_i ||A\_{i,:}||\_2<=1 is exactly the present normalized class. Its feasible output pair is a legal target output, and its max\_y y^T A xhat - min\_x yhat^T A x metric is the target complete gap. Run the theorem at eta=min{epsilon,1/2}. Since eta<=epsilon, its deterministic gap guarantee implies target success probability one, hence at least 2/3, for every fixed admissible matrix. This is a one-way deterministic-witness inclusion into the randomized algorithm class; it transfers no deterministic lower bound.

Oracle/cost map: the source pair query is a legal target query because the target allows arbitrary real x,y. One such source pair is answered by exactly one target bundled response (Ax,A^T y), with order exchanged internally if needed. A source implementation that requests one directional product can obtain it using one target call with the other vector zero and discard the extra response. If two directions are requested sequentially, charge the actual two calls; do not divide directional counts by two or merge adaptively dependent queries. Thus the source count is an upper bound on target calls, up to at most a fixed convention factor absorbed in C\_KOS. Exact arithmetic, known-domain optimization, and computation from returned data are free in both query models. The source has a deterministic worst-case call bound, so its witness satisfies the target pathwise cap; there is no expectation-to-cap conversion.

Uniform integer budget: because m,n>=1 and 0<eta<=1/2, the positive quantity ell\_KOS=1+log(2mn/eta) dominates 1, log m, log n and log(1/eta). The source tilde-O bound can therefore be bounded by C\_KOS eta^(-2/3) ell\_KOS^(p\_KOS) for fixed universal C\_KOS>=1 and p\_KOS>=0, increasing the constant for finite endpoint ranges. Round upward to K\_KOS. For m,n>=2 use the source algorithm. When min(m,n)=1, use the separately proved one-call exact reconstruction instead, which is no greater than K\_KOS. This handles singleton dimensions without relying on an entropy bound with log(1)=0. The choice eta<=1/2 also handles epsilon>=1 and avoids a false vanishing logarithmic factor. All dimensions are finite and positive, and epsilon=0 is outside the native accuracy domain.

Envelope: independently, basis reconstruction costs at most min(m,n) and returns gap zero. Both witnesses are chosen using public dimensions and accuracy, so select the smaller of their public proved integer caps. This proves the displayed min bound directly for q2. The old q1 source-scoped resource record is not identified with q2, and the old narrow b2 record is not needed for the new envelope. On every nonzero comparison updated here, 0<epsilon<2; consequently epsilon/4<=eta<=epsilon and the same upper is written min{min(m,n),tilde-O(epsilon^(-2/3))}, with only the stated positive dimension/precision logarithms suppressed. Existing exact zero and exact one-query rows are sharper and remain selected unchanged. This proves only an upper bound; the separate claimed randomized growing lower remains excluded.

**Sources.** [1](https://arxiv.org/pdf/2601.02347v3)

## References

[1] Ishani Karmarkar; Liam O'Carroll; Aaron Sidford. Solving Matrix Games with Near-Optimal Matvec Complexity. 2026. arXiv:2601.02347v3, 2026-06-22.

https://arxiv.org/pdf/2601.02347v3

[2] Wendao Wu; Cong Fang. Randomized Matvec Lower Bounds for Simplex-Based Matrix Games. 2026. arXiv:2610.02095v2, 2026-10-19.

https://arxiv.org/pdf/2610.02095v2
