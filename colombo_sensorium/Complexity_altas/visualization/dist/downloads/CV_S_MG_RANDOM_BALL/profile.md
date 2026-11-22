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

Paper 2610.02095v2 is already recorded in this existing profile: reference CV_SRC_MG_2610_02095 and the linked excluded lower-bound statement are present. This is a recorded source claim pending proof review, not a missing setting or missing bibliography entry.

Directly checked the versioned primary HTML on 2026-11-22: Section 8, final paragraph, explicitly retains an unresolved verification task for the adaptive core argument. This note neither identifies a proved error nor certifies the argument.

Pending review is scoped to lower bound CV_S_MG_RANDOM_BALL__main__b1. Keep lower_scope_type=not_certified, included_in_bracket=false, eligible_for_bracket=false and selected_in_regimes empty until the targeted proof dependency is resolved. Independently justified endpoints, existing upper bounds and deterministic comparisons retain their current status.

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

Paper 2610.02095v2 is already recorded in this existing profile: reference CV_SRC_MG_2610_02095 and the linked excluded lower-bound statement are present. This is a recorded source claim pending proof review, not a missing setting or missing bibliography entry.

Directly checked the versioned primary HTML on 2026-11-22: Section 8, final paragraph, explicitly retains an unresolved verification task for the adaptive core argument. This note neither identifies a proved error nor certifies the argument.

Pending review is scoped to lower bound CV_S_MG_RANDOM_BALL__main__b1. Keep lower_scope_type=not_certified, included_in_bracket=false, eligible_for_bracket=false and selected_in_regimes empty until the targeted proof dependency is resolved. Independently justified endpoints, existing upper bounds and deterministic comparisons retain their current status.

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

**Local argument.** SIX_PROOF_c88bf8d96092

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

**Local argument.** CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122

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

**Local argument.** CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

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

**Local argument.** CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

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

**Local argument.** CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

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

**Local argument.** CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122

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

**Local argument.** CV_S_MG_RANDOM_BALL__main__proof_kos_full_target_20261122

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) section: Complete local proof CV_S_MG_RANDOM_BALL__main__proof_kos_full_target_20261122; theorem: Full-domain KOS-to-q2 transfer and integer envelope

The target transfer is distinct from the primary theorem and from the historical q1 source-scoped metric/resource record.

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) section: Section 1 (problem and oracle definition; Footnote 3) and Section 7.2 (proof of main results); theorem: Theorem 1.2; proof of Theorems 1.1 and 1.2; equations: (1)

The source explicitly counts matrix-vector products and hides only polylogarithmic factors in m,n,epsilon^(-1).

Primary HTML and the source main theorem definitions were re-read on 2026-11-22.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: fb295dc212d3e5cff1f2867477bad9826cff33b9dda2720ccb01ebe384394f63

### Native proof: SIX_PROOF_c88bf8d96092

Native pointer: /proofs/0; canonical SHA-256: e1615d8c95b04b61caeb5ae844662f25098ce45196f02e2e50b73b4cfa8e5ec4

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 6e1e3d55b0a5aab01289824739d2038cd227ae659f7fd031802f0e2d13b840ba

Return any public feasible strategy

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 01e13c1e771cf618c03c37b296b033bc74167499325485f7cd93d874363b46c7

Under the declared matrix normalization and strategy domains, every feasible bilinear payoff lies in $[-1,1]$. The difference between its maximum against a fixed minimizing strategy and its minimum against a fixed maximizing strategy is therefore at most two. Return any publicly specified feasible strategy pair without querying. It meets every tolerance $\varepsilon\ge2$ deterministically. Nonnegativity of query cost certifies exact zero cost.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

### Native proof: CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122

Native pointer: /proofs/1; canonical SHA-256: 92cfb59d7d360ffd235a07cfe15f5a0fb2606bb03cdb8a14cb7c90f9927639c3

#### Native field: kind

Native pointer: /proofs/1/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 13a9577154ab0929dcd95d7d4296806c8dbfd60d3e6117102cf110b39645085d

Exact reconstruction under the target query budget

#### Native field: statement

Native pointer: /proofs/1/statement; canonical SHA-256: d9ae123439c10a3c25c338b5c1e48ef56238dbd55c024850a5f2c3186df3724f

The target randomized accuracy complexity is at most min(m,n).

#### Native field: proof

Native pointer: /proofs/1/proof; canonical SHA-256: 8979e58015e051c5b7064416e78f3f0335a09df942bfc0181d69b6503a8d01ed

If n<=m, query (e_j,0) for j=1,...,n; each bundled response contains the j-th column A e_j. If m<n, query (0,e_i) for i=1,...,m and read each row from A^T e_i. Each is a legal arbitrary-real-vector query and costs exactly one bundled call. The full matrix is then known. A saddle point exists by compact convex strategy sets and bilinearity; exact internal solution is uncharged in this oracle model. The returned feasible pair has gap zero on every instance and every execution, so it meets the target per-instance probability 2/3 for all positive tolerances with pathwise cap min(m,n). This is a direct derivation for q2, not an assertion that the legacy source-scoped q1 is definitionally the same quantity.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: evidence_refs

Native pointer: /proofs/1/evidence_refs; canonical SHA-256: fb9ee8812133136a4dac730430c73bf0520f5212e028dfb19393c8290bd8cb44

#### Native item 1

Native pointer: /proofs/1/evidence_refs/0; canonical SHA-256: 246f369f217a2604aba64dc5fc88ec6d0a58eaef2311c636e4b0230f9158cb08

CV_S_MG_RANDOM_BALL__main__e_target_reconstruction_20261122

#### Native field: verification_scope

Native pointer: /proofs/1/verification_scope; canonical SHA-256: 1350e56715be218d79afee65f34c86d25295364f8783734a58733c7ab14251ec

Complete proof of the stated local endpoint or transfer only; external source theorems are cited premises, not independently re-proved.

### Native proof: CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

Native pointer: /proofs/2; canonical SHA-256: 48ed6df0dcb43915ccc85dc5a2cc7591610db779b7d00aa00326392e8160256c

#### Native field: kind

Native pointer: /proofs/2/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: dc3478521c871da351f9c64e2e4d0a38e78b473f2b223ffef4a13e0e26e32404

Ball-simplex exact zero-query threshold and thin-dimension endpoint

#### Native field: statement

Native pointer: /proofs/2/statement; canonical SHA-256: 038345a2a7fae31a004d36e803782af14cb9f063d3c62e5ae47bccd1d922edff

