# Simplex matrix games with two-sided matrix-vector products

**Setting ID.** `CV_S_SIMPLEX_MATRIX_GAME`

Saddle-point problems

Solve the normalized matrix game $\min_{x\in\Delta_n}\max_{y\in\Delta_m}y^{\mathsf T}Ax$.

**Status.** Other quantified gap present; Bounds missing

**Gap classes present.** Other quantified gap; Logarithmic gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Simplex matrix zero sum game; solution concept: Fixed budget saddle gap; task family: Matrix computation; task family: Minimax; task family: Saddle point

**MODEL tags.** geometry: Compact geometry; geometry: Simplex simplex

**ORACLE tags.** feedback quality: Exact; interface family: Two sided real queries; operation: Two sided matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic algorithms; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point; object: Primal dual pair; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Fixed budget gap risk; criterion: Saddle-point gap

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N bundle; measure: N matvec pair; precision: Bit precision not counted; setup: Initialization included

## 1. Setting specification

### Task

Solve the normalized matrix game $\min_{x\in\Delta_n}\max_{y\in\Delta_m}y^{\mathsf T}Ax$.

### Admissible model

The hidden matrix is $A\in\mathbb R^{m\times n}$, with $\max_{i,j}|A_{ij}|\le1$ and public positive integers $m,n$.

$\Delta_k=\{u\in\mathbb R^k:u\ge0,\ \mathbf1^{\mathsf T}u=1\}$ for every positive integer $k$. Both strategy sets are compact and convex, and a saddle point exists.

### Oracle interface

For arbitrary vectors $(x,y)\in\mathbb R^n\times\mathbb R^m$, one query returns the exact bundle $(Ax,A^{\mathsf T}y)$. Query vectors need not be probability vectors.

One bundled left/right multiplication costs one call. A single-direction multiplication is obtained by setting the other query vector to zero. The matrix is fixed before interaction and its entries are not directly accessible.

Dimensions and strategy sets are public. The requested budget or accuracy is specified by the comparison quantity for the selected view.

### Output

Return $(\widehat x,\widehat y)\in\Delta_n\times\Delta_m$. Unqueried outputs and arbitrary measurable transcript postprocessing are permitted; no certificate is required.

### Loss or accuracy criterion

The loss is $\operatorname{Gap}(\widehat x,\widehat y)=\max_{v\in\Delta_m}v^{\mathsf T}A\widehat x-\min_{u\in\Delta_n}\widehat y^{\mathsf T}Au$. It lies in $[0,2]$.

### Resource accounting

One bundled two-sided query increments $N_{\rm matvec}$ by one. A single right or transpose product can be obtained by setting the other input to zero and is charged as one bundled call.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

#### Deterministic risk

Any measurable sequential adaptive deterministic algorithm is allowed. Queries and outputs may use the complete history, with no additional span, zero-support, communication, or memory restriction.

At public budget $N$, select one deterministic algorithm and then take the worst output gap over every admissible fixed matrix. The call cap holds on every instance:

$$
r_{\rm det}^{\star}(N;m,n)=\inf_{\mathcal A\in\mathfrak A_{\rm det}:\,\sup_A N_{\rm matvec}(\mathcal A,A)\le N}\sup_{A\in[-1,1]^{m\times n}}\left[\max_{v\in\Delta_m}v^{\mathsf T}A\widehat x-\min_{u\in\Delta_n}\widehat y^{\mathsf T}Au\right]
$$

Here $\mathfrak A_{\rm det}$ is the deterministic adaptive class declared above; $\widehat x,\widehat y$ are its feasible outputs.

**View qualification.** This deterministic fixed-budget risk view uses public $N\in\mathbb N_{\ge1}$ and dimensions $m,n\ge2$.

**Budget convention.** fixed worst-case number N of bundled two-sided products

#### Randomized accuracy

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the following guarantee for every admissible fixed matrix:

$$
\exists\mathcal A\ \forall A\in[-1,1]^{m\times n}:\quad\Pr\!\left(\max_{v\in\Delta_m}v^{\mathsf T}A\widehat x-\min_{u\in\Delta_n}\widehat y^{\mathsf T}Au\le\varepsilon\right)\ge\frac23
$$

Probability is over private algorithmic randomness only. The hidden matrix is fixed before interaction.

**View qualification.** This randomized accuracy view allows positive integer dimensions $m,n\ge1$. Its quantity is the smallest fixed worst-case call budget achieving $\Pr(\operatorname{Gap}(\widehat x,\widehat y)\le\varepsilon)\ge2/3$ for every admissible fixed matrix.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$N$: A uniform cap on bundled two-sided matrix-vector calls. **Domain:** Nonnegative integer; the deterministic risk view uses $N\ge1$.

$d$: The total dimension of the two strategy spaces. **Domain:** An integer at least four.

$d=n+m$

$\varepsilon$: Target full-gap tolerance in the randomized accuracy view; an auxiliary tolerance for rate inversion in the deterministic risk view. **Domain:** Positive real number.

$m$: Number of matrix rows and coordinates of the maximizing strategy y. **Domain:** Positive integer; the deterministic risk view requires $m,n\ge2$.

$n$: Number of matrix columns and coordinates of the minimizing strategy x. **Domain:** Positive integer; the deterministic risk view requires $m,n\ge2$.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$N_{\rm matvec}$: Number of bundled exact two-sided matrix-vector product calls **Domain:** Nonnegative integer count; expected work is its expectation.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\log,\ln,\log_+$: Natural logarithm and its nonnegative truncation **Domain:** Arguments of log and ln are positive; the argument of $\log_+$ may be zero.

$\log_+(t)=\log(\max\{1,t\})$

$C$: A sufficient universal constant in the source lower-bound dimension window, not a matrix-norm parameter. **Domain:** A fixed positive constant with unspecified numerical value.

$A$: Hidden payoff matrix **Domain:** $A\in\mathbb R^{m\times n}$.

$\max_{i,j}|A_{ij}|\le1$.

$x,y$: Minimizing and maximizing variables; query vectors may be arbitrary real vectors. **Domain:** $x\in\mathbb R^n,\ y\in\mathbb R^m$.

$\widehat x,\widehat y$: The feasible strategies returned as the final output **Domain:** $\widehat x\in\Delta_n,\ \widehat y\in\Delta_m$.

$r^\star(N;m,n),\ r_{\rm det}^{\star}(N;m,n)$: Equivalent notation for the optimal deterministic worst-case output gap at budget N. **Domain:** Nonnegative risk, for $N\ge1$ and $m,n\ge2$.

$$
r_{\rm det}^{\star}(N;m,n)=\inf_{\mathcal A\in\mathfrak A_{\rm det}:\,\sup_A N_{\rm matvec}(\mathcal A,A)\le N}\sup_{A\in[-1,1]^{m\times n}}\left[\max_{v\in\Delta_m}v^{\mathsf T}A\widehat x-\min_{u\in\Delta_n}\widehat y^{\mathsf T}Au\right]
$$

$\Delta_k,\mathbf1$: $k$-dimensional probability simplex and the all-ones vector of the corresponding dimension **Domain:** $k\ge1$.

$\Delta_k=\{u\in\mathbb R^k:u_j\ge0,\ \mathbf1^\top u=1\}$

$\operatorname{Gap}$: Full primal-dual gap over the two strategy simplices **Domain:** $[0,2]$.

$$
\operatorname{Gap}(\widehat x,\widehat y)=\max_{v\in\Delta_m}v^{\mathsf T}A\widehat x-\min_{u\in\Delta_n}\widehat y^{\mathsf T}Au
$$

$f$: Bilinear payoff determined by the hidden matrix **Domain:** $\mathbb R^n\times\mathbb R^m\to\mathbb R$.

$f(x,y)=y^{\mathsf T}Ax$

$\varepsilon_0$: A sufficiently small accuracy threshold for the randomized matrix lower bound. **Domain:** Universal positive constant.

$q$: This integer scale comes from the source randomized hard-instance construction. It is selected through $\varepsilon$ to specify the dimension window, not an additional oracle budget. **Domain:** Positive integer.

$q\asymp\varepsilon^{-2/3}/\log^{1/3}(1/\varepsilon)$

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$X$: The public strategy set of the minimizing variable. **Domain:** $\Delta_n$.

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

$\mathfrak A_{\rm det}$: Deterministic measurable adaptive algorithms with the declared query and output interface **Domain:** The deterministic risk algorithm view.

## 3. Complexity bracket

### Compared quantities

#### Q1 - fixed budget risk

**View.** Deterministic risk

$$
r_{\rm det}^{\star}(N;m,n)=\inf_{\mathcal A\in\mathfrak A_{\rm det}:\,\sup_A N_{\rm matvec}(\mathcal A,A)\le N}\sup_{A\in[-1,1]^{m\times n}}\left[\max_{v\in\Delta_m}v^{\mathsf T}A\widehat x-\min_{u\in\Delta_n}\widehat y^{\mathsf T}Au\right]
$$

**Scope.** fixed n,m,N satisfying exact theorem window

**Optimization direction.** minimize

For every admissible fixed matrix, the deterministic algorithm makes at most $N$ bundled two-sided calls and returns two feasible strategies. This quantity is the worst-case gap at budget $N$. A single directional product is charged as one bundled call with the other input set to zero.

#### Q2 - source scoped metric resource statement

**View.** Randomized accuracy

**Metric contract.** guarantee: One algorithm family chosen from public inputs satisfies for every legal instance and oracle law: Pr(max_i(A xhat)_i - min_j(A^T yhat)_j<=epsilon)>=2/3.; metric: max_i(A xhat)_i - min_j(A^T yhat)_j; output: domain: Delta_n x Delta_m; postprocessing: arbitrary measurable transcript-based output unless algorithm restriction expressly states otherwise

**Resource contract.** auxiliary: projection/internal model solves separately retained, never counted as hidden oracle; budget: fixed worst-case cap on every transcript; primary: N_matvec_pair; unit: one declared oracle call

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

#### Q3 - target accuracy cost

**View.** Randomized accuracy

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm matvec}(\mathcal A,I,\omega)
$$

**Scope.** The instancewise guarantee uses the same contract; dimension obeys the specification and theorem region.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - Earlier high-dimensional evidence window

**Region.** $N>C,\ m>C N,\ n>C N^2\log N$

**Views.** Deterministic risk

**Quantity.** Q1

**Resource.** Worst-case saddle gap under a fixed total two-sided matrix–vector query budget N.

**Status.** Other quantified gap

**Lower bound.** B2

$$
\Omega(1/(\log(m)\sqrt{\log(n)}\,N^{5/2}))
$$

**Upper bound.** B1

$$
O(\sqrt{\log(n+1)\log(m+1)}/N)
$$

**Gap or comparison.** $O\!\left(N^{3/2}\log(m)\sqrt{\log(n)\log(n+1)\log(m+1)}\right)$

**Comparison argument.** The bounds compare directly for the same arbitrary adaptive deterministic class and full saddle gap. The displayed factor is the upper bound divided by the lower bound. Tighter overlapping regions are recorded separately.

### R2 - Large-dimension regime in the 2026 result

**Region.** Assume $N>C$, $m>2CN$, and $n>CN^2\log N$; $C$ is the source theorem's universal sufficient constant.

**Views.** Deterministic risk

**Quantity.** Q1

**Resource.** Saddle-gap risk under a fixed budget

**Status.** Logarithmic gap

**Lower bound.** B3

$$
\Omega\!\left(\frac{1}{N[\sqrt{N\log(nm)}+\log(nm)]}\right)
$$

**Upper bound.** B4

$$
\widetilde{O}(N^{-3/2})
$$

**Gap or comparison.** $\operatorname{polylog}(m,n,N)$

**Comparison argument.** Use the v4 risk exponent 3/2 and the 2026 upper bound, retaining all dimension logarithms. The earlier exponent 5/2 remains as dominated historical evidence.

### R3 - Complete-matrix recovery regime

**Region.** $N\ge\min\{m,n\}$.

**Views.** Deterministic risk

**Quantity.** Q1

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B5

$$
0
$$

**Comparison argument.** Nonnegative gap and a zero upper bound imply zero risk.

### R4 - The sufficiently-large-dimension window.

**Region.** $0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}/\log^{1/3}(1/\varepsilon)$, $m,n\ge4q$.

**Views.** Randomized accuracy

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Lower bound missing

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B7, B10

$$
\begin{cases}0,&\varepsilon\ge2-2/\max\{m,n\},\\\widetilde O(\varepsilon^{-2/3}),&0<\varepsilon<2-2/\max\{m,n\}.\end{cases}
$$

**Gap or comparison.** Exact zero on r1 intersect r5, with no multiplicative ratio; a positive lower rate is missing elsewhere.

**Comparison argument.** Intersect each branch with this comparison's unchanged r1 predicate. The new zero-call branch proves exact zero wherever r1 meets r5; outside r5 retain the existing upper theorem and the absence of a certified positive lower rate. The excluded randomized lower claim remains excluded.

### R5 - The coarse-accuracy zero-query region.

**Region.** $\varepsilon\ge2$.

**Views.** Randomized accuracy

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B9

$$
0
$$

**Comparison argument.** Cost is nonnegative.

### R6 - The bound’s native applicability window.

**Region.** Require $m,n\ge1$ and $\varepsilon>0$. Only calls to the two matrix-product channels are counted. Once the matrix is recovered, internal exact solution is free.

**Views.** Randomized accuracy

**Quantity.** Q2

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B8

### R7 - Dimension-dependent zero-query endpoint

**Region.** $m,n\ge1,\quad \varepsilon>0,\quad \varepsilon\ge 2-2/\max\{m,n\}$.

**Views.** Randomized accuracy

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B10

$$
0
$$

**Comparison argument.** The uniform-strategy proof gives zero calls on the entire declared region. Nonnegative query cost yields exact equality. A multiplicative ratio is inapplicable at zero.

## 4. Bounds and supporting evidence

### B1 - entropy Mirror-Prox on product simplexes

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic risk

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Mirror-Prox uses exact operator responses, fixed step sizes, and deterministic proximal updates. Its averaged output is also deterministic.

$$
O(\sqrt{\log(n+1)\log(m+1)}/N)
$$