N*=0 for epsilon>=1; N*>=1 for 0<epsilon<1; if min(m,n)=1 then N*=1 for 0<epsilon<1.

#### Native field: proof

Native pointer: /proofs/2/proof; canonical SHA-256: db04f8c875ce852a8a1c9ffdf6e5ec46c8bfd96db688146a366c887c83da5209

For any normalized A and any y in Delta_m, choose x=0. The full saddle gap is max_i (A x)_i-min_{||u||<=1} y^T A u=||A^T y||<=sum_i y_i ||A_i||<=1. Thus zero queries suffice for epsilon>=1, deterministically, in all positive dimensions.
For necessity, fix a unit vector a=e_1 in R^n. Let A_+ have every row a^T and A_-=-A_+. Every feasible output (x,y) has gaps 1+a^T x and 1-a^T x respectively. When epsilon<1, their success events are disjoint. A zero-query randomized algorithm has the same output law under both fixed matrices. Consequently the two success probabilities sum to at most one, so at least one is at most 1/2<2/3. This proves N*>=1 for any fixed pathwise cap below one. At epsilon=1 the output x=0 succeeds for both and for the whole class; the boundary is closed on the zero side. If min(m,n)=1, the preceding reconstruction proof uses one call and exactly solves every instance. Hence the endpoint complexity is exactly one below 1 and zero at or above 1. No epsilon^(-2/3) lower bound is inferred.

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: evidence_refs

Native pointer: /proofs/2/evidence_refs; canonical SHA-256: 30dd37d3153e8eaf9376d3caadc34763c58950feae8f7cecdfcfdc9de649cf17

#### Native item 1

Native pointer: /proofs/2/evidence_refs/0; canonical SHA-256: c12dae6fea13c563634f25343892f7ca7fa4a215b98ae14822891f1ceb0eb707

CV_S_MG_RANDOM_BALL__main__e_exact_zero_threshold_20261122

#### Native field: verification_scope

Native pointer: /proofs/2/verification_scope; canonical SHA-256: 1350e56715be218d79afee65f34c86d25295364f8783734a58733c7ab14251ec

Complete proof of the stated local endpoint or transfer only; external source theorems are cited premises, not independently re-proved.

### Native proof: CV_S_MG_RANDOM_BALL__main__proof_kos_full_target_20261122

Native pointer: /proofs/3; canonical SHA-256: e9fbb94b404e56c586a4df1f8bf619b7b86059ed4cb91f56369db5798f98064e

#### Native field: kind

Native pointer: /proofs/3/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 60f6e638b8f69a2e3d21ac003e0531ed173cf2ef2212cd3f1bfc9a808c945651

Full-domain KOS v3 witness transfer to the randomized target quantity

#### Native field: statement

Native pointer: /proofs/3/statement; canonical SHA-256: b51f375be1ffa6d46e6ce6bd5a231a7f8c3b57d7bf19e3ce2d59c3d535418a4a

For every positive integer m,n and every epsilon>0, the exact target q2 satisfies N*(epsilon)<=min{min(m,n),K_KOS}, where eta=min{epsilon,1/2}, ell_KOS=1+log(2mn/eta), and K_KOS=ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS)) for universal C_KOS>=1 and p_KOS>=0. No lower-bound dimension window is required.

#### Native field: proof

Native pointer: /proofs/3/proof; canonical SHA-256: 830634749b673645bb822c7689cfa490ccc3296b39ae23fa378ef45c114a7a70

Source premise: Karmarkar--O'Carroll--Sidford, arXiv:2601.02347v3, Theorem 1.2, states a deterministic algorithm for every normalized game of this type with tilde-O(eta^(-2/3)) matvecs. Section 1 defines an eta-solution by the complete saddle gap, and its oracle returns the pair (A^T y,Ax). Footnote 3 limits the hidden factors to polylogarithms in m,n,eta^(-1). The source's Section 7.2 proof establishes this theorem without a lower bound on dimension depending on eta.

Class/output/metric map: the source class X=B_2^n, Y=Delta_m and max_i ||A_{i,:}||_2<=1 is exactly the present normalized class. Its feasible output pair is a legal target output, and its max_y y^T A xhat - min_x yhat^T A x metric is the target complete gap. Run the theorem at eta=min{epsilon,1/2}. Since eta<=epsilon, its deterministic gap guarantee implies target success probability one, hence at least 2/3, for every fixed admissible matrix. This is a one-way deterministic-witness inclusion into the randomized algorithm class; it transfers no deterministic lower bound.

Oracle/cost map: the source pair query is a legal target query because the target allows arbitrary real x,y. One such source pair is answered by exactly one target bundled response (Ax,A^T y), with order exchanged internally if needed. A source implementation that requests one directional product can obtain it using one target call with the other vector zero and discard the extra response. If two directions are requested sequentially, charge the actual two calls; do not divide directional counts by two or merge adaptively dependent queries. Thus the source count is an upper bound on target calls, up to at most a fixed convention factor absorbed in C_KOS. Exact arithmetic, known-domain optimization, and computation from returned data are free in both query models. The source has a deterministic worst-case call bound, so its witness satisfies the target pathwise cap; there is no expectation-to-cap conversion.

Uniform integer budget: because m,n>=1 and 0<eta<=1/2, the positive quantity ell_KOS=1+log(2mn/eta) dominates 1, log m, log n and log(1/eta). The source tilde-O bound can therefore be bounded by C_KOS eta^(-2/3) ell_KOS^(p_KOS) for fixed universal C_KOS>=1 and p_KOS>=0, increasing the constant for finite endpoint ranges. Round upward to K_KOS. For m,n>=2 use the source algorithm. When min(m,n)=1, use the separately proved one-call exact reconstruction instead, which is no greater than K_KOS. This handles singleton dimensions without relying on an entropy bound with log(1)=0. The choice eta<=1/2 also handles epsilon>=1 and avoids a false vanishing logarithmic factor. All dimensions are finite and positive, and epsilon=0 is outside the native accuracy domain.

Envelope: independently, basis reconstruction costs at most min(m,n) and returns gap zero. Both witnesses are chosen using public dimensions and accuracy, so select the smaller of their public proved integer caps. This proves the displayed min bound directly for q2. The old q1 source-scoped resource record is not identified with q2, and the old narrow b2 record is not needed for the new envelope. On every nonzero comparison updated here, 0<epsilon<2; consequently epsilon/4<=eta<=epsilon and the same upper is written min{min(m,n),tilde-O(epsilon^(-2/3))}, with only the stated positive dimension/precision logarithms suppressed. Existing exact zero and exact one-query rows are sharper and remain selected unchanged. This proves only an upper bound; the separate claimed randomized growing lower remains excluded.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: c9253033238d8e8851b7b0d25d2324124b0baa1afe30a95f2cdcd0003eea09ec

#### Native item 1

Native pointer: /proofs/3/source_refs/0; canonical SHA-256: e943536318ccb7c9310622727704c14d9634b8b2a9ebb06f646fbdad99afb067

CV_SRC_Karmarkar2026

#### Native field: premise_proof_refs

Native pointer: /proofs/3/premise_proof_refs; canonical SHA-256: 7089d17e8be3cbeaef22f931e9108eebc515a8fb6cf08137194a956ad8978abf

#### Native item 1

Native pointer: /proofs/3/premise_proof_refs/0; canonical SHA-256: d6b2775c66167eb07f60b75c3d5cc0e331cd039460bdc29e3caa04d9ed9d638b

CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122

#### Native field: evidence_refs

Native pointer: /proofs/3/evidence_refs; canonical SHA-256: 6ed637843ed0b93a426b7e417b6a30ca5fde240a2611fc47230b1d55f61d2a29

#### Native item 1

Native pointer: /proofs/3/evidence_refs/0; canonical SHA-256: 2b5b314ee983d4f6bbfa83bfb424769d858c8a03bef0b7e52b96c0f124940b70

CV_S_MG_RANDOM_BALL__main__e_kos_full_target_20261122

#### Native item 2

Native pointer: /proofs/3/evidence_refs/1; canonical SHA-256: fe011bade649935c62dad47c60fffde1fae6a41da9cfe60d02f12bf38789178c

CV_S_MG_RANDOM_BALL__main__e_kos_v3_primary_20261122

#### Native field: verification_scope

Native pointer: /proofs/3/verification_scope; canonical SHA-256: 566037894c720ce56ab4354e4fe19e8d390758f38834d2346c7754448a2008b9

Complete class, output, guarantee and query-budget transfer; the KOS algorithmic theorem is a cited primary-source premise, not independently re-proved.

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 326bbaf431528858924273ad95631ffe6f51aa35ded292c706cb70143c4a9e8c

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: f749d36cc1030be3788c939cb049cbc3ce314ff989caec6bd48b501122f4d210

#### Native field: setting_id

Native pointer: /joint_analysis/target/setting_id; canonical SHA-256: a675595a8ef60a624fb06df36377429853e4e3e2a7648d333a96c9419d9e21f6

CV_S_MG_RANDOM_BALL

#### Native field: contract_policy

Native pointer: /joint_analysis/target/contract_policy; canonical SHA-256: d4543a64b2bd7b127c223768269eb08c7418c637909f6a10de4ec875e4531c2d

Original common specification and view guarantees retained.

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 297f9b96c1bc849456f8f2b855e731c8298b58b07b3156bd218af864849a1740

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 662f72a6e3a7edac683f97497b4e0e369a503bf75c74386ddb58899e676ac84c

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 2170f789a5d6fd906a7d6c5cfe3eff28ee2580eee98653451fadca943f6962a9

CV_S_MG_RANDOM_BALL_p_258cd1f3e7

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 723a0e33d19a38ec3a1d7f4597003d14f0813c7b21755e1b38d7a6ae3e495fa6

CV_S_MG_RANDOM_BALL_p_bd49cae22d

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 734e45b8c7dac68eaecde21906ca15fbde4808c5c21391f0e9ab51a5d08ab446

CV_S_MG_RANDOM_BALL_p_b427b8da1a

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 70f479a2a104919fc67d0713cd4404aaacf41b707b016fe410fb09ac095ac4d1

CV_S_MG_RANDOM_BALL_p_39006b19fa

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 95011fd6c308c0cc10530a6cc812157b10101e87aa74d4199c230a1280110f06

CV_S_MG_RANDOM_BALL_p_752d295778

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 662f72a6e3a7edac683f97497b4e0e369a503bf75c74386ddb58899e676ac84c

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 2170f789a5d6fd906a7d6c5cfe3eff28ee2580eee98653451fadca943f6962a9

CV_S_MG_RANDOM_BALL_p_258cd1f3e7

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 723a0e33d19a38ec3a1d7f4597003d14f0813c7b21755e1b38d7a6ae3e495fa6

CV_S_MG_RANDOM_BALL_p_bd49cae22d

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 734e45b8c7dac68eaecde21906ca15fbde4808c5c21391f0e9ab51a5d08ab446

CV_S_MG_RANDOM_BALL_p_b427b8da1a

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 70f479a2a104919fc67d0713cd4404aaacf41b707b016fe410fb09ac095ac4d1

CV_S_MG_RANDOM_BALL_p_39006b19fa

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 95011fd6c308c0cc10530a6cc812157b10101e87aa74d4199c230a1280110f06

CV_S_MG_RANDOM_BALL_p_752d295778

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 78ed55afdb31099d2d73ae7856a3451e958b7052509dec6b53105cc7198cc6f7

The complete native model, parameters and tagged view domains; no source-scoped quantity is identified with a target minimax quantity without a separate proof.

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 195b039978d8dbf9f7b60b385d47061e37374bff6f84e935afaa4d06b823694b

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 5b62ca510517c057bb8e70d927827a2f54b1e133f6dec3e8a77e9f61cc5e228a

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 71203cec40abdc46a0d0563203780b1476fd6438ce7cfc1107018bd80d41e1c3

CV_S_MG_RANDOM_BALL__main__c_zero_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 810020b5ae570461e46351215edc70a07732f50b33f8f4c5cad5e9b49ca25884

Exact zero, including epsilon=1.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 810020b5ae570461e46351215edc70a07732f50b33f8f4c5cad5e9b49ca25884

Exact zero, including epsilon=1.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 6c4e5c34ab1292b664ebdeb9f469ed23b37f8d8cc223a9ec085cfc0225336944

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 9b7a01278104731924675956871c862a5479f57d1658f46093ae0f487109df65

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 021d7f284cd50c83326bce9436390da059e4431fe6e8896dd331e3fd30f7dccd

CV_S_MG_RANDOM_BALL__main__b_zero_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 2fa1e1e38a22c97ed54259d40d2de5c8dc1a5143b24093faf2f85c80467003c4