**Sources.** [4](https://www2.isye.gatech.edu/~nemirovs/SIOPT_MP_2004.pdf)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N bundle.** N

**entropy prox.** $O(N)$ exact entropic proximal operations on known geometry.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [4](https://www2.isye.gatech.edu/~nemirovs/SIOPT_MP_2004.pdf) pdf pages: 17; section: Section5; theorem: Example1, equation(5.14)

Entropy-based proximal geometry gives error bounded by the matrix entrywise bound times $O(\sqrt{\log(n+1)\log(m+1)}/N)$. Proximal arithmetic is excluded from the count of left and right matrix-vector calls.

### B2 - adaptive deterministic matrix completion with Gaussian row normalization

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic risk

**Witness or lower-bound scope.** All deterministic adaptive algorithms

**Algorithm-scope qualification.** The source theorem covers arbitrary adaptive deterministic queries, beyond linear-span iterations. It does not thereby give an arbitrary-randomized lower bound.

$$
\Omega(1/(\log(m)\sqrt{\log(n)}\,N^{5/2}))
$$

**Sources.** [3](https://raw.githubusercontent.com/mlresearch/v291/main/assets/kornowski25a/kornowski25a.pdf)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** Assume $m>CN$, $n>CN^2\log N$, and $N>C$, retaining the source's universal constant $C$.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.** The quantity $N$ is the public two-sided query budget. The displayed formula bounds gap risk at that budget and is not a call-count expression.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** A strategy pair with full saddle gap at most $\varepsilon$ gives a maximizing strategy with one-sided suboptimality at most $\varepsilon$. Proposition 14 of the source converts a simplex-simplex solver to an $\ell_1$-ball-simplex solver by doubling matrix width without increasing bundled matvec calls. This record is a version-specific deterministic risk lower bound. The sharper exponent is recorded separately; neither is promoted to an unrestricted randomized lower bound.

**Source location.** [3](https://raw.githubusercontent.com/mlresearch/v291/main/assets/kornowski25a/kornowski25a.pdf) pdf pages: 5; 11; 12; section: Sections2,5; theorem: Definition4, Remark5, Proposition14, Theorem15

The cited Theorem 15 constructs hard instances on an $\ell_1$ ball and a simplex; Proposition 14 converts this to two simplices by doubling the matrix width. Its risk accuracy exponent is $N^{-5/2}$, with the dimension logarithms retained, and its lower bound covers deterministic algorithms only. The later $N^{-3/2}$ risk result is recorded separately.

### B3 - Kornowski–Shamir v4: hard matrices for the two-sided oracle and the simplex reduction.

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic risk

**Witness or lower-bound scope.** All deterministic adaptive algorithms

**Algorithm-scope qualification.** The source theorem covers arbitrary adaptive deterministic queries, beyond linear-span iterations. It does not thereby give an arbitrary-randomized lower bound.

$$
\Omega\!\left(\frac{1}{N[\sqrt{N\log(nm)}+\log(nm)]}\right)
$$

**Sources.** [2](https://arxiv.org/pdf/2412.06990v4)

**Conditions.** $N>C,m>2CN,n>CN^2\log N$. Arbitrary real query vectors and arbitrary feasible outputs are allowed.

**Dimension conditions.** High-dimensional window of the source

**Guarantee conversion.** Worst-case gap risk at a fixed budget; no conversion to query complexity is asserted.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [2](https://arxiv.org/pdf/2412.06990v4) Theorem5.1 for norm p=1; Proposition6.1; Corollary6.2

The improved deterministic simplex/simplex lower risk is order N^(-3/2) up to logs; old2025 bound N^(-5/2) is not the current strongest source version.

Source n x d orientation maps to old atlas n x m with d=m/2 in signed-simplex reduction. Full saddle gap dominates the returned w strategy suboptimality. Original lower is deterministic; do not attribute randomized lower to it. Width factor2 changes constants only; need m>2C N and n>C N^2 log N.

### B4 - A deterministic accelerated matrix-game method, with the accuracy–query relation inverted.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic risk

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The Karmarkar–O’Carroll–Sidford upper-bound method is deterministic. It also supplies an upper bound when randomization is allowed.

$$
\widetilde{O}(N^{-3/2})
$$

**Sources.** [1](https://arxiv.org/pdf/2601.02347v3)

**Conditions.** Theorems 1.1-1.2 give the query upper bound $\widetilde O(\varepsilon^{-2/3})$. Inverting this relation yields the fixed-budget risk bound.

The suppressed factors involve $\log m,\log n,\log N$. For small budgets, truncate the bound at $\operatorname{Gap}\le2$.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Logarithmic factors.** polylog(m,n,N)

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) description: Theorems 1.1–1.2; Section 7.2

$$
\widetilde O(N^{-3/2})
$$

Theorems 1.1-1.2 require $\widetilde O(\varepsilon^{-2/3})$ matrix-vector products. Inverting this relation gives the fixed-budget risk upper bound. Suppressed factors involve $\log m,\log n,\log N$; for small budgets, truncate at $\operatorname{Gap}\le2$.

### B5 - Recover the matrix with basis queries, then solve the known linear program using uncharged internal computation.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic risk

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Recover the hidden matrix with fixed basis queries and solve internally, or return public feasible strategies. Neither procedure randomizes.

$$
0
$$

**Conditions.** Set the unused vector to zero in each two-sided call and recover all rows or columns along the shorter dimension. This takes min(m,n) calls. Once the full matrix is known, an exact Nash equilibrium can be computed.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Local argument.** SIX_PROOF_9faa5d48ad36

### B6 - Fixed random hard-matrix distribution and adaptive-transcript lower bound

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** lower

**View.** Randomized accuracy

**Witness or lower-bound scope.** Witness type not certified

**Algorithm-scope qualification.** The authors claim an arbitrary-randomized lower bound but state that its core proof remains to be verified. It is excluded from the certified bracket; a claimed scope is not a verified theorem scope.

$$
\Omega\!\left(\frac{\varepsilon^{-2/3}}{\log^{7/3}(1/\varepsilon)\log\log(1/\varepsilon)}\right)
$$

**Sources.** [5](https://arxiv.org/pdf/2610.02095v2)

**Conditions.** Source Section 8 explicitly leaves verification of the central adaptive proof unresolved. This record reports the source statement without claiming an independent verification of that proof.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [5](https://arxiv.org/pdf/2610.02095v2) Definition3.1; Theorem3.2; Corollary3.3; Lemma3.4; Section8

Randomized two-sided matvec lower statements in ball/simplex and simplex/simplex geometries.

Full-space query vectors, feasible pair output, full saddle gap, fixed cap and success2/3. Dimensions grow with epsilon and are explicit. Paper itself flags adaptive-core proof verification in Section8; theorem statement audit is NOT certification of that proof.

### B7 - Deterministic matrix-vector method of Karmarkar–O’Carroll–Sidford

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized accuracy

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The Karmarkar–O’Carroll–Sidford upper-bound method is deterministic. It also supplies an upper bound when randomization is allowed.

$$
\widetilde{O}(\varepsilon^{-2/3})
$$

**Sources.** [1](https://arxiv.org/pdf/2601.02347v3)

**Conditions.** The deterministic algorithm of Karmarkar et al. gives the upper bound. Hidden logarithms involve $m,n,1/\varepsilon$, so the result is not a pure power law with a constant uniform in every dimension.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** log m; log n; $\log(1/\varepsilon)$

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) Theorems1.1–1.2; Section7.1–7.2

Deterministic matvec upper tilde O(epsilon^(-2/3)) for both normalized game geometries.

Queries in strategy domain form subset of unrestricted real vectors. Same full saddle gap. One pair of directional matvecs is at most constant overhead in our bundled operation. Logs may depend on m,n and epsilon; no arithmetic/runtime optimality.

### B8 - See the cited theorem

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized accuracy

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Recover the hidden matrix with fixed basis queries and solve internally, or return public feasible strategies. Neither procedure randomizes.

$$
\min\{m,n\}
$$

**Sources.** [5](https://arxiv.org/pdf/2610.02095v2)

**Conditions.** Standard-basis left or right products reconstruct every row or column in at most $\min\{m,n\}$ calls. Exact equilibrium computation from the known matrix is free internal computation.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [5](https://arxiv.org/pdf/2610.02095v2) Definition3.1; Theorem3.2; Corollary3.3; Lemma3.4; Section8

Randomized two-sided matvec lower statements in ball/simplex and simplex/simplex geometries.

Full-space query vectors, feasible pair output, full saddle gap, fixed cap and success2/3. Dimensions grow with epsilon and are explicit. Paper itself flags adaptive-core proof verification in Section8; theorem statement audit is NOT certification of that proof.

### B9 - Return any publicly known feasible strategy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized accuracy

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

### B10 - Uniform strategies

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized accuracy

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Public uniform output; no private randomness or matrix information.

$$
0
$$

**Conditions.** m,n>=1, epsilon>0 and epsilon>=2-2/max(m,n).

**Oracle correspondence.** No calls to any Oracle interface.

**Guarantee conversion.** For every fixed matrix the complete saddle gap is at most the tolerance deterministically, hence with probability at least 2/3.

**Output rule.** Uniform vectors lie in Delta_n x Delta_m.

**Resource conversion.** Exactly zero bundled calls, uniformly over instances and random execution paths.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N matvec pair.** 0

**Constants.** None: exact zero cost and explicit threshold.

**Local argument.** CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_zero

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 893efcd3a69a5247155411b3b907adb170663bf4dfb611770dbcc38cf6a4260b

### Native proof: SIX_PROOF_9faa5d48ad36

Native pointer: /proofs/0; canonical SHA-256: ce280494dc1f53bdfbe99859bb04415cada8d549a6affbbee6ff463cc27a3202

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 71b960f326e4ac7b3fc8ebc9c89f266531d6caa43e5e9ed513ae2b23a14256cf

In each bundled two-sided query, set the unused input vector to zero. Standard basis queries recover all columns using the number of minimizing coordinates, or all rows using the number of maximizing coordinates. Choose the smaller direction for exactly $\min\{m,n\}$ calls. The complete payoff matrix is then known, and an exact equilibrium is obtainable by the allowed uncharged internal optimization. The saddle gap is zero. Transposing the matrix to the canonical row-maximizer convention only swaps the response blocks and does not change the call count.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 07e8ebffa4e51801b70a23c040d03ce5a82521c9ca19b75898eb8c5374c948ba

Recover the matrix with basis queries, then solve the known linear program using uncharged internal computation.

### Native proof: SIX_PROOF_c88bf8d96092

Native pointer: /proofs/1; canonical SHA-256: e1615d8c95b04b61caeb5ae844662f25098ce45196f02e2e50b73b4cfa8e5ec4

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 01e13c1e771cf618c03c37b296b033bc74167499325485f7cd93d874363b46c7

Under the declared matrix normalization and strategy domains, every feasible bilinear payoff lies in $[-1,1]$. The difference between its maximum against a fixed minimizing strategy and its minimum against a fixed maximizing strategy is therefore at most two. Return any publicly specified feasible strategy pair without querying. It meets every tolerance $\varepsilon\ge2$ deterministically. Nonnegativity of query cost certifies exact zero cost.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 6e1e3d55b0a5aab01289824739d2038cd227ae659f7fd031802f0e2d13b840ba

Return any public feasible strategy

### Native proof: CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_zero

Native pointer: /proofs/2; canonical SHA-256: ed8c3965d76a330c93ce66c67f0f5048f58201c3936f06df6783944c44ef5e92

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: e09bf9653307861d97604da640f27e1d4619f8e0d3b7f7a2619c464820b0e1d2

Return x=(1/n,...,1/n) and y=(1/m,...,1/m) without information calls. For any row i and column j, (Ax)_i-(A^T y)_j = sum_{k!=j} A_{ik}/n - sum_{l!=i} A_{lj}/m + (1/n-1/m)A_{ij}. The entry bound gives an upper bound (n-1)/n+(m-1)/m+|1/n-1/m| = 2-2/max(m,n). The full saddle gap is the maximum of these differences over i,j, so the same bound holds for every fixed admissible matrix. The output is feasible and deterministic, hence meets instancewise success probability at least 2/3 whenever epsilon>=2-2/max(m,n). It uses zero calls on every path. Nonnegativity of call cost implies N^*(epsilon;m,n)=0 there. The non-strict inequalities include equality. If m=n=1 the threshold and gap are zero, so every allowed epsilon>0 qualifies. This proves a sufficient zero-cost region, not necessity of the threshold for randomized zero-query methods. All constants and inequalities are exact and uniform in m,n,epsilon.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 9725e5d4e1b7af1fff10ba2c363a6d7975461e6411bcfa8390b7f11c46870ef0

The randomized_accuracy view, guarantee g1, target-accuracy quantity q2 and bundled exact two-sided call resource; m,n positive integers and epsilon>0.

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 17a94e9ed3c8e1819dd2488afb92978124aa8717c0ccb531af39bcfe0eb37094

Dimension-dependent zero-query saddle-gap guarantee

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 8ce42cc6fd5a8be197c4b7a0d6bf6dd85a165410349ef11f72f8d866fe34d185

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: cab29ce52cf34a63a032dffc853dd4960df1ef1cb07f169900eb3e6d78b50561

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 85c106364d02fef2743f1b3640b43349bcf684aa323df7254987ad621d27f31e

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: a5adb2a038594c4b733107458992b8a53d185f85e24c217e9e451edf2ff3d05b

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 173fff601ce1234f7c4eb2eb4408138ad197f177878c516eca23e962d9968cc3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 770ee0bb0c5cb65387de25822997990f2486c6e047db875bcd63a2f005f8af70

Own native comparison predicate

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 01d465a421d168e38d75220694c187b6accb7bc75433156fcbd2beca84baf9f2

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 9f4a44a5f2738fe4eb8418fed140f42f1f40e80ce832e6a6d0e66636df12dbcd

Conditionally retain this exact native bracket; no fresh theorem certification.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 205abbdf84a81bf357bf58671791f2eb3d18ba3f35b3e26d35dd20efdc34233b

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r1

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 3a048629ac356ac5704e875c6de4c6731ca5043d9be08cfd386b9b0b0522beb5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 770ee0bb0c5cb65387de25822997990f2486c6e047db875bcd63a2f005f8af70

Own native comparison predicate

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: bef61c893b62a9b6ef2ebe6d035397360122acd8b22aa112f181ed518cffd6e0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 9f4a44a5f2738fe4eb8418fed140f42f1f40e80ce832e6a6d0e66636df12dbcd

Conditionally retain this exact native bracket; no fresh theorem certification.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 205abbdf84a81bf357bf58671791f2eb3d18ba3f35b3e26d35dd20efdc34233b

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r1

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: e41d4e8d4fc83b36fed121027330658a87c23dd7c676ad353059959f69da3b53

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 65ab802771376684e423cc910702b160a81641c40fec2789935eec0f098d5e98

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: e3db67692bcffe55218a65c50e3686a0f7a7940960adfc734ffd88bf8b695e9a

unresolved

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 181e27559be1123d1e1955c94f021273b863bcb2da5d45f438b535907c7c4155

Different native resource selection; no new transfer or global log-dependent dominance is proved. Keep its separate comparison; consolidation remains unassessed.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: e77fcf7112b598213194dec90d9cb98599643ec5cf3fbdbaaf7c5a582eb59d41

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r2

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: cffda871a85971fb4f81412084964aa5fc08de3137469d69bfb9c18c89e758e8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: 73359df32b2c1fc28e3fcf50a03a7e3ec4458f8f2d0ec9b0032ae2bee3d4bb4d

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: e3db67692bcffe55218a65c50e3686a0f7a7940960adfc734ffd88bf8b695e9a

unresolved

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 181e27559be1123d1e1955c94f021273b863bcb2da5d45f438b535907c7c4155

Different native resource selection; no new transfer or global log-dependent dominance is proved. Keep its separate comparison; consolidation remains unassessed.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: e77fcf7112b598213194dec90d9cb98599643ec5cf3fbdbaaf7c5a582eb59d41

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r2

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: e8d7484ef1aa96969ba823801ae3525a5e818ef634f56b0f72a4e0e70048f4ab

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: fa5bfcbde9ab5c79976bb3f6512ec65b9495ff4e41711740b2d73b3dbed566b0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: 4cf770cda55b2c90cd6b337d1085d6da4aa24fe1eae5fa8b79a81d9b178b003a

The large-dimension source window is outside complete-matrix recovery for sufficiently large source constants.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: 7db8134afb9821691689faabd5eff889a10b48db2cf98f0cb085f5f6582a058e

N>=min(m,n)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 9630443ca1e6bfef0143dc2f103373c7d6b7925dc995cdf2576067c83c1ab891

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 16b732f6ce862744d260c5cfb4af6ac36b3c111d7c5872229fcbc507d7cd2dd2

The source's strict dimension thresholds are sufficient applicability restrictions, not proved intrinsic transitions.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 029220be62bd10e20fe9daf7f5d6cec1b084d4d207f4a15aff42f5c74fda3634

Universal constants of r1 and r2 are not identified; no fixed-dimensional N->infinity conclusion.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 0e0e6c7d3d7bb83c1905bdb396d7c23c51401a757086f56f3cfe2ecd71d8f04f

Cross-projection candidates and explicit native dispatch are recorded but not newly merged.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: e92767b2468d893d3d5d64bdae8f0c138ac1395dfefe12710af1a68bec41e9ac

$O\!\left(N^{3/2}\log(m)\sqrt{\log(n)\log(n+1)\log(m+1)}\right)$ (retained native comparison, not a claim of the consolidated strongest envelope)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: f7455e5231687be31c0fee5c35d6d5db7094440f153944842981e6f82879f958

\Omega(1/(\log(m)\sqrt{\log(n)}\,N^{5/2}))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: dd2b16ec8b565a6d390c9a334f9c3a14737fdab0e7241bb5ebbe97fffde4296c

The native displayed bracket is retained. Consolidation across resource-projection IDs and uniform dominance of all logarithmic terms are pending; the published gap label is not a global optimality claim.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 1027dcd5463e911d47bf0b1b113856c38bac80f1c1111305f3283a2748e4fc4e

O(\sqrt{\log(n+1)\log(m+1)}/N)

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: d32b6f37b7fde6bb1146594fe7418b8115e500f7322a3b11868afe4110a3f7c6

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 4288504088fa193e1b8828afd8479c05ff4a78c83218bb2baba794ebb4229014

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 216e450ecc05eadef7580a015fc340adc0449f19ba0f1244157d3012acb0d65b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: a205dd0a31d7a1a4f42ceb2b4ac29e2dedd33b19e852d401e2e85c0f7ba9fb1f

r2 intersect r1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 01d465a421d168e38d75220694c187b6accb7bc75433156fcbd2beca84baf9f2

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 459645bfe01049a382fb656251149a32b308f85096d8b6e6790c511994b95f45

The frozen c2 native dispatch already permits this algorithm on r1 and takes the minimum of applicable branches. Retain that exact guarded dispatch; no new cross-resource transfer is asserted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 205abbdf84a81bf357bf58671791f2eb3d18ba3f35b3e26d35dd20efdc34233b

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r1

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 629bbb937c1c1e2b917e433ebd4c3b0d6a12c8cdaeb7f1e43bc01868968cc4bc

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: bef61c893b62a9b6ef2ebe6d035397360122acd8b22aa112f181ed518cffd6e0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: e3db67692bcffe55218a65c50e3686a0f7a7940960adfc734ffd88bf8b695e9a

unresolved

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 181e27559be1123d1e1955c94f021273b863bcb2da5d45f438b535907c7c4155

Different native resource selection; no new transfer or global log-dependent dominance is proved. Keep its separate comparison; consolidation remains unassessed.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 205abbdf84a81bf357bf58671791f2eb3d18ba3f35b3e26d35dd20efdc34233b

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r1

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: e1d9b815a60c44356ffa619524aa4bccc836fb8a2152b43d6c6376a7c8ec4b88

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 770ee0bb0c5cb65387de25822997990f2486c6e047db875bcd63a2f005f8af70

Own native comparison predicate

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 65ab802771376684e423cc910702b160a81641c40fec2789935eec0f098d5e98

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 9f4a44a5f2738fe4eb8418fed140f42f1f40e80ce832e6a6d0e66636df12dbcd

Conditionally retain this exact native bracket; no fresh theorem certification.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: e77fcf7112b598213194dec90d9cb98599643ec5cf3fbdbaaf7c5a582eb59d41

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r2

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: 3d5f597bb9d15852c86377cb4e92c0d4cf4979bb118273087b4c24114f4d6d76

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 770ee0bb0c5cb65387de25822997990f2486c6e047db875bcd63a2f005f8af70

Own native comparison predicate

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: 73359df32b2c1fc28e3fcf50a03a7e3ec4458f8f2d0ec9b0032ae2bee3d4bb4d

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 9f4a44a5f2738fe4eb8418fed140f42f1f40e80ce832e6a6d0e66636df12dbcd

Conditionally retain this exact native bracket; no fresh theorem certification.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: e77fcf7112b598213194dec90d9cb98599643ec5cf3fbdbaaf7c5a582eb59d41

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r2

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: e8d7484ef1aa96969ba823801ae3525a5e818ef634f56b0f72a4e0e70048f4ab

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: fa5bfcbde9ab5c79976bb3f6512ec65b9495ff4e41711740b2d73b3dbed566b0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 4cf770cda55b2c90cd6b337d1085d6da4aa24fe1eae5fa8b79a81d9b178b003a

The large-dimension source window is outside complete-matrix recovery for sufficiently large source constants.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: 7db8134afb9821691689faabd5eff889a10b48db2cf98f0cb085f5f6582a058e

N>=min(m,n)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 2c0a94fa41b25e8fd81b616666a84a31a5867744410b6a3188ed2672a2ebe17e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 16b732f6ce862744d260c5cfb4af6ac36b3c111d7c5872229fcbc507d7cd2dd2

The source's strict dimension thresholds are sufficient applicability restrictions, not proved intrinsic transitions.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 029220be62bd10e20fe9daf7f5d6cec1b084d4d207f4a15aff42f5c74fda3634

Universal constants of r1 and r2 are not identified; no fixed-dimensional N->infinity conclusion.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 3177fe0ad9c04f8da04e7618970d78ccd8acc0a21aa43d3e3bae812f26cbe8a9

Retain the explicit b1 dispatch only on r1. Other cross-projection consolidation remains pending; do not replace guarded minima by an unproved globally dominant term.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 16d8b3fb551b1c3509d7d73f44ccbc286b6644bcb8c73e25faf8d525151f6174

The displayed native polylog(m,n,N) upper/lower ratio remains an upper estimate; with the existing dispatch the actual guarded ratio is min{U4,U1 when r1}/L3. Numerical crossovers are not established.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: c94b8de627d68fd5f34316b9da297b61757712c63d7f49b3eb2d9c91295d000f

\Omega\!\left(\frac{1}{N[\sqrt{N\log(nm)}+\log(nm)]}\right)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: dd2b16ec8b565a6d390c9a334f9c3a14737fdab0e7241bb5ebbe97fffde4296c

The native displayed bracket is retained. Consolidation across resource-projection IDs and uniform dominance of all logarithmic terms are pending; the published gap label is not a global optimality claim.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: b20114f80a8b9d78a6a9875a669b45d861fa19c61b985b2e2eb74fda56fe11b9

min{retained tilde O(N^(-3/2)) on r2, retained O(sqrt(log(n+1)log(m+1))/N) on r2 intersect r1}, exactly following frozen c2 dispatch; retain hidden logs and the recorded gap cap.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 0e40c0ca6784ab02118d14de3bb789f2abc74d6fff2594c9428c27969071283e

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 6c62d5afb2c1cb47d6c6fb03d6594caf667f2d80ffb377809937ba39091715f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 6105190ede488b3c48a2fb5f6275bc23a8651d5e392f1d70e17e051e6f56fff9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 01d465a421d168e38d75220694c187b6accb7bc75433156fcbd2beca84baf9f2

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 922ecd00de52e2b8249cfa4a6582d6190c79bef99263db30f13bb018b16feba9

Its recorded large-dimension window excludes saturation. No cross-projection transfer is proposed.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 205abbdf84a81bf357bf58671791f2eb3d18ba3f35b3e26d35dd20efdc34233b

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r1

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 7f48d5551d6ee0d38af6bceb2d6cb8e0f7cca5cba2edddae4de9be04e210378c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: bef61c893b62a9b6ef2ebe6d035397360122acd8b22aa112f181ed518cffd6e0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 922ecd00de52e2b8249cfa4a6582d6190c79bef99263db30f13bb018b16feba9

Its recorded large-dimension window excludes saturation. No cross-projection transfer is proposed.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 205abbdf84a81bf357bf58671791f2eb3d18ba3f35b3e26d35dd20efdc34233b

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r1

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: 394341203e1e89468dd776462a34c3164157dffce589e952f0631c9be276962c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: 65ab802771376684e423cc910702b160a81641c40fec2789935eec0f098d5e98

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 922ecd00de52e2b8249cfa4a6582d6190c79bef99263db30f13bb018b16feba9

Its recorded large-dimension window excludes saturation. No cross-projection transfer is proposed.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: e77fcf7112b598213194dec90d9cb98599643ec5cf3fbdbaaf7c5a582eb59d41

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r2

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: 4c914e55bb568963f15270b137bc611161a2627cee715160f7ef008d532a3721

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: 73359df32b2c1fc28e3fcf50a03a7e3ec4458f8f2d0ec9b0032ae2bee3d4bb4d

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 922ecd00de52e2b8249cfa4a6582d6190c79bef99263db30f13bb018b16feba9

Its recorded large-dimension window excludes saturation. No cross-projection transfer is proposed.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: e77fcf7112b598213194dec90d9cb98599643ec5cf3fbdbaaf7c5a582eb59d41

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r2

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: 471c661008f21f3adc25133178472323f2144abf75ef5da82ce21576fb4daffa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 770ee0bb0c5cb65387de25822997990f2486c6e047db875bcd63a2f005f8af70

Own native comparison predicate

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: fa5bfcbde9ab5c79976bb3f6512ec65b9495ff4e41711740b2d73b3dbed566b0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 9f4a44a5f2738fe4eb8418fed140f42f1f40e80ce832e6a6d0e66636df12dbcd

Conditionally retain this exact native bracket; no fresh theorem certification.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 32282a9fcef8118766412fa1119aaf2dfc9f0fb85ab8de285ecbd13944fc8b98

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__r3

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: b9989b1e5bf975fc9ee8678fa62f3383bfd669944a7edb6ffbaace5202b553e2

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: c216ab27a7991f45f0247f9413c409aac81b70571541c3c32f9e3584a849c1eb

Equality N=min(m,n) is included by the frozen recovery proof; no arithmetic-cost claim.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: 07393b12c90c47d1bbe8835252b48567b3d445e47e95439837684322ba23acb9

Exact risk 0; ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 7d11f065cf16302d41587e23179fb67e29ff621f9891eb594f358b357feae439

None on this exact saturation region.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 8f44604bfeb02e4fdf668cc299dd1e3943d48843a2c4935ddbc7ec122d805b3a

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 336840cd40e3331b172dd0e01894af36f1d38dc5e70e49fc51f1f18d2d505cf1

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: 1582896d7c2e48703044db25858b202f77276a790982a3eadd5321d51a99570f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 7cc57c9ce756d8d12a89c2bf4e04138f37a7a6fc7eec3972a6ec90babebcbb04

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: e3db67692bcffe55218a65c50e3686a0f7a7940960adfc734ffd88bf8b695e9a

unresolved

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 8750f3964977cd3dc2b83c98dcc94d480e67c8b98613b40e1b943e7b1838e6c7

Frozen candidate is explicitly ineligible: the source's adaptive-core argument remains unverified. It stays outside all active native reference fields.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 77c12b7fedff5579e9061a0738090a997621a2300e14b2e9b653f3d475f65743

the unchanged randomized_accuracy r1 predicate: 0<epsilon<=epsilon_0, source-selected positive integer q asymp epsilon^(-2/3)/log^(1/3)(1/epsilon), m,n>=4q

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 09174c42447777b31bbecd7ac68e5506027b107360b58da085e9ae86fa8d77b2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: 3da97cb33716fc7848cf9fab668c764098286bd9570105979eef102ce52d880b

the unchanged randomized_accuracy r1 predicate: 0<epsilon<=epsilon_0, source-selected positive integer q asymp epsilon^(-2/3)/log^(1/3)(1/epsilon), m,n>=4q AND epsilon<2-2/max(m,n)

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 0224e431fa3bf7cd690f5dc00f4ee780b807c10124c62e0c1b04f1776ae7e683

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: 59309aa02da033bbaeab836c090d145c1000e8e4f5929154401d58deed2eb781

Existing deterministic upper bound is retained outside the zero-cost branch; all hidden dimension and precision logarithms remain.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 4d270b7fe1849297317284ba09b98110afab6be82d3b071a57122f1c88a0190d

r3: m,n>=1 and 0<epsilon<2

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 12aaccf62cf2e2c9fdaa50cf924c2b49df9887e34f009454a32b9e9928792b0a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: 0b26e5a1e918922c6f8a62347f2b5b32e5e2ceb775f0a4093fedc9d16f31a792

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 1f73537e9417f113d9fa4fc07f8e8a0cf5d6a3eef2f64d8db562e3552b749124

This bound belongs to source-scoped quantity q1 and unassessed resource_cc7c360256, whereas this comparison uses q2/resource_fbe102dfeb. No transfer or quantity merger is adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 5ba0e15405f6f80410f2fc0f3c28cba2940c91895e4eed5117c4fdec1f722905

r4: m,n>=1 and epsilon>0

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 3fef88c8a5270519d66757d20cb11a39f7b1a701c4be1da1bd3d3f65cdd0c1d7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: 01ef8c82e9d9d74a051196b44c17098dff68f22b1de8b0153e3183a6b0726716

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: 7dd597c4f3239b1f99b2eb719318530fcf459228e09aaa39bea45d3eaffa17d1

On its epsilon>=2 guard the original zero-call witness has the same exact value as the new included witness. It remains active in its original c2 comparison; no duplicate active reference is added here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 08e94af1390544908f624d2bbff1181e5d1478a97074ea3a2a4f52f1092c6295

epsilon>=2

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: 813b3d558a7dcc0e24c02ffef27acaf77bbf9ed9553b84e8f26b61edb6fcbd70

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: e8b440a26e8846fef111f569072949f53620c13fd2a76dfc874cb018680233a9

the unchanged randomized_accuracy r1 predicate: 0<epsilon<=epsilon_0, source-selected positive integer q asymp epsilon^(-2/3)/log^(1/3)(1/epsilon), m,n>=4q AND epsilon>=2-2/max(m,n)

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: a94c57c4f61e7d0b7c343022890872a95f17357aa69e41da78c616356fcdf384

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: 7619ce2ed3b41c7b79e0522b0c7b4d9db3cdb549bc4dcfae2d76aacd00f687ee

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 808239454aaa76794fce024284a6de4efadb7f62dcce69715804d725f725b074

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_zero

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: b9c7597e779db1eda1b8efc78da614b029214e9fd466c24e75a4d985e837b53b

Uniform-output proof gives exact zero cost after intersecting the unchanged r1 predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: b44475ee03040b6379fb25c3a3c5159567ca162c48880b7569a2aeee6fcedcff

m,n>=1, epsilon>0, epsilon>=2-2/max(m,n) in randomized_accuracy

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: 113f72650d273ae88d1f3af01b08f6f9338265569115eeba1a734393de2ce303

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: fdbbce1def72c078c6695fd592f297ea33fc345f7a1f9a215eacd7dcd468c8b5

Do not assume a numerical epsilon_0 or identify it with 2; intersect guards literally.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: 9c71aa93e13fce3b9f99ee0e44bd6568f423a4162d22a8c183feb2e96c850894

If r1 meets the new endpoint, the native comparison now displays the zero branch; no presumed empty intersection is used.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: d8fb429828ae7f86ace488442179fb31312757928cfacb314ea4333a511cf81a

Exact 0 on the new branch, ratio inapplicable; outside it the positive lower side remains missing.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 92b0770f63294d9d71af3db4656522e3cf0a494bee01ae6d8ee50ac9dd941a07

0 by nonnegative query cost; on the zero-upper subregion this certifies exact equality. No certified positive rate elsewhere.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 106c73895642ba47cff0f7b3009062a76fecdc9d75a633a1fcba4dcee064f5e4

The claimed randomized lower bound remains ineligible. No positive-rate bracket closure is asserted.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: 2814d016b2aec402edb03a5e6ed6a020bc323222d962f6790cf23c1ab2685757

0 on r1 intersect {epsilon>=2-2/max(m,n)}; otherwise retained tilde O(epsilon^(-2/3)), including all hidden dimension and precision factors.

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: 829d64048e5f1a0ec725af147b558b31df2e8da76fff2c683ea503d29fd66fb9

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: 6623219252e668f06f78e86fbe3813c3fdef1a825167dc4e7f5bf6c5b51f34a7

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: cdc6d219f2b1e074cb41d15b275a3c268b435d3efd8a642cbe242437d124438c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: 7cc57c9ce756d8d12a89c2bf4e04138f37a7a6fc7eec3972a6ec90babebcbb04

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 6835183ab710529371e83b085df4eded3b1fcc38fbbeb2d00877f3d3663c843f

Its claimed small-accuracy lower statement is ineligible and does not enter this zero-cost bracket.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 77c12b7fedff5579e9061a0738090a997621a2300e14b2e9b653f3d475f65743

the unchanged randomized_accuracy r1 predicate: 0<epsilon<=epsilon_0, source-selected positive integer q asymp epsilon^(-2/3)/log^(1/3)(1/epsilon), m,n>=4q

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: ae034cae16a8f719d2246d35c734bb9cc6d103348c493012c15660b427e7ff48

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: 0224e431fa3bf7cd690f5dc00f4ee780b807c10124c62e0c1b04f1776ae7e683

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: 1cc453ad121bbd023e59eb33102a9e948280da77acc149d256430d903b236b65

Its strict accuracy guard excludes epsilon>=2.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: a5754f6884bd3e2741fc279948a55dce3c76cd882eb4eadde0d24a6c587cce1e

0<epsilon<2

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: c7eddbbb75d74138d585f2d0c2e1d37e8d5be94498b8d4c2c00c79d48dfa971b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: 0b26e5a1e918922c6f8a62347f2b5b32e5e2ceb775f0a4093fedc9d16f31a792

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: 0db69b4cf067454a025be8cdceb42a7002a4d8d63186ce6ecadfed8146d4a556

Different q1/resource identity; no transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: 4338a108861b4544d1ccc477071741bd19304eacf93538ef4388dfc5a4c1f4e7

all positive epsilon

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/bound_uses/3; canonical SHA-256: c74842afd03a71fef5b605843278ad5e6c43182af75640a348ad30cd1b6a9d6d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/adopted_region; canonical SHA-256: 08e94af1390544908f624d2bbff1181e5d1478a97074ea3a2a4f52f1092c6295

epsilon>=2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/bound_id; canonical SHA-256: 01ef8c82e9d9d74a051196b44c17098dff68f22b1de8b0153e3183a6b0726716

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/reason; canonical SHA-256: c2fe2bdf425c52dc75fafd9bab95bc1a11a9d82cafb513902c5cf7f179fc8f5b

Retain the original exact-zero witness and nonnegativity certificate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/validity_region; canonical SHA-256: 08e94af1390544908f624d2bbff1181e5d1478a97074ea3a2a4f52f1092c6295

epsilon>=2

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/bound_uses/4; canonical SHA-256: 1e9d2622541ff3da67fd339d07b6adcef5165e2509893411c1bbf2c13c83470c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/bound_id; canonical SHA-256: a94c57c4f61e7d0b7c343022890872a95f17357aa69e41da78c616356fcdf384

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs; canonical SHA-256: 7619ce2ed3b41c7b79e0522b0c7b4d9db3cdb549bc4dcfae2d76aacd00f687ee

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 808239454aaa76794fce024284a6de4efadb7f62dcce69715804d725f725b074

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_zero

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/reason; canonical SHA-256: 915decc532b3f4fd5749ec3ea91268bdec418125c19ea928cbc64394cf151a21

On this comparison the old witness already attains exact zero; the new witness has equal cost, so no improvement here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/validity_region; canonical SHA-256: b44475ee03040b6379fb25c3a3c5159567ca162c48880b7569a2aeee6fcedcff

m,n>=1, epsilon>0, epsilon>=2-2/max(m,n) in randomized_accuracy

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: b678b6f8dbec025ae052e60160f1a8b6e32fcf8005190d563467ddffd9121028

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: 0806f40b406c2d71913f1f73f443efa2a2d35c317f99a6ce4f05d063b43c2f85

The old closed epsilon=2 endpoint is unchanged.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: 304e3d533281f4a0483e7b47d21e96f580ed4475bb9f3bb1599e2f7bdc5bf120

Exact 0; ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: a34f659dbdd79283ff9b55186fea59fecba2284e474fe3ee149631af83624d3d

None in this region.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: 0891224c2b72fabbdb055b38a1bd3e1f3f06029f6ca92baf6a7e2e100c5cbd02

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: 0b34382aa9d755b21d44765e11b0b23a16474b91c3b515ef760943ce94942c4a

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: 7e5b00f95620b231ca4a3ec65e73bad6da9e8abdf7a2e781753c34e09c6d9626

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: 7cc57c9ce756d8d12a89c2bf4e04138f37a7a6fc7eec3972a6ec90babebcbb04

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: 510bb97efbc5e66da1d49955b017ef122ed1e8cd21e3d4ac850c64f05d9137af

Different target-accuracy quantity q2; excluded lower claim is not transferred.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: 77c12b7fedff5579e9061a0738090a997621a2300e14b2e9b653f3d475f65743

the unchanged randomized_accuracy r1 predicate: 0<epsilon<=epsilon_0, source-selected positive integer q asymp epsilon^(-2/3)/log^(1/3)(1/epsilon), m,n>=4q

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: 1aed6b73399eca61a8bf4bf69bcefb2712b39231e5875b67b490cc8101c5f7a1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: 0224e431fa3bf7cd690f5dc00f4ee780b807c10124c62e0c1b04f1776ae7e683

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: bf51ca48a364bc7ae679321c799c4bbbdf71c105b94587fd2ef6017e5572279a

Different q2 and scalar resource projection; no transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: a7fdc4e6e62bd8f54a36b6a09e6d49ad2f83090e8524364984ff597db557e5fa

r3

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: a5844ecbe2ca7a47882fcf508b4adc6b86bf5d11ea389c111ccb8eb41ec7167c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: 4e3b5454cf93e32fad90650d43c8d7596ecb6593117b88a667c81644fa84f11d

r4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: 0b26e5a1e918922c6f8a62347f2b5b32e5e2ceb775f0a4093fedc9d16f31a792

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: cc6a593676133a66ecf5f3cf44bc02ac2e60650cb23cd73ed8f635dde4248e90

Retain the native source-scoped reconstruction guarantee; do not convert it automatically into a q2 minimax bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: 954de8fe0e9109dd64b885d6c517199614af329bd1eea1c6c9e5bbbf64a0ffed

r4: m,n>=1, epsilon>0

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/bound_uses/3; canonical SHA-256: 35c14b6a702180b045a174744b80c8f852c9cb9346abffa117de72e98b2d2c4a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/bound_id; canonical SHA-256: 01ef8c82e9d9d74a051196b44c17098dff68f22b1de8b0153e3183a6b0726716

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/reason; canonical SHA-256: ceb44c63d56f1800c3aaf8a93c1da7140f9f34a3a3654aec8237f0b526a2fd04

Different q2/resource identity.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/validity_region; canonical SHA-256: 08e94af1390544908f624d2bbff1181e5d1478a97074ea3a2a4f52f1092c6295

epsilon>=2

#### Native item 5

Native pointer: /joint_analysis/comparisons/5/bound_uses/4; canonical SHA-256: 834f57e07354bd7be977523b539329c2f8b6a92df441ac579635b2d8c97728a4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/bound_id; canonical SHA-256: a94c57c4f61e7d0b7c343022890872a95f17357aa69e41da78c616356fcdf384

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/reason; canonical SHA-256: dac97a63de669aadc7439601659510867febf9aa1394edf5e362bb4b1ec06f2a

New zero-cost statement is for q2/resource_fbe102dfeb; this q1/resource_cc7c360256 statement is preserved.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/validity_region; canonical SHA-256: b44475ee03040b6379fb25c3a3c5159567ca162c48880b7569a2aeee6fcedcff

m,n>=1, epsilon>0, epsilon>=2-2/max(m,n) in randomized_accuracy

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: 6d431c0dd27d2f95e8bcaf4c421a1662afba2c9a80c901228db1aba3ebf01604

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: 57108cc053bd1836092786a9b1ab7aa66f86203a19887d07a0c88f1256674a2a

min(m,n)=1 permits reconstruction with one call; this does not rule out zero calls for easier tolerances.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/boundary_checks/1; canonical SHA-256: af41ef0a56cbaace5a0b3a060c8ad6e6345ddd8edf07f447a83b5751a75efc9c

Exact internal solution after recovery is uncharged.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: bf8f51e4806249e98f156ee80f6c76a871a7e484534a21b4d3c91ad41570b4f9

Unassessed scalar minimax gap; do not infer a ratio.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: e67d491b35719019a62201740f1998f41b2b2f18fe34d722e3ffef3c05fea445

No registered compatible lower statement.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: c6dd3236f64b313f0ac26dcbbe53148dae7281cd6d8fc1bacfeabe57f293908d

An explicit reviewed transfer to q2 would be required before combining this record with q2 bounds.

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: ed41b997c9da2a84744fcdf3ca28d12a9ca5b2f12bdd4244ef98082b1a1c9800

Native source-scoped statement: at most min(m,n) calls; its resource projection remains unassessed.

#### Native item 7

Native pointer: /joint_analysis/comparisons/6; canonical SHA-256: a26aa76a3e11c58bf1276111948d2b6fe9b26e0f80fb1a67c439b2b4e5a23912

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/6/bound_uses; canonical SHA-256: 06ea1ac87a62066c4aae3a68b8791e3fe5df7fffd77558c8a7a87f142785c0f6

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0; canonical SHA-256: 7cc50373451c94bdad0f16a6c5513af4ca1c33360c5d1a6e75a0d8a76fbe7aa3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/bound_id; canonical SHA-256: 7cc57c9ce756d8d12a89c2bf4e04138f37a7a6fc7eec3972a6ec90babebcbb04

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/disposition; canonical SHA-256: e3db67692bcffe55218a65c50e3686a0f7a7940960adfc734ffd88bf8b695e9a

unresolved

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/reason; canonical SHA-256: babc10e7dd924f63bbc29d33a0734043c135843116f8a4b2a4c654185b37c8e1

The frozen randomized lower claim remains ineligible; a possible guarded intersection supplies no adopted lower theorem.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/validity_region; canonical SHA-256: 77c12b7fedff5579e9061a0738090a997621a2300e14b2e9b653f3d475f65743

the unchanged randomized_accuracy r1 predicate: 0<epsilon<=epsilon_0, source-selected positive integer q asymp epsilon^(-2/3)/log^(1/3)(1/epsilon), m,n>=4q

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/1; canonical SHA-256: 93506b9597c7baad3e2a189f7adb45eae28448e02a04dbc473817d4de328afa8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/bound_id; canonical SHA-256: 0224e431fa3bf7cd690f5dc00f4ee780b807c10124c62e0c1b04f1776ae7e683

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/reason; canonical SHA-256: ae2ff8ab118c26cd170badeaf1e6e8031317d9b900d0b4adf7ca389cde554b49

On its intersection with this endpoint, the positive upper estimate is weaker than exact zero.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/validity_region; canonical SHA-256: 8394fdc0369980d9b502a1de3bac503a70386088cb5bf7d12d2169cec39441d2

r3: 0<epsilon<2

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/bound_uses/2; canonical SHA-256: 8af7f6e9b1c77db15a8db059d9a3716a50df2f058a21326f3724f1cbfc598830

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/bound_id; canonical SHA-256: 0b26e5a1e918922c6f8a62347f2b5b32e5e2ceb775f0a4093fedc9d16f31a792

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/reason; canonical SHA-256: bd23781ddba88c45caf63abf9e0b457c7d6f9f1367953a1d96bc9782c03a6420

Different quantity/resource IDs; no implicit transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/validity_region; canonical SHA-256: 4e3b5454cf93e32fad90650d43c8d7596ecb6593117b88a667c81644fa84f11d

r4

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/bound_uses/3; canonical SHA-256: 3fef88c8a5270519d66757d20cb11a39f7b1a701c4be1da1bd3d3f65cdd0c1d7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/bound_id; canonical SHA-256: 01ef8c82e9d9d74a051196b44c17098dff68f22b1de8b0153e3183a6b0726716

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/reason; canonical SHA-256: 7dd597c4f3239b1f99b2eb719318530fcf459228e09aaa39bea45d3eaffa17d1

On its epsilon>=2 guard the original zero-call witness has the same exact value as the new included witness. It remains active in its original c2 comparison; no duplicate active reference is added here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/validity_region; canonical SHA-256: 08e94af1390544908f624d2bbff1181e5d1478a97074ea3a2a4f52f1092c6295

epsilon>=2

#### Native item 5

Native pointer: /joint_analysis/comparisons/6/bound_uses/4; canonical SHA-256: 3a3ffe66499009a0378e7cbe230b57eaae07c07a9d9f43cf48da6ceaad5a23e8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/adopted_region; canonical SHA-256: b44475ee03040b6379fb25c3a3c5159567ca162c48880b7569a2aeee6fcedcff

m,n>=1, epsilon>0, epsilon>=2-2/max(m,n) in randomized_accuracy

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/bound_id; canonical SHA-256: a94c57c4f61e7d0b7c343022890872a95f17357aa69e41da78c616356fcdf384

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/mapping_proof_refs; canonical SHA-256: 7619ce2ed3b41c7b79e0522b0c7b4d9db3cdb549bc4dcfae2d76aacd00f687ee

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 808239454aaa76794fce024284a6de4efadb7f62dcce69715804d725f725b074

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_zero

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/reason; canonical SHA-256: 7207380380c2c733ad828862698b52377c7368130ea094b75a654eddf28b29c8

Public uniform strategies certify zero calls; nonnegativity certifies exact optimal cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/validity_region; canonical SHA-256: b44475ee03040b6379fb25c3a3c5159567ca162c48880b7569a2aeee6fcedcff

m,n>=1, epsilon>0, epsilon>=2-2/max(m,n) in randomized_accuracy

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/6/boundary_checks; canonical SHA-256: 111116087d0ebe1968af6ee25f15b471a2c51b8c4861f8279fca3621907b1338

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/boundary_checks/0; canonical SHA-256: 0220caed0b2d0b9efc029de134e3623bba93f5ed7ebcd50d44d7735514bbb552

epsilon=2-2/max(m,n) is included whenever positive.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/boundary_checks/1; canonical SHA-256: 556878fad62bbc176872c2001f78c9c418f71fa906810859a8cb36690a10b0f6

For m=n=1 the threshold is 0; only the original positive-epsilon domain is included.

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/boundary_checks/2; canonical SHA-256: 524ffa8ca23736d6037eaa8a98546cc8f6dfc7affbb5fff356a5f53d3790d81a

For m=n=2, epsilon=1 is a concrete newly recorded zero-query endpoint.

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/boundary_checks/3; canonical SHA-256: 806ac26fe6f5c228ec16d18de10c709e28ba7f5096d2ba546e38aed955c2f7f7

No assertion of necessity of this threshold for randomized zero-query algorithms.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/6/comparison_id; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/6/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/6/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/6/gap; canonical SHA-256: 304e3d533281f4a0483e7b47d21e96f580ed4475bb9f3bb1599e2f7bdc5bf120

Exact 0; ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/6/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/6/remaining_gap; canonical SHA-256: 3f43ffd3db9f1cee06603cb992cc882320eaf2023de373791f5dac8f12457621

None on the proved sufficient zero-cost region; behavior below its threshold remains separately unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/6/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/6/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/6/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: ee24e5b86f69e9e3609d14363026f9377c40292c16913981bf7b2e5d9489edfd

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: ed49292f5064067f3988f8a062452fe5a071b82093aa01a9d0dd4d38385ed044

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: bb31697710cb5aa2ebf669a4e1c12df0d1c511085bcee8eeb99e030ac714daaa

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 898e37b5c7afcf089244cf8c6315917f793870e30305d680d4fece74aef26e3b

det_recovery

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 1fb32358efaa6c815f8c7603d80d3f1b822a05074310f70fe09482f7c1d72261

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: 7d8d66f0e43855127cf8f207989f0ee8fbc69792c68068df172d4fe428bb3016

SIX_PROOF_9faa5d48ad36

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 45b99c8f3b75fd37ce9c74fa7ae92d81dbc055c826e06e036b94bd76dd26e7c8

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 351d76c3ee644d1337093daf9ed54cc987557a7ab8a62f9a2dac8d3060169aa1

Exact zero on the complete-recovery branch; other views and resource IDs are not merged.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 1f2ec36ee77640433d35436835aa971b04aba45bd076b61173b6d14d03a9d8bc

deterministic_risk AND N>=min(m,n)

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: e7c25ad8c777143fb1eac0b3a4c415ccc60e5ee97db4d04fa92f785ff663be4e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 5e3e8a151b06c696b975edf13e331bbfcd4341cc3e1419160d177774d53d3cdc

det_both_windows

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 5fd3d4a3e892293e222bcbe9f277b003b24b57fffc7dcaf926e1e345a836e57a

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 5598230b4a760f1b47ff3b29a1408eb44bf5b2a321409c1c2e3c1c110ee7a6d2

Both native brackets retained separately; cross-projection consolidated envelope is unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: e628523c1037277d5a44e0027e83c5881ef04c1a8c4e4ba312af1d6675fcd411

deterministic_risk AND NOT (N>=min(m,n)) AND deterministic_risk r1 with its own sufficient universal constant AND deterministic_risk r2 with its own sufficient universal constant

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 7410993470eab0e1bb10fe0e5531cacafd38c020f008f30f4bdaee4b8e4c16a6

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 79232dc13894941a1a5d225fa71157ae00448490f384e4e2d119a7106cfb93bc

det_old_only

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: d918c2546b0e2da3d2a596a2ac5698b7f010da2a40893b74489e1a290ea4b201

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: b5c9d71d3d79c5dae6cae1aeb953df52bfcf68508095658eb398f35902b01ff4

Old window retained; this is a source-applicability difference, not an intrinsic phase.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: fd2d02dd32078d6159be7cd027f6cd2e0e9bf61c94bcc786a977566824c18531

deterministic_risk AND NOT (N>=min(m,n)) AND deterministic_risk r1 with its own sufficient universal constant AND NOT (deterministic_risk r2 with its own sufficient universal constant)

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: 132faec0bf1dd3efe30ef8883043612c65d95ac3363758cb2462909bc591e08e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: cee28ae879d98456e629f78b262c82363af1531608c3d7d8ae1ea27f30a95618

det_new_only

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 87845cbe95a2a0b7a7210e89d07eab92f6c3f3190baa2a40c8fb1d3ef5feede9

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: c114136bb75a591293be7c73c35fbdc7de28dbaa04b163eaf85c6a680303f2e4

Newer native window retained with its own constant.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 1b0b3717baffe25d3d3d82081e23151f23d7bd6c035bb0009e8d41ae99fc4403

deterministic_risk AND NOT (N>=min(m,n)) AND NOT (deterministic_risk r1 with its own sufficient universal constant) AND deterministic_risk r2 with its own sufficient universal constant

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: 7b1ea220334d4f04f4a6484d39714983cbd0e6f46cd4c798eecd930292961ad7

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: 6c150dcdd972534bbed7374adfa599150f9eaf8d92d626e9ae2f7798202e6ceb

det_residual

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: 91deab7eacd2ab5af3989553eceb24e7ec99788095b124b04bfb52ed6546ee8f

No completed guarded envelope assembly here; this is not a proved open region.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: ae7b1cc3fa9b0f5df7eb9e9140b4341633f2cec183ab06de4e520ba6e366109d

deterministic_risk AND NOT (N>=min(m,n)) AND NOT (deterministic_risk r1 with its own sufficient universal constant) AND NOT (deterministic_risk r2 with its own sufficient universal constant)

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native item 6

Native pointer: /joint_analysis/domain_map/cells/5; canonical SHA-256: 37c0ac8cd3660767739072037a16d2d4fd98cbdde686153394076bdb23a33920

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/5/cell_id; canonical SHA-256: e8e7a1846e1edff278cc427a837c7947c6d664e99dea6cafa4133c2d651c4ea0

random_zero

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/5/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs; canonical SHA-256: 7619ce2ed3b41c7b79e0522b0c7b4d9db3cdb549bc4dcfae2d76aacd00f687ee

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs/0; canonical SHA-256: 808239454aaa76794fce024284a6de4efadb7f62dcce69715804d725f725b074

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_zero

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids; canonical SHA-256: 4f5f62c64fe1f1b855d6278826616df7a9b9c696224fe9448aa05792f8aaf7f9

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids/0; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/5/note; canonical SHA-256: bd7e56462435da7a5d6154de7dff539fae8fe020c284bcecd67921ec5a354afc

Only target-accuracy q2/resource_fbe102dfeb is certified here: native c4 and proof_uniform_zero establish exact zero cost on the full stated sufficient predicate. The epsilon>=2 c2 is a narrower q2 record; c1 is a guarded q2 overlap. Distinct source-scoped q1 is not certified or identified with q2.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/5/predicate; canonical SHA-256: b44475ee03040b6379fb25c3a3c5159567ca162c48880b7569a2aeee6fcedcff

m,n>=1, epsilon>0, epsilon>=2-2/max(m,n) in randomized_accuracy

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/5/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/5/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/5/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 7

Native pointer: /joint_analysis/domain_map/cells/6; canonical SHA-256: 773b5097e3dad4e0d553c51ad28756044fbffd2489adee4815b06c90411e5cef

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/6/cell_id; canonical SHA-256: 08a14e3b8effdec482904d3a64868719b70b7b2566649b78b64187c41a1ff504

random_hard_window

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/6/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids; canonical SHA-256: 861e9bf287255c7386af4022452865af9f1563760ecdb963bb4b4874337cc6f3

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids/0; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids/1; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/6/note; canonical SHA-256: 9037707ad9100fd74cf49b6907c7ec094c28c0c2bbe1b5a374642991af3ebd37

q2 upper retained; excluded lower claim remains outside the bracket. q1 is separate.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/6/predicate; canonical SHA-256: abd2c9357592af186a68387ae0d163fcdb1409b38e3904b5bbe93d42bdbdb664

randomized_accuracy AND epsilon<2-2/max(m,n) AND the unchanged randomized_accuracy r1 predicate: 0<epsilon<=epsilon_0, source-selected positive integer q asymp epsilon^(-2/3)/log^(1/3)(1/epsilon), m,n>=4q

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/6/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/6/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/6/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 8

Native pointer: /joint_analysis/domain_map/cells/7; canonical SHA-256: 9667aed6198642013d6d2ad0e6b3ad6ed52750513878ee01b7749e91f4b4cb08

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/7/cell_id; canonical SHA-256: b0b64f70ec5dca6fe2fb83f4cadedc18a90bbd3686bce3b68d287f006e5e8dc8

random_residual

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/7/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/7/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids; canonical SHA-256: 18b8f6dbc50460bddac7d197e4f74eb86c3bae8bee1a0626d9c4ecc814c123a5

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids/0; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/7/note; canonical SHA-256: 8c3a99fd294c07751d6823dc1b8d78ce0a22c61a76520d1edde32a808aedb0a4

q2 b2 exists on its source guard, but the complete joint scalar bracket outside the registered window is not assembled. q1 reconstruction remains separately recorded.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/7/predicate; canonical SHA-256: 747ba76a641f1802849f1b664e7160bc6347f7572195250e729e38875d552429

randomized_accuracy AND epsilon<2-2/max(m,n) AND NOT (the unchanged randomized_accuracy r1 predicate: 0<epsilon<=epsilon_0, source-selected positive integer q asymp epsilon^(-2/3)/log^(1/3)(1/epsilon), m,n>=4q)

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/7/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/7/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/7/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native item 9

Native pointer: /joint_analysis/domain_map/cells/8; canonical SHA-256: 7b4693a884423b2a201ad3a974998327471fb2241fc43af6d5b59e922e689312

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/8/cell_id; canonical SHA-256: bafa9bac0ccdf701b3768c0097fe4be86305e960dccadfed2210a3e6f2b05028

random_zero_q1_unassessed

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/8/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/8/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/8/comparison_ids; canonical SHA-256: 18b8f6dbc50460bddac7d197e4f74eb86c3bae8bee1a0626d9c4ecc814c123a5

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/8/comparison_ids/0; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/8/note; canonical SHA-256: 38916ccf5197a42b4deda1af594b74827729717c5784780df9cd6697e1bd2f57

At these same parameter tuples, the source-scoped q1/resource_cc7c360256 record remains separately unassessed as a scalar minimax target. The q2 zero-cost proof does not silently transfer to this different quantity/resource ID.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/8/predicate; canonical SHA-256: 3af8953dd018a9f1d0c9416e09310cd0394497d60f6b7c8a30be0c0a45083d43

m,n>=1, epsilon>0, epsilon>=2-2/max(m,n) in randomized_accuracy; distinct source-scoped q1 overlay only

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/8/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/8/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/8/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native item 10

Native pointer: /joint_analysis/domain_map/cells/9; canonical SHA-256: 9cbed2940b4094e76fe0186d4806cfe8e3401b0e178740439cb4c82a7ecb0810

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/9/cell_id; canonical SHA-256: f32dc935a099996146c6b409864e05b1e7a277029db39ba3898551b7d9c3c950

random_epsilon_two_overlay

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/9/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/9/closure_proof_refs; canonical SHA-256: 343493aef0c01dad949a0b83a69eb04f2a8c6c9783d33fd03d8ae00c62def26b

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/9/closure_proof_refs/0; canonical SHA-256: 350a70a747ddb690c16fc1f345033a1417d712258ced162725550a7a00a132ca

SIX_PROOF_c88bf8d96092

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids; canonical SHA-256: cba957483bc90f4358b0168e2ba4eed9682c99eb81a32199ff7dfad3784780ed

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids/0; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/9/note; canonical SHA-256: 4e86b882546b5ebd07591eecf8a8ad170d9d1b7fa8ee82d674535244c30a2625

The retained c2 zero-cost comparison is listed only on its own epsilon>=2 guard. It is a narrower overlapping certificate inside the broad q2 random_zero region, not a claim that c2 applies at every point of random_zero.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/9/predicate; canonical SHA-256: 8d1a4d82c9c8864ceabef4767e255c8469a2238c9383df108464446ff9d9f8ba

randomized_accuracy q2 only; m,n>=1 and epsilon>=2

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/9/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/9/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/9/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: a5a5f8b0131cc882b415eed6e051a61abc66e0a0cae5a677ec9edacda39a4202

Within deterministic_risk first split by N>=min(m,n), then outside it by the four Boolean memberships in r1,r2; these cells are disjoint and exhaustive regardless of numerical source constants. Within randomized_accuracy split by epsilon>=2-2/max(m,n), then outside it by r1 membership. Positive epsilon and dimension domains are retained. The c1,c2,c3 IDs in the zero cell mean only their guarded intersections, not unrestricted validity over that cell. The two view domains are separate tagged components. The random_zero closure selector is q2 alone via c4. The coextensive random_zero_q1_unassessed cell is a distinct source-contract overlay, not a second primary parameter phase or an identification of q1/q2. The random_epsilon_two_overlay lists the narrower retained c2 certificate with its own guard; it overlaps the primary zero cell deliberately and does not refine or enlarge that primary partition.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: c4f7d8988d13b2e341a14824f29334c49cc8ac3a16760af183a23d85afd68a63

Explicitly unassessed cells det_residual and random_residual; also unresolved consolidation of different deterministic native resource projections on overlapping source windows.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: b44e0cc8a3c75e75940df2a4cff5c7910ef3b7d5bd3a3c7cae3371829b0a6451

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 808c6a4a3ad37058bbc687d8845d7d01e25764974560e894f8c18e75ee0919ca

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 299cdad0b78e40043581ed64f159ac48a2377fa4b50a0c4f019d6c8c72f42318

The row-column coefficient absolute sum is (n-1)/n+(m-1)/m+|1/n-1/m|=2-2/max(m,n). Maximizing over row and column bounds the full gap. The endpoint is sufficient and closed; no randomized necessity is claimed. This is endpoint coverage, not a main-rate exponent improvement.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 386ac1635d6821be2e81116a454eedf599e19403944c96dc818be410828b1b2e

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 3

Native pointer: /joint_analysis/impact/0/comparison_ids/2; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: fb3cce86ac49ec8e320a896b8bb82949c71f17aaf2429465eb7fc7eb5bf58129

uniform_zero_endpoint

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 4a0390f6bab703e6247d609f85a03549fc7fa7b02912341af0618cb7022e0982

m,n>=1 and 0<epsilon<2 with epsilon>=2-2/max(m,n).

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: ccdf4c88a6fb756f2473e77460e154f78636fee11cf280852b6f42e3ba49d773

zero_query_endpoint

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 176681f5a126785bc23a52653410556f5245f4f21a67c153bf3c8f6ff759843e

Exact q2 cost 0 for epsilon>=2-2/max(m,n); c1 uses this branch on its guarded intersection and keeps its former upper bound elsewhere.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: ce0773b90de3630f90685a3314f4c6f55ad1b143f31c42b76aa0c46f90699bf9

Recorded q2 exact zero only for epsilon>=2; retained positive upper tilde O(epsilon^(-2/3)) on its strict epsilon<2 source guard, with no certified positive lower rate.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: b3cd537ce866965a359cedce1d975563520d2ddd0f76836945461c62386f8bac

epsilon>=2 already had exact zero. Outside the proved zero-cost region all scientific bounds and native comparison keys are retained.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: b44475ee03040b6379fb25c3a3c5159567ca162c48880b7569a2aeee6fcedcff

m,n>=1, epsilon>0, epsilon>=2-2/max(m,n) in randomized_accuracy

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 31b34831555de6af3a94b75b86e0e00af910600a4dad18f9d76caafc7e1b1668

m=n=2, epsilon=1: uniform strategies use zero calls and gap<=1 for every matrix. At m=n=1 every permitted epsilon has zero cost.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 961b0ca896d99e761b7b521284ebc94283af9c8f40835246c5f78be84dd3c6ba

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 24fd553775d8b2f4781909e5f237cf4eb73243661136ee5ddff6907f8d700bf9

Presentation organizes conditionally retained statements and labels unresolved consolidation honestly. It supplies no new external theorem and does not turn unassessed cells into open-problem claims.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: ff715872a3fca718f101f073194bbf750b970eeccc3c783761e96c39cce963dc

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native item 4

Native pointer: /joint_analysis/impact/1/comparison_ids/3; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 5

Native pointer: /joint_analysis/impact/1/comparison_ids/4; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 6

Native pointer: /joint_analysis/impact/1/comparison_ids/5; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: fcdd6190343c888ccea6f4d6f5a5f625d1457b21baf2334f1792d2ec063b793b

first_joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: a6bb2d633e7b42f6a0dcbe9df404ce3307e6a5a617bf6dcc759fb53d9463f6f4

No scientific rate improvement from the annotation itself.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 500eeeb2181c8529ebddf2a642369782ddbcde3cdd51a188d76ed903fcd85c17

The same retained native brackets and statuses, except the separately proved endpoint update, now have explicit joint variables, guards, candidate dispositions and unassessed cells.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: b368ba866d5c486370ab30b578e1d7e83a2253f04c9974395fdef6d4f7505c34

Separate native comparisons without a joint domain map.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: cd5c916efec41c1cc624bc6d0d038936738e089675338b3b75eb36843eda6c3f

All baseline scientific rows other than the explicitly patched c1 envelope; exact-zero c2 and all deterministic/source-scoped rows are preserved.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 13e843375a65ee693a5e47be4a710c7f6315dc639214ade1e00fae4e7417a862

The fixed original view domains.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 1d44427dd94dc65b390c9b4314fa8aded5720aeebaa68e105c9f4c1a3d363c77

The source-scoped q1 recovery statement is kept separate from q2, and different native resource IDs are not merged.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: d50fb21665d2de0b9812bdffe48d109224460071bd652ab0c40bb0d8c808b2ff

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: a3334a9180e9a133331f4cdfcb1665b3cb9824b95716ebf3a54fe84c9df0d6f2

Actual source text at characters 4700-10200 was read; no unverified precision-log inversion or new mapping is adopted.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: a0a37223b1a233f473911838d4fd56a39bea197c1cd6ccf8ae5f54e1ab5512f0

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: b619912846eaeb976c40ae7b8b0a57011c61699107cf34dad07cab426ef294df

named_upper_rate

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 5944d506615408def1ee6153bca215ef7fdcf454b5f0ad0692eef70b98e40619

No new main-rate adoption.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 01160fdd9863a7418d553cb110accd09ef9bd77ab173faf86a8dcc5270355888

Existing tilde epsilon^(-2/3) upper claim and its retained fixed-budget inversion.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 8fd4e2dbd843558cb586fbd9f28a2deec4789294b5378c6cc9a4e2ade4a42688

All main-rate branches.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: e8bf5070457aa94c0595eb01d2f4d780d339d2bd48486e5eeaf28acfdd601551

The theorem's native source scope, retained as in the baseline.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: bdc3e425815acdc0ddee91b8aac1dff46889195a4ba3ed47cbd265272760b8e6

Theorem 1.1 of arXiv:2601.02347v3 repeats the already recorded deterministic exponent.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: b86161fdd22aa262a7e2416e48b8c7c87b27eeef4b17f0f445525104a46f078e

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 6da99f76c7be2920e3d526952442c3842471dfe29d179883473c570fdef41742

Characters 41700-44100 were independently read. A claimed exponent and literature metadata do not establish the missing proof.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 74524af9de76a9514691e9e0e68fe012ef85f5733169b46d47eeb546212c8341

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 674cd766cf9abdde3499ded264df88c173c7eed0328bc8aef70db71af515da0e

random_lower_still_unverified

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 26c022e462249251d08bef526a363d8836106ef0313bf93729679bb239b7eea8

Same exclusion.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: aea2bae9aab17e10d16567aa4c1eb6a222c45351c4d8337132f24558f5113b2a

Randomized b1 excluded; no certified positive lower rate.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: aa908891d0e9f44d7f8692fc723679b3babc1f7b4bd3d012a1d8d64b52dcf639

All lower-rate adoption decisions.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 77c12b7fedff5579e9061a0738090a997621a2300e14b2e9b653f3d475f65743

the unchanged randomized_accuracy r1 predicate: 0<epsilon<=epsilon_0, source-selected positive integer q asymp epsilon^(-2/3)/log^(1/3)(1/epsilon), m,n>=4q

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 9fe0e0ef0fe35f89eb4ce9ffe74fac143d6b1c280b6234fb3bc08abbad064130

arXiv:2610.02095v2 Section 8 still states that adaptive-core verification is unresolved.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: 34119b397dc917c6b0fe160c0b0c854f149448a8afd720aa4a4c2882adabdf51

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 56d9e66e2b9e81d38efa09f7945f6b7dcc51e209c7f0ffd714ef558bc9d54771

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration. This revision addresses the preserved actual independent-review issues. Publication and typed projection obligations are explicit; every mathematical formula and adoption guard is verified against the exact native candidate, and historical effects are not reported as new frontier gains.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 2d26a8a9a23b47aff0d2e563c9a078161ed96d8e2d469fe17051d327924a502f

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 3

Native pointer: /joint_analysis/impact/4/comparison_ids/2; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native item 4

Native pointer: /joint_analysis/impact/4/comparison_ids/3; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 5

Native pointer: /joint_analysis/impact/4/comparison_ids/4; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 6

Native pointer: /joint_analysis/impact/4/comparison_ids/5; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native item 7

Native pointer: /joint_analysis/impact/4/comparison_ids/6; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 5282f962c07b3bb29d06c005055835c072b37ac5fafb158fb660924d0a50ed1e

curated_feedback_CV_S_SIMPLEX_MATRIX_GAME_20261116_2a144b4edf

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: c2fefc7028d175e4e57523ef01ff20aac69a7cb129501c7f8dec75285046ba23

Disjoint union of native contracts: deterministic_risk q1 is minimax full saddle-gap risk for integer N>=1 and m,n>=2; randomized_accuracy q2 is the least fixed worst-case bundled-call cap for epsilon>0 and positive integer m,n with instancewise success >=2/3. Its distinct q1 is only a source-scoped resource statement. All instances have |A_ij|<=1. Joint variation is within each view, never between incompatible costs. Derived d=n+m is redundant; source q is selected through epsilon, not an independent asymptotic budget. Tracking q and epsilon_0 in q2 metadata does not make them independent joint inputs. The fixed-public-input wording of deterministic q1 defines pointwise minimax values and its tracked N,m,n vary jointly here; no metadata edit is required.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 410c7e6591431c8993c38e966baeb10765e6b9a2e0cb02a50f23927cb907d418

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 395ab86ea81939f6cdc73f64388fda360c83a360fef4911fbb4d02d8becfea36

Complete scientific screening of the discovered arXiv:2412.06990v4 route if pursuing a main-rate change; it was metadata-screened but its primary theorem was not read in this finite step.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: dc20c8f4bd53974f7ead38f9a6c0ea9e74ce7b0ced77a48d01e639beaca7285e

Reconcile different deterministic resource-projection IDs by an explicit reviewed transfer before a consolidated strongest envelope is claimed; keep r1/r2 constants and extreme dimension logarithms explicit.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: d81d6790d695413d6e6272f5b1b15d8a73bd72f0f4b17e1e1cd2711a978087ef

The randomized lower candidate's central adaptive-core proof remains unresolved; it is not eligible for adoption.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 1952fe99bc06c2e19e96571bbbb03a7d3b9bba8c164027d8d7bd19015d273244

Assemble q2 envelopes on the unassessed complement and review any desired q1-to-q2 reconstruction transfer separately. These tasks do not affect the zero-call proof.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 9243e26e94e59999e1a877688ac54071b0a386a7b64440f043e5501a15701710

Assess compatible_candidates for CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1 and CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 1887c357506a2737a33e372677e39157c911a2688661903104d5c89df75b6b85

Assess compatible_candidates for CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2 and CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native item 7

Native pointer: /joint_analysis/pending_obligations/6; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: d826928b7b662dbe4129f2edd114f81e07a411f9c9875ea57b4bc538064f92a6

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: b440da739059637128f7ee95a0a98e9d1e8d5ccc18398ec1930e038afadfd1bc

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: a94c57c4f61e7d0b7c343022890872a95f17357aa69e41da78c616356fcdf384

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 0812b4745113d9eaed97d3a639ec908f46f1e7d1581992f1146f4ff43d444ad6

Uniform feasible output has complete saddle gap <=2-2/max(m,n) for every fixed matrix, with no information calls; deterministic success implies the randomized 2/3 guarantee. Nonnegative call cost gives equality.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 7619ce2ed3b41c7b79e0522b0c7b4d9db3cdb549bc4dcfae2d76aacd00f687ee

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: 808239454aaa76794fce024284a6de4efadb7f62dcce69715804d725f725b074

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_zero

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 5b5f65d935c301ac41d8451c4e4e10ae6f7428329b42f655c886afea3ab8a682

All admissible entry-bounded matrices; m,n>=1.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 8d315121c716a69b3b26f05f31e546cb8ad82d544924efe419d1e997dbdb363d

New proof CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_zero; exact premises /common_specification, /views and /quantities/2 with frozen hashes in the endpoint finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: b44475ee03040b6379fb25c3a3c5159567ca162c48880b7569a2aeee6fcedcff

m,n>=1, epsilon>0, epsilon>=2-2/max(m,n) in randomized_accuracy

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: bd530c305b9a6d0cebe6375eaf23e46d1045555761d617ef9f3b82710ed74386

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 2d26a8a9a23b47aff0d2e563c9a078161ed96d8e2d469fe17051d327924a502f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/6; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: d4d3066227543deefb2bd165a10a4f8922532486377109007e37e62d29936c86

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: f44902418633a6a927c42d0e451b78fdca596b9167d496f6305c3031528c835c

No new blind literature search in this migration. Conditional retention of the exact preceding accepted analysis and its finite historical scope; all stated pending work remains pending.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: dd108b5701a0e74097be519a9e6d97f9af44b1e4fa94310dc641757befc216fc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 9196afddf7a31ea6301c3d967b5370fe1a5cbf5febbc46ca7a2e1d34114d0491

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: 54a66eab467db3d40ca6c45ae750e0e0576d631e4d5d8010be0ccc1904086c2b

This directed projection/replacement opportunity needs a separate applicability/cost judgment. Distinct IDs are not merged, and no opposite-direction inference is made.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: fc0551323e345b5807cd54fb4e76d27bdfbcfb02b5a6b1ff2c0b30c406ad1148

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 01d465a421d168e38d75220694c187b6accb7bc75433156fcbd2beca84baf9f2

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: bef61c893b62a9b6ef2ebe6d035397360122acd8b22aa112f181ed518cffd6e0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 65ab802771376684e423cc910702b160a81641c40fec2789935eec0f098d5e98

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: 73359df32b2c1fc28e3fcf50a03a7e3ec4458f8f2d0ec9b0032ae2bee3d4bb4d

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/4; canonical SHA-256: fa5bfcbde9ab5c79976bb3f6512ec65b9495ff4e41711740b2d73b3dbed566b0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: d918c2546b0e2da3d2a596a2ac5698b7f010da2a40893b74489e1a290ea4b201

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: cbd717faae83a18dcd0984f69326879d0fe1418a4573e90441638e7d8eb23ec6

synthesis-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: 9243e26e94e59999e1a877688ac54071b0a386a7b64440f043e5501a15701710

Assess compatible_candidates for CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1 and CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 1d3dbd00acd0b7c46c630a3a6be79f9da4883b6e8c5ddc90ab6234125338485d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: 54a66eab467db3d40ca6c45ae750e0e0576d631e4d5d8010be0ccc1904086c2b

This directed projection/replacement opportunity needs a separate applicability/cost judgment. Distinct IDs are not merged, and no opposite-direction inference is made.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: fc0551323e345b5807cd54fb4e76d27bdfbcfb02b5a6b1ff2c0b30c406ad1148

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 01d465a421d168e38d75220694c187b6accb7bc75433156fcbd2beca84baf9f2

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: bef61c893b62a9b6ef2ebe6d035397360122acd8b22aa112f181ed518cffd6e0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 65ab802771376684e423cc910702b160a81641c40fec2789935eec0f098d5e98

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: 73359df32b2c1fc28e3fcf50a03a7e3ec4458f8f2d0ec9b0032ae2bee3d4bb4d

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/4; canonical SHA-256: fa5bfcbde9ab5c79976bb3f6512ec65b9495ff4e41711740b2d73b3dbed566b0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 87845cbe95a2a0b7a7210e89d07eab92f6c3f3190baa2a40c8fb1d3ef5feede9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: ebcba919e62a1ab3932a5511960ae541204ef3e4e612a3e2b58eaa7aea342c2d

synthesis-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 1887c357506a2737a33e372677e39157c911a2688661903104d5c89df75b6b85

Assess compatible_candidates for CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2 and CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 0c13e404c6d3b29d19e71cf611d90f59882303627c40dbdd0394984966aac028

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: fc0551323e345b5807cd54fb4e76d27bdfbcfb02b5a6b1ff2c0b30c406ad1148

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: 01d465a421d168e38d75220694c187b6accb7bc75433156fcbd2beca84baf9f2

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: bef61c893b62a9b6ef2ebe6d035397360122acd8b22aa112f181ed518cffd6e0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 65ab802771376684e423cc910702b160a81641c40fec2789935eec0f098d5e98

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: 73359df32b2c1fc28e3fcf50a03a7e3ec4458f8f2d0ec9b0032ae2bee3d4bb4d

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: fa5bfcbde9ab5c79976bb3f6512ec65b9495ff4e41711740b2d73b3dbed566b0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 45b99c8f3b75fd37ce9c74fa7ae92d81dbc055c826e06e036b94bd76dd26e7c8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 94ebdcb021bcbc6fc94fa708c1e7a7f9d1afd6248b96e70935fa7df176e425ff

synthesis-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 8adaa5adbd9bf2c9b4c2b02ccb130509dc62519ab6b55cd11c05e4c23c856c53

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: e019ffaf71800e35fdc9b361259390fa21e9f990c0aa8d2b9ae2dce3f4e7a971

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: 0224e431fa3bf7cd690f5dc00f4ee780b807c10124c62e0c1b04f1776ae7e683

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 01ef8c82e9d9d74a051196b44c17098dff68f22b1de8b0153e3183a6b0726716

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: a94c57c4f61e7d0b7c343022890872a95f17357aa69e41da78c616356fcdf384

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 74524af9de76a9514691e9e0e68fe012ef85f5733169b46d47eeb546212c8341

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 7f1a6540bd14dbb3bcfdfdfac9a64bfde09607556bb3c904bfc43adedf6ede22

synthesis-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 5ea2ffe816e856673279bad6fb27e7143438f295a800e1943ae5360187c5ff1d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: e019ffaf71800e35fdc9b361259390fa21e9f990c0aa8d2b9ae2dce3f4e7a971

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: 0224e431fa3bf7cd690f5dc00f4ee780b807c10124c62e0c1b04f1776ae7e683

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: 01ef8c82e9d9d74a051196b44c17098dff68f22b1de8b0153e3183a6b0726716

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: a94c57c4f61e7d0b7c343022890872a95f17357aa69e41da78c616356fcdf384

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: cba957483bc90f4358b0168e2ba4eed9682c99eb81a32199ff7dfad3784780ed

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: ca0bbdf769e92b6ee0fc04da5960cb413f34af9e8cc0d5eca08f2ac29f71ac8f

synthesis-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: ec2bd9717d00fff7779be72f93dbb1022c08e2bf5d143dc602f76d32a58f1691

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 74f99108d3804d3af139e811cfe7217592990cfb2dbdd948c7d887a481278568

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/0; canonical SHA-256: 0b26e5a1e918922c6f8a62347f2b5b32e5e2ceb775f0a4093fedc9d16f31a792

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 18b8f6dbc50460bddac7d197e4f74eb86c3bae8bee1a0626d9c4ecc814c123a5

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 8cedb7c54fb7a3ff1b2d98263a56263d1a8afbb4fdabf8cee435054dc16d1ea3

synthesis-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 52fddbdce5aa47c9514821d42fda98de53084bf4e7cb4a52cefc5646357c7817

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: e019ffaf71800e35fdc9b361259390fa21e9f990c0aa8d2b9ae2dce3f4e7a971

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/0; canonical SHA-256: 0224e431fa3bf7cd690f5dc00f4ee780b807c10124c62e0c1b04f1776ae7e683

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/1; canonical SHA-256: 01ef8c82e9d9d74a051196b44c17098dff68f22b1de8b0153e3183a6b0726716

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/2; canonical SHA-256: a94c57c4f61e7d0b7c343022890872a95f17357aa69e41da78c616356fcdf384

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 4f5f62c64fe1f1b855d6278826616df7a9b9c696224fe9448aa05792f8aaf7f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 5fa33983f32a4c1027a92106c478a51fb23e76f63df8884a2a111e3319f68669

synthesis-6

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 76f4af52bdbcf52ea2cff1f90ba90e3726f2c97f4620684a5e3a24a8799531b6

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 2d26a8a9a23b47aff0d2e563c9a078161ed96d8e2d469fe17051d327924a502f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/2; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/3; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/4; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/5; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/6; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 395ab86ea81939f6cdc73f64388fda360c83a360fef4911fbb4d02d8becfea36

Complete scientific screening of the discovered arXiv:2412.06990v4 route if pursuing a main-rate change; it was metadata-screened but its primary theorem was not read in this finite step.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: d8b07fb0a841d8069335d4999bada9290b45eb9c4fde76bfa0477b5a33e3260e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 2d26a8a9a23b47aff0d2e563c9a078161ed96d8e2d469fe17051d327924a502f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/2; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/3; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/4; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/5; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/6; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: dc20c8f4bd53974f7ead38f9a6c0ea9e74ce7b0ced77a48d01e639beaca7285e

Reconcile different deterministic resource-projection IDs by an explicit reviewed transfer before a consolidated strongest envelope is claimed; keep r1/r2 constants and extreme dimension logarithms explicit.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 18d17de914db56abcd1773ba80485e4cca19dcbbabc7124878401d7cbdcd33d2

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 2d26a8a9a23b47aff0d2e563c9a078161ed96d8e2d469fe17051d327924a502f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/2; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/3; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/4; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/5; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/6; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: d81d6790d695413d6e6272f5b1b15d8a73bd72f0f4b17e1e1cd2711a978087ef

The randomized lower candidate's central adaptive-core proof remains unresolved; it is not eligible for adoption.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: 91995225b67dacea2a501d6fbed9d38f7e2d874d3a6eb5eb85ea103a5d39a859

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 2d26a8a9a23b47aff0d2e563c9a078161ed96d8e2d469fe17051d327924a502f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/2; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/3; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/4; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/5; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/6; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 1952fe99bc06c2e19e96571bbbb03a7d3b9bba8c164027d8d7bd19015d273244

Assemble q2 envelopes on the unassessed complement and review any desired q1-to-q2 reconstruction transfer separately. These tasks do not affect the zero-call proof.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: 18e42e2354fd3c05961cb41a8ecd3ff68ac7ede9c8472feb7da6fc8ddb96d9fa

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: 2d26a8a9a23b47aff0d2e563c9a078161ed96d8e2d469fe17051d327924a502f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/2; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/3; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/4; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/5; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/6; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: a0050dd45f09b8c1454f66ddc34c7e3533ab3f980a23fb9c8576d4ecdca8fe45

retained-material-lead-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: 9243e26e94e59999e1a877688ac54071b0a386a7b64440f043e5501a15701710

Assess compatible_candidates for CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1 and CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/obligations/12; canonical SHA-256: 4097f74cdfc3e25e2e42f057c4fbdf0ae6edd49edca7fb05f84448131706c4a9

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids; canonical SHA-256: 2d26a8a9a23b47aff0d2e563c9a078161ed96d8e2d469fe17051d327924a502f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/2; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/3; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/4; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/5; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/6; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/id; canonical SHA-256: 816e64d45ab01655b0cdb3174cc88338b9552319d4504b2ed46ed2504883fbc8

retained-material-lead-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/lead; canonical SHA-256: 1887c357506a2737a33e372677e39157c911a2688661903104d5c89df75b6b85

Assess compatible_candidates for CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2 and CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 14

Native pointer: /joint_analysis/synthesis_coverage/obligations/13; canonical SHA-256: 6dd9ff0df6fd9a3b1f2f65b44cd7ba3f0016117194337a72ab37914345c9bf79

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/argument; canonical SHA-256: 72cb768aa9bc817e3464adc8ebe2016f9ad4fd47bd279a71d5899fab8d317c6f

Directed pending comparison: source resource_ddb4d07949 -> target resource_9c7841878b for the same declared fixed-budget saddle-gap quantity. This is only an opportunity, not an asserted resource identity. Prove the exact allowed query simulation, charged budget, risk guarantee, both source windows and independent constants, including extreme dimension logarithms, before consolidation; do not infer the reverse direction from this record.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs; canonical SHA-256: c6c0eaf99057774de40466b6a2eb811ac0e216e8784b44353bff2f7663afb4f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/0; canonical SHA-256: 01d465a421d168e38d75220694c187b6accb7bc75433156fcbd2beca84baf9f2

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/1; canonical SHA-256: bef61c893b62a9b6ef2ebe6d035397360122acd8b22aa112f181ed518cffd6e0

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids; canonical SHA-256: faac97b1ca36ce9049a4d7a7e6df7e14c887c388be2bc8822b04aab1d03f5eca

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids/0; canonical SHA-256: 5e3e8a151b06c696b975edf13e331bbfcd4341cc3e1419160d177774d53d3cdc

det_both_windows

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids/1; canonical SHA-256: 79232dc13894941a1a5d225fa71157ae00448490f384e4e2d119a7106cfb93bc

det_old_only

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids/2; canonical SHA-256: cee28ae879d98456e629f78b262c82363af1531608c3d7d8ae1ea27f30a95618

det_new_only

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids; canonical SHA-256: 5fd3d4a3e892293e222bcbe9f277b003b24b57fffc7dcaf926e1e345a836e57a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/id; canonical SHA-256: b7a7b7f4dc8c92de5fe3209b6b33aaea710a47bb4d2b8a8313154af8141fb31b

typed-det-ddb4-to-9c

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/lead; canonical SHA-256: dc20c8f4bd53974f7ead38f9a6c0ea9e74ce7b0ced77a48d01e639beaca7285e

Reconcile different deterministic resource-projection IDs by an explicit reviewed transfer before a consolidated strongest envelope is claimed; keep r1/r2 constants and extreme dimension logarithms explicit.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 15

Native pointer: /joint_analysis/synthesis_coverage/obligations/14; canonical SHA-256: 3b6bd7af8e3d68a16a794d1b8094762b4f87fa9ae999728f2190dd07445d959c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/argument; canonical SHA-256: 81d4df6a47fc4e9dbe295978efdb9ad684c12d108d74788f6dac453d9342e38e

Directed pending comparison: source resource_9c7841878b -> target resource_ddb4d07949 for the same declared fixed-budget saddle-gap quantity. This is only an opportunity, not an asserted resource identity. Prove the exact allowed query simulation, charged budget, risk guarantee, both source windows and independent constants, including extreme dimension logarithms, before consolidation; do not infer the reverse direction from this record.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs; canonical SHA-256: e75e87f4f58f9bd52e8469a4fff1aa76fa1f1a8e3cb66ef1a954ace33209d529

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs/0; canonical SHA-256: 65ab802771376684e423cc910702b160a81641c40fec2789935eec0f098d5e98

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs/1; canonical SHA-256: 73359df32b2c1fc28e3fcf50a03a7e3ec4458f8f2d0ec9b0032ae2bee3d4bb4d

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids; canonical SHA-256: faac97b1ca36ce9049a4d7a7e6df7e14c887c388be2bc8822b04aab1d03f5eca

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids/0; canonical SHA-256: 5e3e8a151b06c696b975edf13e331bbfcd4341cc3e1419160d177774d53d3cdc

det_both_windows

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids/1; canonical SHA-256: 79232dc13894941a1a5d225fa71157ae00448490f384e4e2d119a7106cfb93bc

det_old_only

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids/2; canonical SHA-256: cee28ae879d98456e629f78b262c82363af1531608c3d7d8ae1ea27f30a95618

det_new_only

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids; canonical SHA-256: 5fd3d4a3e892293e222bcbe9f277b003b24b57fffc7dcaf926e1e345a836e57a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/id; canonical SHA-256: 2d85bfb4eb69dac2e15e832fc1ea1e816b22daa988c7f2aadc6be1ec2a9481c7

typed-det-9c-to-ddb4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/lead; canonical SHA-256: dc20c8f4bd53974f7ead38f9a6c0ea9e74ce7b0ced77a48d01e639beaca7285e

Reconcile different deterministic resource-projection IDs by an explicit reviewed transfer before a consolidated strongest envelope is claimed; keep r1/r2 constants and extreme dimension logarithms explicit.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 16

Native pointer: /joint_analysis/synthesis_coverage/obligations/15; canonical SHA-256: a02c8e994e06a69efe2ff2b0f69384554755fd1541c9009790a2e4b65ef9aed7

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/argument; canonical SHA-256: 8a737095f1dc0c3c0d17797aeff06dd9895f1e9d991824c7a23b8fa266bfe8e6

Directed pending route: randomized_accuracy b3 on source-scoped q1/resource_cc7c360256 -> target-accuracy q2/resource_fbe102dfeb. Establish the same algorithm family, outputs, fixed-path bundled-call count, instancewise probability, full precision/dimension domain and source guard before adopting a reconstruction bound in q2. The source q1 is not automatically a scalar minimax quantity, and neither q1/q2 nor their resource IDs are merged. The already proved q2 zero branch is unaffected.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs; canonical SHA-256: 74f99108d3804d3af139e811cfe7217592990cfb2dbdd948c7d887a481278568

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs/0; canonical SHA-256: 0b26e5a1e918922c6f8a62347f2b5b32e5e2ceb775f0a4093fedc9d16f31a792

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids; canonical SHA-256: 0bb624f32df7ccffcc4da7903aa45337e268697388111c93950e19f369b8f24f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids/0; canonical SHA-256: 08a14e3b8effdec482904d3a64868719b70b7b2566649b78b64187c41a1ff504

random_hard_window

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids/1; canonical SHA-256: b0b64f70ec5dca6fe2fb83f4cadedc18a90bbd3686bce3b68d287f006e5e8dc8

random_residual

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids/2; canonical SHA-256: bafa9bac0ccdf701b3768c0097fe4be86305e960dccadfed2210a3e6f2b05028

random_zero_q1_unassessed

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids; canonical SHA-256: b3fa26d540714dab81b9a3e7f4c0ca66f5dcb1e74a21c15b365b898cec5bd142

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/0; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/1; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/2; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/3; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/id; canonical SHA-256: e711d4da02e43891f722f58ca20a5b213589078cb71ec7564f8ddd6d65df4c03

typed-rand-source-q1-to-target-q2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/lead; canonical SHA-256: 1952fe99bc06c2e19e96571bbbb03a7d3b9bba8c164027d8d7bd19015d273244

Assemble q2 envelopes on the unassessed complement and review any desired q1-to-q2 reconstruction transfer separately. These tasks do not affect the zero-call proof.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 17

Native pointer: /joint_analysis/synthesis_coverage/obligations/16; canonical SHA-256: 11f0391cf3079ed0f660eac67c6522f5d5526db2cf123a303166dc40c6e59ba7

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/argument; canonical SHA-256: c60f505a364ba8a8d877ee5b7ad6d42e41294d376aecc4e4ae70dee84da04e74

The existing native optimal q2 c4 comparison and the independently specified uniform-output proof certify exactly zero calls on epsilon>=2-2/max(m,n), including equality. This closure selector excludes the distinct q1 c3 source statement and claims no necessary maximal zero-query threshold.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs; canonical SHA-256: ac68a707a0b956f982413f2748751422de53c659d96dc8ef1606c17730289318

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/0; canonical SHA-256: a94c57c4f61e7d0b7c343022890872a95f17357aa69e41da78c616356fcdf384

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids; canonical SHA-256: 94785a046f52faa6415523e67cb64f9a303a4bfd699b949b40deb100b24c61bb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids/0; canonical SHA-256: e8e7a1846e1edff278cc427a837c7947c6d664e99dea6cafa4133c2d651c4ea0

random_zero

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids; canonical SHA-256: 4f5f62c64fe1f1b855d6278826616df7a9b9c696224fe9448aa05792f8aaf7f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/0; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/id; canonical SHA-256: d62374531b980bd0f2c047b87628cdbb060ad560f30cd60c960d2d338e9607f3

typed-publish-q2-uniform-zero

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/kind; canonical SHA-256: 50133df05f664fa7a089f5165d8e064594aa92d2dedff6eb73c481199b11b5cd

closed_region_publication

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs; canonical SHA-256: 7619ce2ed3b41c7b79e0522b0c7b4d9db3cdb549bc4dcfae2d76aacd00f687ee

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs/0; canonical SHA-256: 808239454aaa76794fce024284a6de4efadb7f62dcce69715804d725f725b074

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_zero

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 18

Native pointer: /joint_analysis/synthesis_coverage/obligations/17; canonical SHA-256: 3fcb1e2456b7bb9a8ec9b70bbafc3a411d329086800e9a2d06a04e426e0bd680

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids; canonical SHA-256: 2d26a8a9a23b47aff0d2e563c9a078161ed96d8e2d469fe17051d327924a502f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/0; canonical SHA-256: 12b95f5f195772a41787531b434ffa01d4713c832ee79c2171fb5ef9d795dc74

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/1; canonical SHA-256: 397999a82ffee7dad39163f4672e01d2c5c77d43ffecb03018cdb19b221ed414

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/2; canonical SHA-256: 4a57b9a450e216ec676fed124084da8f4f6d3aac8d0cb1fae59c4f2dcceb38aa

CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/3; canonical SHA-256: 8e3d1cf145bb7b574b46ec2905378b57649dd9da7f8eea79626579915a97a464

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/4; canonical SHA-256: d8d3f0fd84c6bd7b4d847c976f5591f107b0ca37d00b639e7200ba779e42db5c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/5; canonical SHA-256: c44a5d929bd5610a095a5613c61c1567a191ab1b2dd0bcb7b467f391897baaff

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/6; canonical SHA-256: 0e8b2fdbab3a7bf20830fd5f8fd1f2818734298fcef951541ff89efbf0baef95

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/id; canonical SHA-256: 7b66618750ce506ccf40819cef50f764846b4ebf660cc36789c8ef551ca05dfe

curated-scope-limit-2a144b4edf

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 0c48c6d68957143dbf6ad0bea963eb184040f6076d77202e84ee61f2c49b1fe5

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: bb45436f2986b85857424be2f8c43d2451bcd5a420696958170f92dd226d3f3a

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: 8d65311f8a785198e53a1915bb5908b3c4abf1e26623fde6d8d4f09ed2c903fc

/views/1

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: f1096cde15a520562dc4693c6e0b624bdb9b388f32263d6c4947dbf7a56c363a

/quantities/1

#### Native item 7

Native pointer: /joint_analysis/target/contract_refs/6; canonical SHA-256: 4b81cab280b1e31c2ea7afa9a416577b7c9c22795698d5d642e0394c36a90edd

/quantities/2

#### Native item 8

Native pointer: /joint_analysis/target/contract_refs/7; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 9aeca75ca7a72e23c49a01f1a446b8413de03f869df2a81b1691c2ce131e622a

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 07eb839401397f911b0ac8db4f8323c07d0e06d35bd8595da9842401f28a8f25

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: b02d131326a05f6ae4132570176b105a7b6fdd9dad9c60aa9281f030290f19c7

Universal positive source threshold; its value is not numerically specified and is not a jointly varying input.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 322dba9ee8e3a24549067957d3cfcd7965218db4ad0272986c31916fe1680bdd

CV_S_SIMPLEX_MATRIX_GAME_p_bd49cae22d

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 322dba9ee8e3a24549067957d3cfcd7965218db4ad0272986c31916fe1680bdd

CV_S_SIMPLEX_MATRIX_GAME_p_bd49cae22d

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: c2fefc7028d175e4e57523ef01ff20aac69a7cb129501c7f8dec75285046ba23

Disjoint union of native contracts: deterministic_risk q1 is minimax full saddle-gap risk for integer N>=1 and m,n>=2; randomized_accuracy q2 is the least fixed worst-case bundled-call cap for epsilon>0 and positive integer m,n with instancewise success >=2/3. Its distinct q1 is only a source-scoped resource statement. All instances have |A_ij|<=1. Joint variation is within each view, never between incompatible costs. Derived d=n+m is redundant; source q is selected through epsilon, not an independent asymptotic budget. Tracking q and epsilon_0 in q2 metadata does not make them independent joint inputs. The fixed-public-input wording of deterministic q1 defines pointwise minimax values and its tracked N,m,n vary jointly here; no metadata edit is required.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 2372ccc11d104ad4921365840f271b5f35c6740d183408a409049efa9724c0ef

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 78ff6dd70b4caac907e0a385eaa192f90843a0b14cd24a344d9f7d1a4dded319

CV_S_SIMPLEX_MATRIX_GAME_p_0b9ae4651b

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 5cef0704ac0dbf70151ed70c6b302c697117ac69e525f5ce5fc8405a44c28bc1

CV_S_SIMPLEX_MATRIX_GAME_p_a171441ef1

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 7fee57c670d23d2fa4b1dcd09028fb758ad56eb068d0d1c96f01348fcbac4ab0

CV_S_SIMPLEX_MATRIX_GAME_p_ed345de805

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 99344acb3790ea62d00f27f9ab40ef5e0f4c166e4bace49fc7021735a03575e0

CV_S_SIMPLEX_MATRIX_GAME_p_258cd1f3e7

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: b96d2064cef7cf920864e8b27afa9f709ae4ae9daac6411d1fc6a588b5cd9954

CV_S_SIMPLEX_MATRIX_GAME_p_b427b8da1a

#### Native item 6

Native pointer: /joint_analysis/target/joint_variables/5; canonical SHA-256: 5eeb150e1a6a59abd2ea43a73bb97290c329794d3009c1b2ca78564a0f491d09

CV_S_SIMPLEX_MATRIX_GAME_p_39006b19fa

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 2372ccc11d104ad4921365840f271b5f35c6740d183408a409049efa9724c0ef

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 78ff6dd70b4caac907e0a385eaa192f90843a0b14cd24a344d9f7d1a4dded319

CV_S_SIMPLEX_MATRIX_GAME_p_0b9ae4651b

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 5cef0704ac0dbf70151ed70c6b302c697117ac69e525f5ce5fc8405a44c28bc1

CV_S_SIMPLEX_MATRIX_GAME_p_a171441ef1

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 7fee57c670d23d2fa4b1dcd09028fb758ad56eb068d0d1c96f01348fcbac4ab0

CV_S_SIMPLEX_MATRIX_GAME_p_ed345de805

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 99344acb3790ea62d00f27f9ab40ef5e0f4c166e4bace49fc7021735a03575e0

CV_S_SIMPLEX_MATRIX_GAME_p_258cd1f3e7

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: b96d2064cef7cf920864e8b27afa9f709ae4ae9daac6411d1fc6a588b5cd9954

CV_S_SIMPLEX_MATRIX_GAME_p_b427b8da1a

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: 5eeb150e1a6a59abd2ea43a73bb97290c329794d3009c1b2ca78564a0f491d09

CV_S_SIMPLEX_MATRIX_GAME_p_39006b19fa

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Ishani Karmarkar; Liam O'Carroll; Aaron Sidford. Solving Matrix Games with Near-Optimal Matvec Complexity. 2026. arXiv:2601.02347v3, 2026-06-22.

https://arxiv.org/pdf/2601.02347v3

[2] Guy Kornowski; Ohad Shamir. The Oracle Complexity of Simplex-based Matrix Games. 2026. arXiv:2412.06990v4, 2026-02.

https://arxiv.org/pdf/2412.06990v4

[3] Guy Kornowski; Ohad Shamir. The Oracle Complexity of Simplex-based Matrix Games: Linear Separability and Nash Equilibria. 2025. COLT, PMLR291:3292--3318.

https://raw.githubusercontent.com/mlresearch/v291/main/assets/kornowski25a/kornowski25a.pdf

[4] Arkadi Nemirovski. Prox-Method with Rate of Convergence O(1/t) for Variational Inequalities with Lipschitz Continuous Monotone Operators and Smooth Convex-Concave Saddle Point Problems. 2004. SIAM J. Optim. 15(1):229--251.

https://www2.isye.gatech.edu/~nemirovs/SIOPT_MP_2004.pdf

[5] Wendao Wu; Cong Fang. Randomized Matvec Lower Bounds for Simplex-Based Matrix Games. 2026. arXiv:2610.02095v2, 2026-10-19.

https://arxiv.org/pdf/2610.02095v2