$m,n\ge1$ and $\varepsilon\ge1$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 2fa1e1e38a22c97ed54259d40d2de5c8dc1a5143b24093faf2f85c80467003c4

$m,n\ge1$ and $\varepsilon\ge1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 49378ca38da5df56f23ed5e46458db4fdc8b48da46f0bf23d170cf1280b4eff9

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 49fd896d34f621e4259ebf14c8c234e816c0261c8595dbc3e790d23247117a6c

CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: d6567c99cd10fcec386d42d525aae8c4aa5f076d171847b86e2942955742af16

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 6b59421df5db815b87f29ed0c7a7d5732224fec831c60f5dc1797a8f598117d8

CV_S_MG_RANDOM_BALL__main__b_zero_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 2fa1e1e38a22c97ed54259d40d2de5c8dc1a5143b24093faf2f85c80467003c4

$m,n\ge1$ and $\varepsilon\ge1$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 2fa1e1e38a22c97ed54259d40d2de5c8dc1a5143b24093faf2f85c80467003c4

$m,n\ge1$ and $\varepsilon\ge1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 49378ca38da5df56f23ed5e46458db4fdc8b48da46f0bf23d170cf1280b4eff9

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 49fd896d34f621e4259ebf14c8c234e816c0261c8595dbc3e790d23247117a6c

CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 41a103be54b65cd57baece16b13ad0d303563b2da59f5b2245505bccabffe65b

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 90dc727754333f44cb5cf3e4eecbcbaea563d7fcf7b72ae8e091a64febf4d284

CV_S_MG_RANDOM_BALL__main__c_thin_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 4ded24727f76715da2681beb91f54aea81f01f2945f48836d262932014facd4e

Exact one bundled query.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 4ded24727f76715da2681beb91f54aea81f01f2945f48836d262932014facd4e

Exact one bundled query.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: bc14de78e590625e8586b4b60e2ccaf725a1e32c282e82def5581d82a45adb03

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: a5de7fc8044a9c202b2ee280171196068aaaef92e133c8ccc8344a619d426dee

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: c2eb1345eee246e69dbd783f6b12d4bf343714390a794705ef2898b3592b30c3

CV_S_MG_RANDOM_BALL__main__b_one_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 760671463b8b6fb62f893608b2d06fab7a04ad8b24e37bccd1bf3bab9a697180

$\min\{m,n\}=1$ and $0<\varepsilon<1$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 760671463b8b6fb62f893608b2d06fab7a04ad8b24e37bccd1bf3bab9a697180

$\min\{m,n\}=1$ and $0<\varepsilon<1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 7089d17e8be3cbeaef22f931e9108eebc515a8fb6cf08137194a956ad8978abf

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: d6b2775c66167eb07f60b75c3d5cc0e331cd039460bdc29e3caa04d9ed9d638b

CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 20c515fe9265a869b415fa3834064251cba17deb5b5049813f52b1da9a0a1fab

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: c8624d7df177912367870107cbb1697a6cda04180d87e287a0db2fb0711c6547

CV_S_MG_RANDOM_BALL__main__b_one_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 760671463b8b6fb62f893608b2d06fab7a04ad8b24e37bccd1bf3bab9a697180

$\min\{m,n\}=1$ and $0<\varepsilon<1$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 760671463b8b6fb62f893608b2d06fab7a04ad8b24e37bccd1bf3bab9a697180

$\min\{m,n\}=1$ and $0<\varepsilon<1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 49378ca38da5df56f23ed5e46458db4fdc8b48da46f0bf23d170cf1280b4eff9

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 49fd896d34f621e4259ebf14c8c234e816c0261c8595dbc3e790d23247117a6c

CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: ee78a2678b1a63c8b5ed8ea73ceb1062832cbc8d895479a6ced2049803c80d09

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 76fc6342ce118fe5a7d667b41f8e3625ca5752c6484a3cb3d15b1e495d6b2875

CV_S_MG_RANDOM_BALL__main__c_hard_window_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: d80100f23285d37a225ac848b5956a282d7300066d9f8a781565bfafd1483ebb

\min\{\min(m,n),\widetilde O(\varepsilon^{-2/3})\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: a504bd3c72c1b0b9cf94ce1932f39826b936e6c09f7cc8f73048287d2eae9a00

At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: a504bd3c72c1b0b9cf94ce1932f39826b936e6c09f7cc8f73048287d2eae9a00

At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 4e60760c2a59162be33f29c05fd97bc1fab68bd8574b14e2b2b9345de49af55a

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 11ccf8afaff128f1db115fb4735008710aa5964e275493c61b8b5af0b68eb857

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 1e032a9043b7b7fa6a273c19b6c17fc6c557cd8ccee6aabfd0f35781c433e613

CV_S_MG_RANDOM_BALL__main__b_kos_full_target_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 7d192e59c93ff4e49e0ad6e66892d9d1e4099e7840076da7138c2ed87fbea41c

$0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}$, $m\ge4q,n\ge2q+1$. Additionally $\varepsilon<1$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 82e3595955f587fd14a5c5cbe83c3c87683ede63d8ab2513cf27e466bd7e0ddf

All finite m,n>=1 and epsilon>0 in the normalized target class.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 450337259bf95f6d01d1eb4fd85b59e4618241b5df5048fc24af4669f5bb82b4

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 8af0ae3d470c2cd15936582c2f71d71b77b1f653082766431a765dcc203c7954

CV_S_MG_RANDOM_BALL__main__proof_kos_full_target_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: fd0a79722c699ed443e329b807a721657d14bfae4640287da78f4f7adf94e02a

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: ca3f52057ec97e479c237ba8c474d9abf5e70db6d5c5020165ade8a1288a400e

CV_S_MG_RANDOM_BALL__main__b_target_reconstruction_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: 7d192e59c93ff4e49e0ad6e66892d9d1e4099e7840076da7138c2ed87fbea41c

$0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}$, $m\ge4q,n\ge2q+1$. Additionally $\varepsilon<1$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 82e3595955f587fd14a5c5cbe83c3c87683ede63d8ab2513cf27e466bd7e0ddf

All finite m,n>=1 and epsilon>0 in the normalized target class.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7089d17e8be3cbeaef22f931e9108eebc515a8fb6cf08137194a956ad8978abf

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: d6b2775c66167eb07f60b75c3d5cc0e331cd039460bdc29e3caa04d9ed9d638b

CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: ec5041b4ce807e6c3778a43aedf75a0844958552f5d935f37110cbd6f1856f96

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: c8624d7df177912367870107cbb1697a6cda04180d87e287a0db2fb0711c6547

CV_S_MG_RANDOM_BALL__main__b_one_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 7d192e59c93ff4e49e0ad6e66892d9d1e4099e7840076da7138c2ed87fbea41c

$0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}$, $m\ge4q,n\ge2q+1$. Additionally $\varepsilon<1$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 7d192e59c93ff4e49e0ad6e66892d9d1e4099e7840076da7138c2ed87fbea41c

$0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}$, $m\ge4q,n\ge2q+1$. Additionally $\varepsilon<1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 49378ca38da5df56f23ed5e46458db4fdc8b48da46f0bf23d170cf1280b4eff9

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 49fd896d34f621e4259ebf14c8c234e816c0261c8595dbc3e790d23247117a6c

CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 555e344f66fc115756073f6463fae12773df3cff6c3ba3b50f1c64dc95fa961a

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 440c776ccb74a92e922d6eefef6212961cf58eaa0deaf3cd735bc58c22e4394e

KOS accuracy is clamped to eta<=1/2; logarithms stay positive and caps are rounded upward. Singleton dimensions retain their exact zero/one rows.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: c51011119c5c4ff97e177eb8d8c9c7b92ccbe638246d18bce5bea386c16010df

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: b0ae48ff40f1ce75a4a2b6325c68a5f4628a118fd0943294f8da72cdb63831af

CV_S_MG_RANDOM_BALL__main__c_remaining_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: d80100f23285d37a225ac848b5956a282d7300066d9f8a781565bfafd1483ebb

\min\{\min(m,n),\widetilde O(\varepsilon^{-2/3})\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: a504bd3c72c1b0b9cf94ce1932f39826b936e6c09f7cc8f73048287d2eae9a00

At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: a504bd3c72c1b0b9cf94ce1932f39826b936e6c09f7cc8f73048287d2eae9a00

At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 208537cc4301778e8b1ea97f161c1f8db80079aa1d7537f168dea325376e7fa6

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: 262c963c824afa38bc5253c20c640086fd9ffbee16aea6d0f44ce63bfacb5f86

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 1e032a9043b7b7fa6a273c19b6c17fc6c557cd8ccee6aabfd0f35781c433e613

CV_S_MG_RANDOM_BALL__main__b_kos_full_target_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 301d08e88046de329984f4fa3d0b54fd69e98bb6316a0998b8616bb13ff5f37e

$\min\{m,n\}\ge2$, $0<\varepsilon<1$, and not the complete high-dimensional source-window predicate H.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 82e3595955f587fd14a5c5cbe83c3c87683ede63d8ab2513cf27e466bd7e0ddf

All finite m,n>=1 and epsilon>0 in the normalized target class.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 450337259bf95f6d01d1eb4fd85b59e4618241b5df5048fc24af4669f5bb82b4

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 8af0ae3d470c2cd15936582c2f71d71b77b1f653082766431a765dcc203c7954

CV_S_MG_RANDOM_BALL__main__proof_kos_full_target_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: d17a184a36ffc9479d55a1feb9bbdf0f028d98d78977c96a86a1007038222768

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: ca3f52057ec97e479c237ba8c474d9abf5e70db6d5c5020165ade8a1288a400e

CV_S_MG_RANDOM_BALL__main__b_target_reconstruction_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: 301d08e88046de329984f4fa3d0b54fd69e98bb6316a0998b8616bb13ff5f37e

$\min\{m,n\}\ge2$, $0<\varepsilon<1$, and not the complete high-dimensional source-window predicate H.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 82e3595955f587fd14a5c5cbe83c3c87683ede63d8ab2513cf27e466bd7e0ddf

All finite m,n>=1 and epsilon>0 in the normalized target class.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7089d17e8be3cbeaef22f931e9108eebc515a8fb6cf08137194a956ad8978abf

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: d6b2775c66167eb07f60b75c3d5cc0e331cd039460bdc29e3caa04d9ed9d638b

CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 65170baf5c31b60e7c89334f4f2c1435bf72c74c2f3512af40e9533116a697c6

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: c8624d7df177912367870107cbb1697a6cda04180d87e287a0db2fb0711c6547

CV_S_MG_RANDOM_BALL__main__b_one_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 301d08e88046de329984f4fa3d0b54fd69e98bb6316a0998b8616bb13ff5f37e

$\min\{m,n\}\ge2$, $0<\varepsilon<1$, and not the complete high-dimensional source-window predicate H.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 301d08e88046de329984f4fa3d0b54fd69e98bb6316a0998b8616bb13ff5f37e

$\min\{m,n\}\ge2$, $0<\varepsilon<1$, and not the complete high-dimensional source-window predicate H.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 49378ca38da5df56f23ed5e46458db4fdc8b48da46f0bf23d170cf1280b4eff9

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 49fd896d34f621e4259ebf14c8c234e816c0261c8595dbc3e790d23247117a6c

CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: 555e344f66fc115756073f6463fae12773df3cff6c3ba3b50f1c64dc95fa961a

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: 440c776ccb74a92e922d6eefef6212961cf58eaa0deaf3cd735bc58c22e4394e

KOS accuracy is clamped to eta<=1/2; logarithms stay positive and caps are rounded upward. Singleton dimensions retain their exact zero/one rows.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 53e4eb42ce9b6a222c6103be33ed9f34a07e4319d6f56a42d645fd61dbdb8ead

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 4cf68769103b49f4fdea29dfa18373f4e9a246fb29fd2cfcb55d07a948dc6e20

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 0167b89f70b5186b54513db2acc6743ff678b811698d5ef10007bff8a9974d6b

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 71203cec40abdc46a0d0563203780b1476fd6438ce7cfc1107018bd80d41e1c3

CV_S_MG_RANDOM_BALL__main__c_zero_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 2fa1e1e38a22c97ed54259d40d2de5c8dc1a5143b24093faf2f85c80467003c4

$m,n\ge1$ and $\varepsilon\ge1$.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: e34f7eba1233aa4462531a8f9c38648c88b37865c1158113739dbaea7253f2b1

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 71203cec40abdc46a0d0563203780b1476fd6438ce7cfc1107018bd80d41e1c3

CV_S_MG_RANDOM_BALL__main__c_zero_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 8dcaac3655a3051a68b12d492a0ef630eb86fb405ec145a145432aeb838addaa

Exact short proof of both sides of the zero-query threshold.

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: b07b0f9658e946d1e40bc850b25145b8a2c8caf5813f2917e821e39c4209b02a

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 90dc727754333f44cb5cf3e4eecbcbaea563d7fcf7b72ae8e091a64febf4d284

CV_S_MG_RANDOM_BALL__main__c_thin_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 760671463b8b6fb62f893608b2d06fab7a04ad8b24e37bccd1bf3bab9a697180

$\min\{m,n\}=1$ and $0<\varepsilon<1$.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: a0b57a5c0e476cb2b4ac1a0c93025c0dc17abcb49e3eaf4ef98def2f087c3767

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 90dc727754333f44cb5cf3e4eecbcbaea563d7fcf7b72ae8e091a64febf4d284

CV_S_MG_RANDOM_BALL__main__c_thin_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 83c94a6549c6d2b31ab58173ed43fac0a086be7648df02d10fff294f4debd4c3

One-query reconstruction matches a randomized zero-query impossibility.

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 53d181e61ec847410ade51945489137278b3b9d8b9349bb0b9ce790824d780ed

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 76fc6342ce118fe5a7d667b41f8e3625ca5752c6484a3cb3d15b1e495d6b2875

CV_S_MG_RANDOM_BALL__main__c_hard_window_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 7d192e59c93ff4e49e0ad6e66892d9d1e4099e7840076da7138c2ed87fbea41c

$0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}$, $m\ge4q,n\ge2q+1$. Additionally $\varepsilon<1$.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: b838441274076824c6e2814217a3c0dd73b8ad171b9e9404c3df93c15c221a41

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 76fc6342ce118fe5a7d667b41f8e3625ca5752c6484a3cb3d15b1e495d6b2875

CV_S_MG_RANDOM_BALL__main__c_hard_window_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 5449d4674df6113362cde822346485ef323635ee4094b7fe6be9e21655e7f546

The new complete KOS v3-to-q2 proof gives a deterministic pathwise cap in every positive dimension, independent of the source lower-bound window H. Take the minimum with the separately proved q2 basis-reconstruction cap. Explicitly the integer envelope is min{min(m,n),ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS))}. The displayed tilde form is valid on this row because 0<epsilon<2; eta=min{epsilon,1/2}. This changes only the upper side and leaves all lower exclusions and endpoint predicates intact.

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: c78ba1763e84eca4ad1f5f7dd2194116d098bc6f524ca1dd23aa09aff7f37e67

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: b0ae48ff40f1ce75a4a2b6325c68a5f4628a118fd0943294f8da72cdb63831af

CV_S_MG_RANDOM_BALL__main__c_remaining_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 301d08e88046de329984f4fa3d0b54fd69e98bb6316a0998b8616bb13ff5f37e

$\min\{m,n\}\ge2$, $0<\varepsilon<1$, and not the complete high-dimensional source-window predicate H.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 866a77f227156cbf3a6e6a51e6b2971edbdfab7a1b4da4e54ccc35fd9a44695f

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: b0ae48ff40f1ce75a4a2b6325c68a5f4628a118fd0943294f8da72cdb63831af

CV_S_MG_RANDOM_BALL__main__c_remaining_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: 5449d4674df6113362cde822346485ef323635ee4094b7fe6be9e21655e7f546

The new complete KOS v3-to-q2 proof gives a deterministic pathwise cap in every positive dimension, independent of the source lower-bound window H. Take the minimum with the separately proved q2 basis-reconstruction cap. Explicitly the integer envelope is min{min(m,n),ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS))}. The displayed tilde form is valid on this row because 0<epsilon<2; eta=min{epsilon,1/2}. This changes only the upper side and leaves all lower exclusions and endpoint predicates intact.

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 7481541e12643c6b92e959039da0bd751f40354f696dd28d0b17e9092b48b04c

Within positive dimensions and positive tolerance, first split epsilon>=1 from epsilon<1. Below 1, split min(m,n)=1 from min(m,n)>=2; in the latter split by the original source-window H. These four cells are disjoint and cover the full target-accuracy domain. Legacy q1 is retained only as an unselected source-scoped record; reconstruction is separately proved for q2.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 972ea8a41362086708909ce378df98205a855f46924d80e1b28c5836b554c444

See explicitly marked missing-lower or retained deterministic residual cells.

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 305fd45c6bddee57f34402e8a31f5c5b2b41bd2cf2225313fef607b938a3d28c

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: a0654d8fd5027e5f6f98f0be510546e69e8e460bce54434b3b9f08d2b9b55d01

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 600df104489af8e2331ed945a6731c915f608eed348b59a258c74029b84d5202

CV_S_MG_RANDOM_BALL_mathematical_update_20261122

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: cb96035ecbae7df227084eeca52927bd1b8bcf3cc51c362f601c0f8f170fa6d4

Prove the exact ball-simplex zero-query threshold epsilon>=1, improving the earlier sufficient condition epsilon>=2. Add a lower bound N>=1 valid for arbitrary randomized algorithms and close the exact zero/one-query complexity when min(m,n)=1. Independently prove the min(m,n) reconstruction upper bound for q2, without equating it implicitly with the original source-scoped q1. The main high-dimensional window has only a proved constant lower bound and therefore a polynomial gap; the unverified epsilon^(-2/3) lower-bound claim remains excluded.

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 9bc5fa618c62e4cd980b9115e134224f29da9d8392b50289b20d538a0c7e207c

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 71203cec40abdc46a0d0563203780b1476fd6438ce7cfc1107018bd80d41e1c3

CV_S_MG_RANDOM_BALL__main__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: 90dc727754333f44cb5cf3e4eecbcbaea563d7fcf7b72ae8e091a64febf4d284

CV_S_MG_RANDOM_BALL__main__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/impact/0/comparison_ids/2; canonical SHA-256: 76fc6342ce118fe5a7d667b41f8e3625ca5752c6484a3cb3d15b1e495d6b2875

CV_S_MG_RANDOM_BALL__main__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/impact/0/comparison_ids/3; canonical SHA-256: b0ae48ff40f1ce75a4a2b6325c68a5f4628a118fd0943294f8da72cdb63831af

CV_S_MG_RANDOM_BALL__main__c_remaining_20261122

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 984ee132a57143c1c90dba25a0f0fb82a83e47605f80d83e1c295151915db07c

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 569048a860ca624e585b8a6585e738c5e0d13e0a45831a586541a57782caed33

CV_S_MG_RANDOM_BALL_kos_full_target_20261122

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 0663e251644c0a2694b5a2aa4c953e4bf14c7cb36d807c28736671d8e98615fb

improvement

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 69ae467c4fd15634c53fbd5eca7249059adb5e24df218a719580f05f4a23fdab

Extend the certified KOS upper to all positive dimensions and accuracies under the target q2; select it with reconstruction outside H as well as inside H.

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 0c6ce517c09fb21878ae18a8b4d75cab1074ca2028cd7c550bedafdca22575d4

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 76fc6342ce118fe5a7d667b41f8e3625ca5752c6484a3cb3d15b1e495d6b2875

CV_S_MG_RANDOM_BALL__main__c_hard_window_20261122

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: b0ae48ff40f1ce75a4a2b6325c68a5f4628a118fd0943294f8da72cdb63831af

CV_S_MG_RANDOM_BALL__main__c_remaining_20261122

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 0e5184668fab51d577af7659b6a3116571d710e67084da38784c1340bff19881

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 8181d2c860576d2794369f5228afc34d216faa6153ba8cc63c88b24cd94f4a5a

Verify the adaptive-core argument or locate a corrected source before adopting the claimed epsilon^(-2/3) randomized lower.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 7fe07e7359d60730a9f65692655516138854202a0457af42a4f97ddee9a3a237

Close the genuine dimension/accuracy gap above the elementary one-query lower.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 463dd4edbc8b092a7c5c2fbef3c6471c898a49131bace98ea9befbfc1ee04a45

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 9bc5fa618c62e4cd980b9115e134224f29da9d8392b50289b20d538a0c7e207c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 71203cec40abdc46a0d0563203780b1476fd6438ce7cfc1107018bd80d41e1c3

CV_S_MG_RANDOM_BALL__main__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 90dc727754333f44cb5cf3e4eecbcbaea563d7fcf7b72ae8e091a64febf4d284

CV_S_MG_RANDOM_BALL__main__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 76fc6342ce118fe5a7d667b41f8e3625ca5752c6484a3cb3d15b1e495d6b2875

CV_S_MG_RANDOM_BALL__main__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: b0ae48ff40f1ce75a4a2b6325c68a5f4628a118fd0943294f8da72cdb63831af

CV_S_MG_RANDOM_BALL__main__c_remaining_20261122

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: c55d3bf8e166968932e27c21a26f703cfe11a47fa8a650bf864fb829b49d99a4

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: 732d644c9a4910bc79c46406734ebdc342be508a168e6d85b2ba9497049e2722

Targeted checks of the named primary versions and complete local proofs; no exhaustive literature claim.

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 0816dbd435c18c4ae1513e19c9a6f606a634c4b09a21c77a8a17c21e9214a1c5

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 643c7fc3c8b693bf099d084c2acf6d42c996c850910e32362aaf365a7002cd87

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: 56faeda9bb894418ff9945a53fbcabbc9c4d62e4e2a5e17f6ce8e0b16051e82d

pending-20261122-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: 8181d2c860576d2794369f5228afc34d216faa6153ba8cc63c88b24cd94f4a5a

Verify the adaptive-core argument or locate a corrected source before adopting the claimed epsilon^(-2/3) randomized lower.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 9bc5fa618c62e4cd980b9115e134224f29da9d8392b50289b20d538a0c7e207c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 71203cec40abdc46a0d0563203780b1476fd6438ce7cfc1107018bd80d41e1c3

CV_S_MG_RANDOM_BALL__main__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/1; canonical SHA-256: 90dc727754333f44cb5cf3e4eecbcbaea563d7fcf7b72ae8e091a64febf4d284

CV_S_MG_RANDOM_BALL__main__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/2; canonical SHA-256: 76fc6342ce118fe5a7d667b41f8e3625ca5752c6484a3cb3d15b1e495d6b2875

CV_S_MG_RANDOM_BALL__main__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/3; canonical SHA-256: b0ae48ff40f1ce75a4a2b6325c68a5f4628a118fd0943294f8da72cdb63831af

CV_S_MG_RANDOM_BALL__main__c_remaining_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 8d14ccd5368015735025e0df9c69fe9258020045d3a1e95d1cec8d1d066f9317

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: 116cc72611b7d9bbc01357f04524c3a2e8c10665ec909c36222d1aad26e7983c

pending-20261122-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 7fe07e7359d60730a9f65692655516138854202a0457af42a4f97ddee9a3a237

Close the genuine dimension/accuracy gap above the elementary one-query lower.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 9bc5fa618c62e4cd980b9115e134224f29da9d8392b50289b20d538a0c7e207c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 71203cec40abdc46a0d0563203780b1476fd6438ce7cfc1107018bd80d41e1c3

CV_S_MG_RANDOM_BALL__main__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/1; canonical SHA-256: 90dc727754333f44cb5cf3e4eecbcbaea563d7fcf7b72ae8e091a64febf4d284

CV_S_MG_RANDOM_BALL__main__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/2; canonical SHA-256: 76fc6342ce118fe5a7d667b41f8e3625ca5752c6484a3cb3d15b1e495d6b2875

CV_S_MG_RANDOM_BALL__main__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/3; canonical SHA-256: b0ae48ff40f1ce75a4a2b6325c68a5f4628a118fd0943294f8da72cdb63831af

CV_S_MG_RANDOM_BALL__main__c_remaining_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 557c6f4098c6d961dee802fb36bab2559745bea941967f4bd5050c9b8d6e8674

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 39fc030c426d7c61a27d59640b2671b3a4809a89e76604c67580ac8204f667a5

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: ca3f52057ec97e479c237ba8c474d9abf5e70db6d5c5020165ade8a1288a400e

CV_S_MG_RANDOM_BALL__main__b_target_reconstruction_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 7089d17e8be3cbeaef22f931e9108eebc515a8fb6cf08137194a956ad8978abf

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: d6b2775c66167eb07f60b75c3d5cc0e331cd039460bdc29e3caa04d9ed9d638b

CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 86a56affecced021a612c5515c54235026178e695e4178c4e2de5ba496c5d9d7

#### Native item 1

Native pointer: /joint_analysis/provenance/0/target_domain/0; canonical SHA-256: 6ba3424dd3d6ae088d44a8de318cc1a5ba11535600e90e2cf54271d46f9912f3

CV_S_MG_RANDOM_BALL__main__r_full_target_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 15194c526fe4592a1f86dc96d8875a72422d992ea986c4d5eeef24ad7986aa28

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 021d7f284cd50c83326bce9436390da059e4431fe6e8896dd331e3fd30f7dccd

CV_S_MG_RANDOM_BALL__main__b_zero_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 49378ca38da5df56f23ed5e46458db4fdc8b48da46f0bf23d170cf1280b4eff9

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 49fd896d34f621e4259ebf14c8c234e816c0261c8595dbc3e790d23247117a6c

CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 0db36c52a48934aa7b1f075d9e24d7c24d572e6a97448a4d1a26169d6d830bb1

#### Native item 1

Native pointer: /joint_analysis/provenance/1/target_domain/0; canonical SHA-256: cf932ad1ab158bdac8eb90063e9845ff8ee22706efea698bafadf27848a9dc01

CV_S_MG_RANDOM_BALL__main__r_zero_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 78dd8cf0f9e9fc9fc1a10d4606e23d5c46581b3f793006d583cde1cda141c83c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 6b59421df5db815b87f29ed0c7a7d5732224fec831c60f5dc1797a8f598117d8

CV_S_MG_RANDOM_BALL__main__b_zero_lower_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 49378ca38da5df56f23ed5e46458db4fdc8b48da46f0bf23d170cf1280b4eff9

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 49fd896d34f621e4259ebf14c8c234e816c0261c8595dbc3e790d23247117a6c

CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 0db36c52a48934aa7b1f075d9e24d7c24d572e6a97448a4d1a26169d6d830bb1

#### Native item 1

Native pointer: /joint_analysis/provenance/2/target_domain/0; canonical SHA-256: cf932ad1ab158bdac8eb90063e9845ff8ee22706efea698bafadf27848a9dc01

CV_S_MG_RANDOM_BALL__main__r_zero_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 1cc80daec9d4133360e83851ea6a3af05be4ce736facadbfc4229bb7f331dab8

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: c8624d7df177912367870107cbb1697a6cda04180d87e287a0db2fb0711c6547

CV_S_MG_RANDOM_BALL__main__b_one_lower_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 49378ca38da5df56f23ed5e46458db4fdc8b48da46f0bf23d170cf1280b4eff9

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: 49fd896d34f621e4259ebf14c8c234e816c0261c8595dbc3e790d23247117a6c

CV_S_MG_RANDOM_BALL__main__proof_exact_zero_threshold_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 63b05679b0a7880e8824d85ff9ad81acce8d5bd8005aee4ae43eaebbb4dbb3f3

#### Native item 1

Native pointer: /joint_analysis/provenance/3/target_domain/0; canonical SHA-256: 6d9aad46ebc61c0b42da6f2ea06b8713ce21bc3e759d96f4c205b8417b2557f4

CV_S_MG_RANDOM_BALL__main__r_positive_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: e65f1e913447def35d4fd275a116edf71bbe8c975d522c055f270f57032641dd

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: c2eb1345eee246e69dbd783f6b12d4bf343714390a794705ef2898b3592b30c3

CV_S_MG_RANDOM_BALL__main__b_one_upper_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 7089d17e8be3cbeaef22f931e9108eebc515a8fb6cf08137194a956ad8978abf

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: d6b2775c66167eb07f60b75c3d5cc0e331cd039460bdc29e3caa04d9ed9d638b

CV_S_MG_RANDOM_BALL__main__proof_target_reconstruction_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 6f0346d131a29525765db79c91c4deeb392b0352df626226ae706a26c6862c68

#### Native item 1

Native pointer: /joint_analysis/provenance/4/target_domain/0; canonical SHA-256: ccb8415635b3787dfa9437df3c127aed935cb668b63f6b1bc600d2c0d3ecd659

CV_S_MG_RANDOM_BALL__main__r_thin_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: 922c839e4212dc8b6894e0ba76f4c05baef16875290ebbd11a47364fe29f9c44

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: 1e032a9043b7b7fa6a273c19b6c17fc6c557cd8ccee6aabfd0f35781c433e613

CV_S_MG_RANDOM_BALL__main__b_kos_full_target_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: f7a61f49ae5e60151d293133b29642f789e81e3d59dc194e683d14af3fdbef2b

source_theorem_with_analyst_transfer

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: c9253033238d8e8851b7b0d25d2324124b0baa1afe30a95f2cdcd0003eea09ec

#### Native item 1

Native pointer: /joint_analysis/provenance/5/source_refs/0; canonical SHA-256: e943536318ccb7c9310622727704c14d9634b8b2a9ebb06f646fbdad99afb067

CV_SRC_Karmarkar2026

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 450337259bf95f6d01d1eb4fd85b59e4618241b5df5048fc24af4669f5bb82b4

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: 8af0ae3d470c2cd15936582c2f71d71b77b1f653082766431a765dcc203c7954

CV_S_MG_RANDOM_BALL__main__proof_kos_full_target_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: f30ef474c153882e3559b28e269dedb5fcbd9a05a1a89ceb3c3fef25bab1044a

KOS arXiv:2601.02347v3 Theorem 1.2: all normalized games; deterministic complete-gap algorithm.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 86a56affecced021a612c5515c54235026178e695e4178c4e2de5ba496c5d9d7

#### Native item 1

Native pointer: /joint_analysis/provenance/5/target_domain/0; canonical SHA-256: 6ba3424dd3d6ae088d44a8de318cc1a5ba11535600e90e2cf54271d46f9912f3

CV_S_MG_RANDOM_BALL__main__r_full_target_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 6ac7c049d48965d8052556dc2653ddf8d7c41bcc1c86a7a3c93066a2b63b3760

Identity instance/output/gap; legal pair queries; deterministic pathwise cap; public accuracy clamp and singleton reconstruction.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: 740a81b5e585360c4c68be7971c517951aa749c6e9ebe926ebf44decf9c80176

Section 1, Theorem 1.2, Footnote 3, Section 7.2 proof; https://arxiv.org/html/2601.02347v3

## References

[1] Ishani Karmarkar; Liam O'Carroll; Aaron Sidford. Solving Matrix Games with Near-Optimal Matvec Complexity. 2026. arXiv:2601.02347v3, 2026-06-22.

https://arxiv.org/pdf/2601.02347v3

[2] Wendao Wu; Cong Fang. Randomized Matvec Lower Bounds for Simplex-Based Matrix Games. 2026. arXiv:2610.02095v2, 2026-10-19.

https://arxiv.org/pdf/2610.02095v2
