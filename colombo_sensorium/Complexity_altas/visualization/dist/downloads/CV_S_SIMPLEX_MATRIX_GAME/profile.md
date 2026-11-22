# Simplex matrix games with two-sided matrix-vector products

**Setting ID.** `CV_S_SIMPLEX_MATRIX_GAME`

Saddle-point problems

Normalized simplex-simplex matrix games with separate deterministic-risk and randomized-accuracy views. The randomized view has proved singleton-side 0/1 thresholds and explicit remaining gaps; the source adaptive-core claim is not promoted to an accepted lower bound. A full-domain KOS v3 upper is combined with exact reconstruction under the randomized target quantity.

**Status.** Polynomial gap present; Bounds missing

**Gap classes present.** Polynomial gap; Other quantified gap; Logarithmic gap

**TASK tags.** formulation: Simplex matrix zero sum game; solution concept: Fixed budget saddle gap; task family: Matrix computation; task family: Minimax; task family: Saddle point

**MODEL tags.** geometry: Compact geometry; geometry: Simplex simplex

**ORACLE tags.** feedback quality: Exact; interface family: Two sided real queries; operation: Two sided matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

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

$D$: Maximum dimension for the randomized accuracy view **Domain:** Positive integer.

$D=\max\{m,n\}$

$k_D$: Uniform random subset size for the exact 2/3-confidence endpoint **Domain:** Positive integer.

$k_D=\lceil2D/3\rceil$

$\tau_D$: Exact zero-query threshold when one strategy simplex is a singleton; a necessary threshold in general **Domain:** Nonnegative real number.

$\tau_D=2-2/k_D$

$\eta$: Public target accuracy used to run the KOS witness; clamping avoids nonpositive precision logarithms. **Domain:** Real number in (0,1/2].

$\eta=\min\{\varepsilon,1/2\}$

$\ell_{\mathrm{KOS}}$: Positive dimension and precision logarithm dominating the polylogarithmic factors in KOS v3. **Domain:** Positive real number.

$\ell_{\mathrm{KOS}}=1+\log(2mn/\eta)$

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

### R4 - Certified zero-query region

**Region.** $m,n\ge1$, $\varepsilon>0$, and either $\varepsilon\ge u_D$ or $(\min\{m,n\}=1\ \text{and}\ \varepsilon\ge\tau_D)$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

**Views.** Randomized accuracy

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B14

$$
0
$$

**Upper bound.** B12, B13

$$
0
$$

**Gap or comparison.** Exact zero on this union; no general two-sided necessity is claimed.

**Comparison argument.** Use uniform strategies on the u_D branch or a randomized subset on the singleton-side branch. Both witnesses have exact zero cost.

### R5 - Exact one-query singleton-side regime

**Region.** $\min\{m,n\}=1$, $D\ge2$, and $0<\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

**Views.** Randomized accuracy

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B15

$$
1
$$

**Upper bound.** B16

$$
1
$$

**Gap or comparison.** Exact one query; equality epsilon=tau_D belongs to the zero side.

**Comparison argument.** The hidden-coordinate lower matches one-call reconstruction.

### R6 - High-dimensional source window with a proved elementary lower

**Region.** $0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}/\log^{1/3}(1/\varepsilon)$, $m,n\ge4q$. Additionally $\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

**Views.** Randomized accuracy

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Polynomial gap

**Lower bound.** B15

$$
1
$$

**Upper bound.** B17, B11

$$
\min\{\min(m,n),\widetilde O(\varepsilon^{-2/3})\}
$$

**Gap or comparison.** At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

**Comparison argument.** The new complete KOS v3-to-q2 proof gives a deterministic pathwise cap in every positive dimension, independent of the source lower-bound window H. Take the minimum with the separately proved q2 basis-reconstruction cap. Explicitly the integer envelope is min{min(m,n),ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS))}. The displayed tilde form is valid on this row because 0<epsilon<2; eta=min{epsilon,1/2}. This changes only the upper side and leaves all lower exclusions and endpoint predicates intact.

### R7 - Other certified positive-cost two-sided dimensions

**Region.** $\min\{m,n\}\ge2$, $0<\varepsilon<\tau_D$, and not the original high-dimensional source-window H. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

**Views.** Randomized accuracy

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Polynomial gap

**Lower bound.** B15

$$
1
$$

**Upper bound.** B17, B11

$$
\min\{\min(m,n),\widetilde O(\varepsilon^{-2/3})\}
$$

**Gap or comparison.** At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

**Comparison argument.** The new complete KOS v3-to-q2 proof gives a deterministic pathwise cap in every positive dimension, independent of the source lower-bound window H. Take the minimum with the separately proved q2 basis-reconstruction cap. Explicitly the integer envelope is min{min(m,n),ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS))}. The displayed tilde form is valid on this row because 0<epsilon<2; eta=min{epsilon,1/2}. This changes only the upper side and leaves all lower exclusions and endpoint predicates intact.

### R8 - Unclosed randomized zero-query transition

**Region.** $\min\{m,n\}\ge2$ and $\tau_D\le\varepsilon<u_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

**Views.** Randomized accuracy

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B17, B11

$$
\min\{\min(m,n),\widetilde O(\varepsilon^{-2/3})\}
$$

**Gap or comparison.** A positive lower or a matching zero-query construction is missing in this interval.

**Comparison argument.** The new complete KOS v3-to-q2 proof gives a deterministic pathwise cap in every positive dimension, independent of the source lower-bound window H. Take the minimum with the separately proved q2 basis-reconstruction cap. Explicitly the integer envelope is min{min(m,n),ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS))}. The displayed tilde form is valid on this row because 0<epsilon<2; eta=min{epsilon,1/2}. This changes only the upper side and leaves all lower exclusions and endpoint predicates intact.

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

**Conditions.** Source Section 8 explicitly leaves verification of the central adaptive proof unresolved. This record reports the source statement without claiming an independent verification of that proof.; 2026-11-22 source check still finds v2 as the latest discoverable version. Its Section 8 final paragraph retains the adaptive-core proof-verification qualification; the new local endpoint proofs do not resolve that argument.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [5](https://arxiv.org/pdf/2610.02095v2) Definition3.1; Theorem3.2; Corollary3.3; Lemma3.4; Section8

Randomized two-sided matvec lower statements in ball/simplex and simplex/simplex geometries.

Full-space query vectors, feasible pair output, full saddle gap, fixed cap and success2/3. Dimensions grow with epsilon and are explicit. Paper itself flags adaptive-core proof verification in Section8; theorem statement audit is NOT certification of that proof.

Paper 2610.02095v2 is already recorded in this existing profile: reference CV_SRC_MG_2610_02095 and the linked excluded lower-bound statement are present. This is a recorded source claim pending proof review, not a missing setting or missing bibliography entry.

Directly checked the versioned primary HTML on 2026-11-22: Section 8, final paragraph, explicitly retains an unresolved verification task for the adaptive core argument. This note neither identifies a proved error nor certifies the argument.

Pending review is scoped to lower bound CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b1. Keep lower_scope_type=not_certified, included_in_bracket=false, eligible_for_bracket=false and selected_in_regimes empty until the targeted proof dependency is resolved. Independently justified endpoints, existing upper bounds and deterministic comparisons retain their current status.

### B7 - Deterministic matrix-vector method of Karmarkar–O’Carroll–Sidford

**Admission.** Eligible evidence; not selected in the displayed bracket

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

**Admission.** Eligible evidence; not selected in the displayed bracket

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

Paper 2610.02095v2 is already recorded in this existing profile: reference CV_SRC_MG_2610_02095 and the linked excluded lower-bound statement are present. This is a recorded source claim pending proof review, not a missing setting or missing bibliography entry.

Directly checked the versioned primary HTML on 2026-11-22: Section 8, final paragraph, explicitly retains an unresolved verification task for the adaptive core argument. This note neither identifies a proved error nor certifies the argument.

Pending review is scoped to lower bound CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b1. Keep lower_scope_type=not_certified, included_in_bracket=false, eligible_for_bracket=false and selected_in_regimes empty until the targeted proof dependency is resolved. Independently justified endpoints, existing upper bounds and deterministic comparisons retain their current status.

### B9 - Return any publicly known feasible strategy

**Admission.** Eligible evidence; not selected in the displayed bracket

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

**Admission.** Eligible evidence; not selected in the displayed bracket

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

### B11 - Basis reconstruction and exact internal solution

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized accuracy

**Witness or lower-bound scope.** Deterministic witness

$$
\min\{m,n\}
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122

**Source location.**  section: Complete local proof CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122; theorem: Exact reconstruction under the target query budget

Analyst-derived argument is kept separate from published/preprint evidence.

### B12 - Public uniform strategies

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized accuracy

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_threshold_20261122

**Source location.**  section: Complete local proof CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_threshold_20261122; theorem: Uniform-strategy zero-query certificate

Analyst-derived argument is kept separate from published/preprint evidence.

### B13 - Uniform random subset of ceil(2D/3) coordinates

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized accuracy

**Witness or lower-bound scope.** Randomized witness

$$
0
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

**Source location.**  section: Complete local proof CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122; theorem: Hidden-coordinate lower and exact singleton-side threshold

Analyst-derived argument is kept separate from published/preprint evidence.

### B14 - Nonnegative query count

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized accuracy

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

**Source location.**  section: Complete local proof CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122; theorem: Hidden-coordinate lower and exact singleton-side threshold

Analyst-derived argument is kept separate from published/preprint evidence.

### B15 - Fixed hidden optimal-coordinate matrices

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized accuracy

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

**Source location.**  section: Complete local proof CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122; theorem: Hidden-coordinate lower and exact singleton-side threshold

Analyst-derived argument is kept separate from published/preprint evidence.

### B16 - One basis query reconstructs the vector game

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized accuracy

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122

**Source location.**  section: Complete local proof CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122; theorem: Exact reconstruction under the target query budget

Analyst-derived argument is kept separate from published/preprint evidence.

### B17 - KOS v3 Theorem 1.1 with accuracy clamping; exact reconstruction for singleton dimensions

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized accuracy

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

**Local argument.** CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_kos_full_target_20261122

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) section: Complete local proof CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_kos_full_target_20261122; theorem: Full-domain KOS-to-q2 transfer and integer envelope

The target transfer is distinct from the primary theorem and from the historical q1 source-scoped metric/resource record.

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) section: Section 1 (problem and oracle definition; Footnote 3) and Section 7.2 (proof of main results); theorem: Theorem 1.1; proof of Theorems 1.1 and 1.2; equations: (1)

The source explicitly counts matrix-vector products and hides only polylogarithmic factors in m,n,epsilon^(-1).

Primary HTML and the source main theorem definitions were re-read on 2026-11-22.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 3e7807d2111e275556db8c1b7031f8303fc1d28758e34a5975ddd667fc4cbe75

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

### Native proof: CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122

Native pointer: /proofs/3; canonical SHA-256: c86ea915aa5357af7e9ab2d54dbac878e5ac772dd14355dc6f7b5e5413784f7d

#### Native field: kind

Native pointer: /proofs/3/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 13a9577154ab0929dcd95d7d4296806c8dbfd60d3e6117102cf110b39645085d

Exact reconstruction under the target query budget

#### Native field: statement

Native pointer: /proofs/3/statement; canonical SHA-256: d9ae123439c10a3c25c338b5c1e48ef56238dbd55c024850a5f2c3186df3724f

The target randomized accuracy complexity is at most min(m,n).

#### Native field: proof

Native pointer: /proofs/3/proof; canonical SHA-256: 8979e58015e051c5b7064416e78f3f0335a09df942bfc0181d69b6503a8d01ed

If n<=m, query (e_j,0) for j=1,...,n; each bundled response contains the j-th column A e_j. If m<n, query (0,e_i) for i=1,...,m and read each row from A^T e_i. Each is a legal arbitrary-real-vector query and costs exactly one bundled call. The full matrix is then known. A saddle point exists by compact convex strategy sets and bilinearity; exact internal solution is uncharged in this oracle model. The returned feasible pair has gap zero on every instance and every execution, so it meets the target per-instance probability 2/3 for all positive tolerances with pathwise cap min(m,n). This is a direct derivation for q2, not an assertion that the legacy source-scoped q1 is definitionally the same quantity.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: evidence_refs

Native pointer: /proofs/3/evidence_refs; canonical SHA-256: d95da1138b1b9f38db9f41737dede41488c7d6bf9690f8e7c235e7d819531190

#### Native item 1

Native pointer: /proofs/3/evidence_refs/0; canonical SHA-256: a48ffc21f83f89fd1d1fb67df19c16e9b03d4130b8f886e11bd6939efcd3c6d0

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__e_target_reconstruction_20261122

#### Native field: verification_scope

Native pointer: /proofs/3/verification_scope; canonical SHA-256: 1350e56715be218d79afee65f34c86d25295364f8783734a58733c7ab14251ec

Complete proof of the stated local endpoint or transfer only; external source theorems are cited premises, not independently re-proved.

### Native proof: CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

Native pointer: /proofs/4; canonical SHA-256: 1c1f78fbcc97c5df871ca49da2c796372b45d180802e7de271774a35aeddfe48

#### Native field: kind

Native pointer: /proofs/4/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: ca0095034e066750e7963e5e46b89e7aa7023aad1d0909f5c2ed2e3796a45060

Hidden-coordinate lower and exact singleton-side threshold

#### Native field: statement

Native pointer: /proofs/4/statement; canonical SHA-256: 93d93080d00621704087518c67aff536231d5e29a4ea07208304092ce135305d

For D>=2 and epsilon<tau_D, N*>=1. If min(m,n)=1, N*=0 for epsilon>=tau_D and N*=1 below it; D=1 is always zero.

#### Native field: proof

Native pointer: /proofs/4/proof; canonical SHA-256: e9aa2d2cd807ab4f783c2a3c97191c32e633ecad37aade2f88e4dbc6de7b41ab

Let D=max(m,n) and k_D=ceil(2D/3). Suppose first n=D>=2. For each j in [n], take A^(j) with every row identical, entry -1 in column j and +1 elsewhere. The full gap of any output equals 2(1-x_j), independent of y. If epsilon<tau_D=2-2/k_D, success requires x_j>=1-epsilon/2>1/k_D. Since the coordinates of x sum to one, at most k_D-1 indices can satisfy this for any fixed output. For a zero-query randomized output, average success over these D fixed matrices is at most (k_D-1)/D<2/3. At least one fixed matrix therefore violates the required confidence. If m=D instead, use matrices with identical columns, entry +1 in the distinguished row and -1 elsewhere. The gap is 2(1-y_i), and the same argument applies. This is an indistinguishability proof for arbitrary private randomness, without any span restriction or finite-precision assumption.
If m=1, choose a uniformly random k_D-subset S of the n=D column coordinates and output its uniform distribution. Fix an arbitrary matrix and one minimizing coordinate j*. The chance that j* belongs to S is k_D/D>=2/3. Conditional on this event, the average loss in S minus its minimum is at most 2(k_D-1)/k_D=tau_D, since every entry lies in [-1,1]. Thus zero queries meet the target for epsilon>=tau_D, including equality. When n=1 use a uniformly random k_D-subset of the maximizing rows; conditional on containing a maximizing row, the maximum minus subset average has the same bound. Below tau_D, the proved one-query necessity and one-query exact reconstruction match. For D=1 the only strategy pair has gap zero, k_D=1 and tau_D=0, so all positive tolerances cost zero. The sufficiency argument requires one side to be a singleton. In general two-sided geometries only the lower for epsilon<tau_D is claimed; the region between tau_D and the deterministic uniform-strategy threshold remains unresolved here.

#### Native field: source_refs

Native pointer: /proofs/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: evidence_refs

Native pointer: /proofs/4/evidence_refs; canonical SHA-256: b783cb68f526315f6a8041d1417e5d202f62eca1969ff451883c2774888aba7a

#### Native item 1

Native pointer: /proofs/4/evidence_refs/0; canonical SHA-256: 1da85bda94704a3bd1e85dd7d3645eef9b6b4cbe5179c2a6a593107829d522f4

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__e_randomized_thin_threshold_20261122

#### Native field: verification_scope

Native pointer: /proofs/4/verification_scope; canonical SHA-256: 1350e56715be218d79afee65f34c86d25295364f8783734a58733c7ab14251ec

Complete proof of the stated local endpoint or transfer only; external source theorems are cited premises, not independently re-proved.

### Native proof: CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_threshold_20261122

Native pointer: /proofs/5; canonical SHA-256: ac70bc9dedf72419dd0ccdad8fb0abb633a6cd81b22779ca30debdfb33e8f106

#### Native field: kind

Native pointer: /proofs/5/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/5/title; canonical SHA-256: defe3b105dd7dfbd61c516e09331e1fd09e2ac2abe6d2c26c4c35c3288929341

Uniform-strategy zero-query certificate

#### Native field: statement

Native pointer: /proofs/5/statement; canonical SHA-256: 2a7f22dfa62f9fba84ce718a72bab0da818207213b547c2c4c03a58c1a27a27c

For all m,n>=1, uniform strategies have full gap at most u_D=2-2/D.

#### Native field: proof

Native pointer: /proofs/5/proof; canonical SHA-256: 44d0f92f2344f73526735c796d3e88e1f8227a2fb4d076e6682712cdb27c3d24

For x=(1/n)1 and y=(1/m)1, fix a maximizing row i and minimizing column j. Their difference is the inner product of A with e_i x^T-y e_j^T. The coefficient l1 norm is (1-1/n)+(1-1/m)+|1/n-1/m|=2-2/max(m,n). Since every matrix entry has magnitude at most one, this bounds the difference for every i,j and hence the full gap. The certificate is deterministic and valid for every matrix. This is a sufficient threshold in general; its optimality for arbitrary zero-query randomization is not asserted.

#### Native field: source_refs

Native pointer: /proofs/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: evidence_refs

Native pointer: /proofs/5/evidence_refs; canonical SHA-256: b6796c0d1734bee20593245b4037860cc80fc8eb51ff3fab04bdef0af866dd0f

#### Native item 1

Native pointer: /proofs/5/evidence_refs/0; canonical SHA-256: 9d515bfbfb4376d6daf3a5a908c2b8f66b0b9a0e5b25beb2eb9d8c1ee236abbc

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__e_uniform_threshold_20261122

#### Native field: verification_scope

Native pointer: /proofs/5/verification_scope; canonical SHA-256: 1350e56715be218d79afee65f34c86d25295364f8783734a58733c7ab14251ec

Complete proof of the stated local endpoint or transfer only; external source theorems are cited premises, not independently re-proved.

### Native proof: CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_kos_full_target_20261122

Native pointer: /proofs/6; canonical SHA-256: a38e7090d391fd2bf474a1dccd226a84cf64fcb3a4e0675b13572d8bdf1306ef

#### Native field: kind

Native pointer: /proofs/6/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/6/title; canonical SHA-256: 60f6e638b8f69a2e3d21ac003e0531ed173cf2ef2212cd3f1bfc9a808c945651

Full-domain KOS v3 witness transfer to the randomized target quantity

#### Native field: statement

Native pointer: /proofs/6/statement; canonical SHA-256: b51f375be1ffa6d46e6ce6bd5a231a7f8c3b57d7bf19e3ce2d59c3d535418a4a

For every positive integer m,n and every epsilon>0, the exact target q2 satisfies N*(epsilon)<=min{min(m,n),K_KOS}, where eta=min{epsilon,1/2}, ell_KOS=1+log(2mn/eta), and K_KOS=ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS)) for universal C_KOS>=1 and p_KOS>=0. No lower-bound dimension window is required.

#### Native field: proof

Native pointer: /proofs/6/proof; canonical SHA-256: f62148a6962773b7a8bc5cf54d7915b6ba9b2a4da950a393155e8609c6b1a863

Source premise: Karmarkar--O'Carroll--Sidford, arXiv:2601.02347v3, Theorem 1.1, states a deterministic algorithm for every normalized game of this type with tilde-O(eta^(-2/3)) matvecs. Section 1 defines an eta-solution by the complete saddle gap, and its oracle returns the pair (A^T y,Ax). Footnote 3 limits the hidden factors to polylogarithms in m,n,eta^(-1). The source's Section 7.2 proof establishes this theorem without a lower bound on dimension depending on eta.

Class/output/metric map: the source class X=Delta_n, Y=Delta_m and max_{i,j}|A_{ij}|<=1 is exactly the present normalized class. Its feasible output pair is a legal target output, and its max_y y^T A xhat - min_x yhat^T A x metric is the target complete gap. Run the theorem at eta=min{epsilon,1/2}. Since eta<=epsilon, its deterministic gap guarantee implies target success probability one, hence at least 2/3, for every fixed admissible matrix. This is a one-way deterministic-witness inclusion into the randomized algorithm class; it transfers no deterministic lower bound.

Oracle/cost map: the source pair query is a legal target query because the target allows arbitrary real x,y. One such source pair is answered by exactly one target bundled response (Ax,A^T y), with order exchanged internally if needed. A source implementation that requests one directional product can obtain it using one target call with the other vector zero and discard the extra response. If two directions are requested sequentially, charge the actual two calls; do not divide directional counts by two or merge adaptively dependent queries. Thus the source count is an upper bound on target calls, up to at most a fixed convention factor absorbed in C_KOS. Exact arithmetic, known-domain optimization, and computation from returned data are free in both query models. The source has a deterministic worst-case call bound, so its witness satisfies the target pathwise cap; there is no expectation-to-cap conversion.

Uniform integer budget: because m,n>=1 and 0<eta<=1/2, the positive quantity ell_KOS=1+log(2mn/eta) dominates 1, log m, log n and log(1/eta). The source tilde-O bound can therefore be bounded by C_KOS eta^(-2/3) ell_KOS^(p_KOS) for fixed universal C_KOS>=1 and p_KOS>=0, increasing the constant for finite endpoint ranges. Round upward to K_KOS. For m,n>=2 use the source algorithm. When min(m,n)=1, use the separately proved one-call exact reconstruction instead, which is no greater than K_KOS. This handles singleton dimensions without relying on an entropy bound with log(1)=0. The choice eta<=1/2 also handles epsilon>=1 and avoids a false vanishing logarithmic factor. All dimensions are finite and positive, and epsilon=0 is outside the native accuracy domain.

Envelope: independently, basis reconstruction costs at most min(m,n) and returns gap zero. Both witnesses are chosen using public dimensions and accuracy, so select the smaller of their public proved integer caps. This proves the displayed min bound directly for q2. The old q1 source-scoped resource record is not identified with q2, and the old narrow b2 record is not needed for the new envelope. On every nonzero comparison updated here, 0<epsilon<2; consequently epsilon/4<=eta<=epsilon and the same upper is written min{min(m,n),tilde-O(epsilon^(-2/3))}, with only the stated positive dimension/precision logarithms suppressed. Existing exact zero and exact one-query rows are sharper and remain selected unchanged. This proves only an upper bound; the separate claimed randomized growing lower remains excluded.

#### Native field: source_refs

Native pointer: /proofs/6/source_refs; canonical SHA-256: c9253033238d8e8851b7b0d25d2324124b0baa1afe30a95f2cdcd0003eea09ec

#### Native item 1

Native pointer: /proofs/6/source_refs/0; canonical SHA-256: e943536318ccb7c9310622727704c14d9634b8b2a9ebb06f646fbdad99afb067

CV_SRC_Karmarkar2026

#### Native field: premise_proof_refs

Native pointer: /proofs/6/premise_proof_refs; canonical SHA-256: 2b62a5043ac3076d16da7772653b1a2af450fb3b0a2054ca5dab4eef1eb790f7

#### Native item 1

Native pointer: /proofs/6/premise_proof_refs/0; canonical SHA-256: da1cda2218c0bed86ba6783759ca5c83bf560387c1269bddcaa12cc4951aaae3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122

#### Native field: evidence_refs

Native pointer: /proofs/6/evidence_refs; canonical SHA-256: cd3a86ed046e10186308f060d7c1ed519b381cd44a7ce5605addb84b61e4e134

#### Native item 1

Native pointer: /proofs/6/evidence_refs/0; canonical SHA-256: 03f3df8790ada7b7f91fcfb298f21f39dbb0f92764e02160bd29a9fea9008876

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__e_kos_full_target_20261122

#### Native item 2

Native pointer: /proofs/6/evidence_refs/1; canonical SHA-256: 7f2740ba4cf45403fe3ee08241f6c95f33b91b2df1ce358e659c83becf649d0d

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__e_kos_v3_primary_20261122

#### Native field: verification_scope

Native pointer: /proofs/6/verification_scope; canonical SHA-256: 566037894c720ce56ab4354e4fe19e8d390758f38834d2346c7754448a2008b9

Complete class, output, guarantee and query-budget transfer; the KOS algorithmic theorem is a cited primary-source premise, not independently re-proved.

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: d8ead3b8a2518ba74f3ede6526dc1e4b03d20244522a7060f32b42ddf8be6661

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 18f3d736ef89ce50299de3209413d4dd98bf80aed1ccf7ee5592063430189e21

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

#### Native field: setting_id

Native pointer: /joint_analysis/target/setting_id; canonical SHA-256: f3c07771e252492ac22b3428a73c18189cd145519a7ee126adc5e637a3692524

CV_S_SIMPLEX_MATRIX_GAME

#### Native field: contract_policy

Native pointer: /joint_analysis/target/contract_policy; canonical SHA-256: d4543a64b2bd7b127c223768269eb08c7418c637909f6a10de4ec875e4531c2d

Original common specification and view guarantees retained.

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 01cd64dfdd15fe48633f4ff2f14162d6c15ff1c02aee14b872551478c4cc5eeb

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

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: f842c2ffa07dea1ac0f53f09fc2f055e10a1888816ed30c166f40edb8015920c

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 41b3a8a86e2cb239a1ba15a6229e3fb929a4b058c3b6bd39d0caa7d9017ca87d

Exact zero on this union; no general two-sided necessity is claimed.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 41b3a8a86e2cb239a1ba15a6229e3fb929a4b058c3b6bd39d0caa7d9017ca87d

Exact zero on this union; no general two-sided necessity is claimed.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: e433df791d42f01c356d17deb5768b68737977099d3d82e2f07eb7d6c687f00f

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: 328a08f3e7dde4854ce1a157261fdb3976bb6063fc867122dbb747e6a14ddcb8

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 9347774c748cae842cea3e0dfe4010f2a9f07294ccac131ceb87eec6922de352

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_uniform_zero_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 196c6122e53966f85256d603038b22d82e632d75f652c44a43d809de61c23bdd

$m,n\ge1$, $\varepsilon>0$, and either $\varepsilon\ge u_D$ or $(\min\{m,n\}=1\ \text{and}\ \varepsilon\ge\tau_D)$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 196c6122e53966f85256d603038b22d82e632d75f652c44a43d809de61c23bdd

$m,n\ge1$, $\varepsilon>0$, and either $\varepsilon\ge u_D$ or $(\min\{m,n\}=1\ \text{and}\ \varepsilon\ge\tau_D)$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 452fc4cf3882a94925a0493ec314bb65b329767d79e72292537c7e68c3cad38f

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 96f915266ce47a4c29e75eaff43e8aaf9cfb092d52268b9604e9344b59c48ef0

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 4804d43a2631cc19ad8892eca02277e4110685cef0e1e8c56c8d8c6aef6d317a

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 89a82855e57a36cb0562d6505da0bb6f53a54339f0fbefe905fe512b80c0c3c3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_randomized_zero_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: 196c6122e53966f85256d603038b22d82e632d75f652c44a43d809de61c23bdd

$m,n\ge1$, $\varepsilon>0$, and either $\varepsilon\ge u_D$ or $(\min\{m,n\}=1\ \text{and}\ \varepsilon\ge\tau_D)$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 196c6122e53966f85256d603038b22d82e632d75f652c44a43d809de61c23bdd

$m,n\ge1$, $\varepsilon>0$, and either $\varepsilon\ge u_D$ or $(\min\{m,n\}=1\ \text{and}\ \varepsilon\ge\tau_D)$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 6b72d8bea49b13615ee0941da39c4df49214eb9a874aba12bb3a51e10bfaac50

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: b72a5c5be102d35325bda1001d53ed808d86ab8f047546b7759c89e3c3e5b34c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 3d8e89da782afc87ff5b5a6c3943247f35ca234c76188ba1cd802b688bdb4834

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: 19552b9326018707547eedcb28610b6bc9e08cfc6b555b880fcb22037fabce97

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_zero_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 196c6122e53966f85256d603038b22d82e632d75f652c44a43d809de61c23bdd

$m,n\ge1$, $\varepsilon>0$, and either $\varepsilon\ge u_D$ or $(\min\{m,n\}=1\ \text{and}\ \varepsilon\ge\tau_D)$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 196c6122e53966f85256d603038b22d82e632d75f652c44a43d809de61c23bdd

$m,n\ge1$, $\varepsilon>0$, and either $\varepsilon\ge u_D$ or $(\min\{m,n\}=1\ \text{and}\ \varepsilon\ge\tau_D)$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 6b72d8bea49b13615ee0941da39c4df49214eb9a874aba12bb3a51e10bfaac50

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: b72a5c5be102d35325bda1001d53ed808d86ab8f047546b7759c89e3c3e5b34c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: a93bea6cea2fac7f73d3015211a166b0f39e688284cc807a7d9c8c675c3cb64f

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: a249c92d22bc7c38292489daf6c4f4281a877b8ffaa24408f7f3d79dc3564a8a

Exact one query; equality epsilon=tau_D belongs to the zero side.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: a249c92d22bc7c38292489daf6c4f4281a877b8ffaa24408f7f3d79dc3564a8a

Exact one query; equality epsilon=tau_D belongs to the zero side.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: 77a222cda5b12c4b1fc76dff6f4fa984fdfc2b7fb5be24837313fc811872b4a2

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: 2e5b5e510b256043f41a288857d259065313711110d6a559f35f52f266ca6725

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: 48be827b97443259a31aad074305ca2d31c8d7c393abf8fb5a950265c750a0f7

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_one_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: 3c46164d21b72a6f1a129b9b205afdcccd184b13afeb7bd069c9db179d1d1268

$\min\{m,n\}=1$, $D\ge2$, and $0<\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 3c46164d21b72a6f1a129b9b205afdcccd184b13afeb7bd069c9db179d1d1268

$\min\{m,n\}=1$, $D\ge2$, and $0<\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 2b62a5043ac3076d16da7772653b1a2af450fb3b0a2054ca5dab4eef1eb790f7

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: da1cda2218c0bed86ba6783759ca5c83bf560387c1269bddcaa12cc4951aaae3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: 9f57bd80bc49323ab8737a81302da9ab240d54c0ed45123a8ce1bcd20e214807

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: 1ce5aa9d949dd4006256f299820cec0cfdf20c13eebdda1e2865ea74569f46b3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_one_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: 3c46164d21b72a6f1a129b9b205afdcccd184b13afeb7bd069c9db179d1d1268

$\min\{m,n\}=1$, $D\ge2$, and $0<\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: 3c46164d21b72a6f1a129b9b205afdcccd184b13afeb7bd069c9db179d1d1268

$\min\{m,n\}=1$, $D\ge2$, and $0<\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 6b72d8bea49b13615ee0941da39c4df49214eb9a874aba12bb3a51e10bfaac50

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: b72a5c5be102d35325bda1001d53ed808d86ab8f047546b7759c89e3c3e5b34c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: c7db379d6061e838c34d546415d6028ddc89a568261dba4cb1f3f5b1a9bd4d62

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: d80100f23285d37a225ac848b5956a282d7300066d9f8a781565bfafd1483ebb

\min\{\min(m,n),\widetilde O(\varepsilon^{-2/3})\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: a504bd3c72c1b0b9cf94ce1932f39826b936e6c09f7cc8f73048287d2eae9a00

At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: a504bd3c72c1b0b9cf94ce1932f39826b936e6c09f7cc8f73048287d2eae9a00

At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: cc7e42a0ea6b043032ed196ab067315474c7b6e67db4b3c896dc874f72ee9b36

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: 025d283cd5989fbca29f0446c8d338e9425159f63311027f4fe8654cfc945f16

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: 9c392ae2b179f9879ef589303abec0a61fd70883336db6d68effb655931b48bd

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_kos_full_target_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: ac0dc455fd57e7ff0782b93550ae0dde0dfb4fd2a40320e74e24a955c285f99d

$0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}/\log^{1/3}(1/\varepsilon)$, $m,n\ge4q$. Additionally $\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: 82e3595955f587fd14a5c5cbe83c3c87683ede63d8ab2513cf27e466bd7e0ddf

All finite m,n>=1 and epsilon>0 in the normalized target class.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: 7da9452780da5b5b1226913418fb87be7539f46812bbe338dd82390147d9395f

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 8de4f945635da63ef7db52589f2a701e854d643d3af52d964ed23f6ba2f7fd7f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_kos_full_target_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: 711a78a507c542ef9f6dbc47c2e824a970c19332ea61949159d31184f0c4ea5e

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: bdbedfe3fbb2032f24dc2379c5942b1593834c8ab4ccdf5bf81ab8031b2fd416

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_target_reconstruction_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: ac0dc455fd57e7ff0782b93550ae0dde0dfb4fd2a40320e74e24a955c285f99d

$0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}/\log^{1/3}(1/\varepsilon)$, $m,n\ge4q$. Additionally $\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: 82e3595955f587fd14a5c5cbe83c3c87683ede63d8ab2513cf27e466bd7e0ddf

All finite m,n>=1 and epsilon>0 in the normalized target class.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: 2b62a5043ac3076d16da7772653b1a2af450fb3b0a2054ca5dab4eef1eb790f7

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: da1cda2218c0bed86ba6783759ca5c83bf560387c1269bddcaa12cc4951aaae3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: 4c9120a0dbc5bb3717f214ef86675de51670f62b0ad2056f0b6c24d972d86001

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: 1ce5aa9d949dd4006256f299820cec0cfdf20c13eebdda1e2865ea74569f46b3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_one_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: ac0dc455fd57e7ff0782b93550ae0dde0dfb4fd2a40320e74e24a955c285f99d

$0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}/\log^{1/3}(1/\varepsilon)$, $m,n\ge4q$. Additionally $\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: ac0dc455fd57e7ff0782b93550ae0dde0dfb4fd2a40320e74e24a955c285f99d

$0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}/\log^{1/3}(1/\varepsilon)$, $m,n\ge4q$. Additionally $\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: 6b72d8bea49b13615ee0941da39c4df49214eb9a874aba12bb3a51e10bfaac50

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: b72a5c5be102d35325bda1001d53ed808d86ab8f047546b7759c89e3c3e5b34c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: 555e344f66fc115756073f6463fae12773df3cff6c3ba3b50f1c64dc95fa961a

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/boundary_checks/1; canonical SHA-256: 440c776ccb74a92e922d6eefef6212961cf58eaa0deaf3cd735bc58c22e4394e

KOS accuracy is clamped to eta<=1/2; logarithms stay positive and caps are rounded upward. Singleton dimensions retain their exact zero/one rows.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 7

Native pointer: /joint_analysis/comparisons/6; canonical SHA-256: bc09232d3a7b6fe8c195175f5a4397ef831902a254256224d016e0dbc070b523

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/6/comparison_id; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/6/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/6/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/6/upper_envelope; canonical SHA-256: d80100f23285d37a225ac848b5956a282d7300066d9f8a781565bfafd1483ebb

\min\{\min(m,n),\widetilde O(\varepsilon^{-2/3})\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/6/lower_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native field: gap

Native pointer: /joint_analysis/comparisons/6/gap; canonical SHA-256: a504bd3c72c1b0b9cf94ce1932f39826b936e6c09f7cc8f73048287d2eae9a00

At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/6/remaining_gap; canonical SHA-256: a504bd3c72c1b0b9cf94ce1932f39826b936e6c09f7cc8f73048287d2eae9a00

At most the displayed min{dimension reconstruction,KOS} upper over the proved lower 1; no growing randomized lower has been certified here.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/6/bound_uses; canonical SHA-256: c5c3eb85854dc1d52f86eec82a191baa706299054799b8c5b467c804e921f409

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0; canonical SHA-256: 6b002620a2eb81bb3d4a092e06ff3963637e82fd136414a626660849c74b73b0

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/bound_id; canonical SHA-256: 9c392ae2b179f9879ef589303abec0a61fd70883336db6d68effb655931b48bd

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_kos_full_target_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/adopted_region; canonical SHA-256: d76225e0446fe53271af55abf50dd42834061584fe140715feeb404f5b33dece

$\min\{m,n\}\ge2$, $0<\varepsilon<\tau_D$, and not the original high-dimensional source-window H. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/validity_region; canonical SHA-256: 82e3595955f587fd14a5c5cbe83c3c87683ede63d8ab2513cf27e466bd7e0ddf

All finite m,n>=1 and epsilon>0 in the normalized target class.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs; canonical SHA-256: 7da9452780da5b5b1226913418fb87be7539f46812bbe338dd82390147d9395f

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 8de4f945635da63ef7db52589f2a701e854d643d3af52d964ed23f6ba2f7fd7f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_kos_full_target_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/1; canonical SHA-256: 41cf3b4f6b7d1c312060b5420f73336b569ac18b026e5b478735a7f3fb988154

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/bound_id; canonical SHA-256: bdbedfe3fbb2032f24dc2379c5942b1593834c8ab4ccdf5bf81ab8031b2fd416

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_target_reconstruction_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/adopted_region; canonical SHA-256: d76225e0446fe53271af55abf50dd42834061584fe140715feeb404f5b33dece

$\min\{m,n\}\ge2$, $0<\varepsilon<\tau_D$, and not the original high-dimensional source-window H. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/validity_region; canonical SHA-256: 82e3595955f587fd14a5c5cbe83c3c87683ede63d8ab2513cf27e466bd7e0ddf

All finite m,n>=1 and epsilon>0 in the normalized target class.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs; canonical SHA-256: 2b62a5043ac3076d16da7772653b1a2af450fb3b0a2054ca5dab4eef1eb790f7

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: da1cda2218c0bed86ba6783759ca5c83bf560387c1269bddcaa12cc4951aaae3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/bound_uses/2; canonical SHA-256: ee8572c639172f8825e0cdee21a8a4e4a00faa2c9eabece2e7e79b0ca8847e6e

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/bound_id; canonical SHA-256: 1ce5aa9d949dd4006256f299820cec0cfdf20c13eebdda1e2865ea74569f46b3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_one_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/adopted_region; canonical SHA-256: d76225e0446fe53271af55abf50dd42834061584fe140715feeb404f5b33dece

$\min\{m,n\}\ge2$, $0<\varepsilon<\tau_D$, and not the original high-dimensional source-window H. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/validity_region; canonical SHA-256: d76225e0446fe53271af55abf50dd42834061584fe140715feeb404f5b33dece

$\min\{m,n\}\ge2$, $0<\varepsilon<\tau_D$, and not the original high-dimensional source-window H. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs; canonical SHA-256: 6b72d8bea49b13615ee0941da39c4df49214eb9a874aba12bb3a51e10bfaac50

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: b72a5c5be102d35325bda1001d53ed808d86ab8f047546b7759c89e3c3e5b34c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/6/boundary_checks; canonical SHA-256: 555e344f66fc115756073f6463fae12773df3cff6c3ba3b50f1c64dc95fa961a

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/boundary_checks/1; canonical SHA-256: 440c776ccb74a92e922d6eefef6212961cf58eaa0deaf3cd735bc58c22e4394e

KOS accuracy is clamped to eta<=1/2; logarithms stay positive and caps are rounded upward. Singleton dimensions retain their exact zero/one rows.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/6/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/6/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 8

Native pointer: /joint_analysis/comparisons/7; canonical SHA-256: 04029a9ef45e84ff9d469ae19756afc7262787944b2f18e183e1141fdaa0ca04

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/7/comparison_id; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/7/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/7/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/7/upper_envelope; canonical SHA-256: d80100f23285d37a225ac848b5956a282d7300066d9f8a781565bfafd1483ebb

\min\{\min(m,n),\widetilde O(\varepsilon^{-2/3})\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/7/lower_envelope; canonical SHA-256: 12ae32cb1ec02d01eda3581b127c1fee3b0dc53572ed6baf239721a03d82e126

Native value (string): ""

#### Native field: gap

Native pointer: /joint_analysis/comparisons/7/gap; canonical SHA-256: 3954163f246a74c8aeaa3ce61d168dd725d6d93f3e9e315742f5b94258cd5557

A positive lower or a matching zero-query construction is missing in this interval.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/7/remaining_gap; canonical SHA-256: 3954163f246a74c8aeaa3ce61d168dd725d6d93f3e9e315742f5b94258cd5557

A positive lower or a matching zero-query construction is missing in this interval.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/7/bound_uses; canonical SHA-256: e4274f400e4543e3033333c09878e3a864dee88a3e9db6cf44dd0320560a4a62

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/0; canonical SHA-256: 8a7d8b8a77456ab1318fac2f3c7cd493f74164f4f1db1bcfde630d8c3bad8d40

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/bound_id; canonical SHA-256: 9c392ae2b179f9879ef589303abec0a61fd70883336db6d68effb655931b48bd

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_kos_full_target_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/adopted_region; canonical SHA-256: 61aaca4a825bd92c3eccbed58c9f6db50d37205e2a21d36a0f82a162d8d82c4e

$\min\{m,n\}\ge2$ and $\tau_D\le\varepsilon<u_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/validity_region; canonical SHA-256: 82e3595955f587fd14a5c5cbe83c3c87683ede63d8ab2513cf27e466bd7e0ddf

All finite m,n>=1 and epsilon>0 in the normalized target class.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/mapping_proof_refs; canonical SHA-256: 7da9452780da5b5b1226913418fb87be7539f46812bbe338dd82390147d9395f

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 8de4f945635da63ef7db52589f2a701e854d643d3af52d964ed23f6ba2f7fd7f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_kos_full_target_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/bound_uses/1; canonical SHA-256: 2a45fd8b16bdfb0fd9225b4ea67b44da11b6d207c2d416891d0d8b2a795ffb29

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/bound_id; canonical SHA-256: bdbedfe3fbb2032f24dc2379c5942b1593834c8ab4ccdf5bf81ab8031b2fd416

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_target_reconstruction_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/adopted_region; canonical SHA-256: 61aaca4a825bd92c3eccbed58c9f6db50d37205e2a21d36a0f82a162d8d82c4e

$\min\{m,n\}\ge2$ and $\tau_D\le\varepsilon<u_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/validity_region; canonical SHA-256: 82e3595955f587fd14a5c5cbe83c3c87683ede63d8ab2513cf27e466bd7e0ddf

All finite m,n>=1 and epsilon>0 in the normalized target class.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs; canonical SHA-256: 2b62a5043ac3076d16da7772653b1a2af450fb3b0a2054ca5dab4eef1eb790f7

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: da1cda2218c0bed86ba6783759ca5c83bf560387c1269bddcaa12cc4951aaae3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/reason; canonical SHA-256: cce27b902ffd494d217ff23198b60566ec22bbe014d919ac6f8ea750aff2047a

Same target q2, view, full-gap guarantee and fixed pathwise query cap; the full KOS upper has no lower-bound dimension guard.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/7/boundary_checks; canonical SHA-256: 555e344f66fc115756073f6463fae12773df3cff6c3ba3b50f1c64dc95fa961a

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/boundary_checks/1; canonical SHA-256: 440c776ccb74a92e922d6eefef6212961cf58eaa0deaf3cd735bc58c22e4394e

KOS accuracy is clamped to eta<=1/2; logarithms stay positive and caps are rounded upward. Singleton dimensions retain their exact zero/one rows.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/7/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/7/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 46d83667db13b479c195d420ab292a050ac28f615d1ed3c0fe9894a33d679b74

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: a8505e9572bc60ed7d34daafb6d7d3c1e9eb18f1a618ad45a87c64ee2a6a4ab5

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

Native pointer: /joint_analysis/domain_map/cells/5; canonical SHA-256: 85da5ecce909d23cdbc75e5e2360dd1b3cdb35d82be2ce1941c8ce4186fb3f0d

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/5/cell_id; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/5/predicate; canonical SHA-256: 196c6122e53966f85256d603038b22d82e632d75f652c44a43d809de61c23bdd

$m,n\ge1$, $\varepsilon>0$, and either $\varepsilon\ge u_D$ or $(\min\{m,n\}=1\ \text{and}\ \varepsilon\ge\tau_D)$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids; canonical SHA-256: 6862be6cb2709f7e763f3bab8c02b4f36b7e66119acc156675401767547942db

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids/0; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/5/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/5/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/5/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/5/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/5/note; canonical SHA-256: 7622ddd9bb81a47bae0952449f688ff0267743c52f8e61ca081276d76f82bed2

Use uniform strategies on the u_D branch or a randomized subset on the singleton-side branch. Both witnesses have exact zero cost.

#### Native item 7

Native pointer: /joint_analysis/domain_map/cells/6; canonical SHA-256: d80e6b20fcc0452d81265730b8fab534667e461001786806539797b5068252db

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/6/cell_id; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/6/predicate; canonical SHA-256: 3c46164d21b72a6f1a129b9b205afdcccd184b13afeb7bd069c9db179d1d1268

$\min\{m,n\}=1$, $D\ge2$, and $0<\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids; canonical SHA-256: a77605cd7ccc355b49434fa97072ff6a31f21a1f47bc502b287982a0fd0df7f4

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids/0; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/6/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/6/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/6/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/6/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/6/note; canonical SHA-256: 4929aef226f03f47baf3b83b6d826e4a9a5fd4b0b423029bee9ea92f99ba8421

The hidden-coordinate lower matches one-call reconstruction.

#### Native item 8

Native pointer: /joint_analysis/domain_map/cells/7; canonical SHA-256: f50a717cb253acb3d5b687513a274ccac1810123d2076a6336a694c6dab7b1b7

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/7/cell_id; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/7/predicate; canonical SHA-256: ac0dc455fd57e7ff0782b93550ae0dde0dfb4fd2a40320e74e24a955c285f99d

$0<\varepsilon\le\varepsilon_0$, $q\asymp\varepsilon^{-2/3}/\log^{1/3}(1/\varepsilon)$, $m,n\ge4q$. Additionally $\varepsilon<\tau_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids; canonical SHA-256: c7b31727f3f695adecde59f732dd44bc1382af0a3505ff5e6d3f8b36f65d90eb

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids/0; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/7/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/7/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/7/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/7/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/7/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/7/note; canonical SHA-256: 5449d4674df6113362cde822346485ef323635ee4094b7fe6be9e21655e7f546

The new complete KOS v3-to-q2 proof gives a deterministic pathwise cap in every positive dimension, independent of the source lower-bound window H. Take the minimum with the separately proved q2 basis-reconstruction cap. Explicitly the integer envelope is min{min(m,n),ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS))}. The displayed tilde form is valid on this row because 0<epsilon<2; eta=min{epsilon,1/2}. This changes only the upper side and leaves all lower exclusions and endpoint predicates intact.

#### Native item 9

Native pointer: /joint_analysis/domain_map/cells/8; canonical SHA-256: 2e03a309f667b2a54d71fe62f61e1fbe1e0be16448c5967774de35c4273bfcad

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/8/cell_id; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/8/predicate; canonical SHA-256: d76225e0446fe53271af55abf50dd42834061584fe140715feeb404f5b33dece

$\min\{m,n\}\ge2$, $0<\varepsilon<\tau_D$, and not the original high-dimensional source-window H. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/8/comparison_ids; canonical SHA-256: e5e26a2d8f02e347c1bd176bb9c03639e725c62605e095ee0b4937fd7cde95a8

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/8/comparison_ids/0; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/8/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/8/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/8/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/8/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/8/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/8/note; canonical SHA-256: 5449d4674df6113362cde822346485ef323635ee4094b7fe6be9e21655e7f546

The new complete KOS v3-to-q2 proof gives a deterministic pathwise cap in every positive dimension, independent of the source lower-bound window H. Take the minimum with the separately proved q2 basis-reconstruction cap. Explicitly the integer envelope is min{min(m,n),ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS))}. The displayed tilde form is valid on this row because 0<epsilon<2; eta=min{epsilon,1/2}. This changes only the upper side and leaves all lower exclusions and endpoint predicates intact.

#### Native item 10

Native pointer: /joint_analysis/domain_map/cells/9; canonical SHA-256: 2586107c3f7fea3e62d10807f8a23dba436785d9b2f04ccb23a61d8c1e328f84

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/9/cell_id; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/9/predicate; canonical SHA-256: 61aaca4a825bd92c3eccbed58c9f6db50d37205e2a21d36a0f82a162d8d82c4e

$\min\{m,n\}\ge2$ and $\tau_D\le\varepsilon<u_D$. $u_D=2-2/D$, $D=\max\{m,n\}$, $k_D=\lceil2D/3\rceil$, $\tau_D=2-2/k_D$.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids; canonical SHA-256: e11cfa11ef086ec3e08a86597fbc9cbab84ba18264fe9cd1d67d795fc6c93115

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids/0; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/9/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/9/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/9/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/9/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/9/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/9/note; canonical SHA-256: 5449d4674df6113362cde822346485ef323635ee4094b7fe6be9e21655e7f546

The new complete KOS v3-to-q2 proof gives a deterministic pathwise cap in every positive dimension, independent of the source lower-bound window H. Take the minimum with the separately proved q2 basis-reconstruction cap. Explicitly the integer envelope is min{min(m,n),ceil(C_KOS eta^(-2/3) ell_KOS^(p_KOS))}. The displayed tilde form is valid on this row because 0<epsilon<2; eta=min{epsilon,1/2}. This changes only the upper side and leaves all lower exclusions and endpoint predicates intact.

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: f273f801cb98974a718f4f6da00a71e334d80188bd37baff5821918ebb1c39fc

The deterministic risk view and its prior domain accounting remain separate. In randomized_accuracy: D=1 is zero; if min(m,n)=1, tau_D divides exact zero and one-query cells. For min(m,n)>=2, split epsilon>=u_D, tau_D<=epsilon<u_D, and epsilon<tau_D, then split the last cell by H. Since tau_D<=u_D, the primary randomized cells are disjoint and exhaustive. The legacy source-scoped q1 remains unselected; its identity is not merged with q2.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 972ea8a41362086708909ce378df98205a855f46924d80e1b28c5836b554c444

See explicitly marked missing-lower or retained deterministic residual cells.

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 66f067aa9f1fdba700ee89c036b869c4dc5000959b615af75ebc8b9454af6f87

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 23632acc9d5f02a655d68e1ae4b35110885917efee28cfca7b0b267bbd633f7a

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: d1885672fc9a8a4d0bd449bd342085285311cecb2effe479c82432d6cdc2291b

CV_S_SIMPLEX_MATRIX_GAME_mathematical_update_20261122

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 20a252d85246bc205a2fdad23d60da9ede1280fb86e487355d6bea8d2fb3f740

Add a complete randomized hidden-coordinate lower bound: N>=1 when epsilon<tau_D=2-2/ceil(2D/3). Prove the exact zero/one-query threshold for min(m,n)=1 using a randomized subset; when D=1, every positive accuracy requires zero queries. Retain the uniform zero-query region for general two-sided games and explicitly mark the interval between tau_D and u_D as missing_lower. Independently prove the q2 reconstruction upper bound. Preserve the original deterministic_risk comparisons and do not transfer their deterministic lower bounds to randomized algorithms. The main high-dimensional randomized window retains only the proved constant lower bound; the stronger source claim of order epsilon^(-2/3) remains excluded.

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 7170addc0845894342ab9774627877016aa836ef10ca8d5a029091bdb960f811

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/impact/0/comparison_ids/2; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/impact/0/comparison_ids/3; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native item 5

Native pointer: /joint_analysis/impact/0/comparison_ids/4; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 7381bb466f7ea8ea8243156bd1097dc106f6fbd37710e021cf34c93e34d99d93

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 4db96bd27013067417890597a1cf8cc345f71cb5049104a8a42172a5004396d3

CV_S_SIMPLEX_MATRIX_GAME_kos_full_target_20261122

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 0663e251644c0a2694b5a2aa4c953e4bf14c7cb36d807c28736671d8e98615fb

improvement

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 69ae467c4fd15634c53fbd5eca7249059adb5e24df218a719580f05f4a23fdab

Extend the certified KOS upper to all positive dimensions and accuracies under the target q2; select it with reconstruction outside H as well as inside H.

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: fa06eda9001b9248e3e71f96f938ccefb814c0a2eefa4a81784c02af1f939b13

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: d4cfc4ce4690a684d3ab5de683287d544a056d11b07d588ec6951765a3e2ded7

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 8181d2c860576d2794369f5228afc34d216faa6153ba8cc63c88b24cd94f4a5a

Verify the adaptive-core argument or locate a corrected source before adopting the claimed epsilon^(-2/3) randomized lower.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 7fe07e7359d60730a9f65692655516138854202a0457af42a4f97ddee9a3a237

Close the genuine dimension/accuracy gap above the elementary one-query lower.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: e3e9c935e76c639ca7d32d094e9c9b5acaabe1a53a617b606d574ca0dd7789bb

Resolve the two-sided randomized zero-query transition tau_D<=epsilon<u_D.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: dc20c8f4bd53974f7ead38f9a6c0ea9e74ce7b0ced77a48d01e639beaca7285e

Reconcile different deterministic resource-projection IDs by an explicit reviewed transfer before a consolidated strongest envelope is claimed; keep r1/r2 constants and extreme dimension logarithms explicit.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 9243e26e94e59999e1a877688ac54071b0a386a7b64440f043e5501a15701710

Assess compatible_candidates for CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1 and CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 1887c357506a2737a33e372677e39157c911a2688661903104d5c89df75b6b85

Assess compatible_candidates for CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2 and CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 6283663e8abfac2d55e84abad4981783248c1c34ce8cd0b9d63ebe87f4b5890e

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: bbb2bbff6f65e78d2e5bfee77aed8e08f768eed00395618b3f0ba24ebb05e81d

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

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/6; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/7; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: a3aa17b6da6e733fa184f8b9a56e8c65c62de1099b1377d4b87f41a6e6a6cde9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 400036feb72b7d6d9159c315f9096f9def3d1ba15a1d8f8087f88be02637810e

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 7170addc0845894342ab9774627877016aa836ef10ca8d5a029091bdb960f811

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/1; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/2; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/3; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/4; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 46360c23281ef67f9dd126a17b8607db3a54843118d6bd75f7041f641f12aced

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 7170addc0845894342ab9774627877016aa836ef10ca8d5a029091bdb960f811

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/1; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/2; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/3; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/4; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 803e4865aff0277ef7c473027081772d85ac2a964c11a9c089d51fe704a1811f

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 6c54e37233d5eaf6c35bbacbc94f2ca42aeb635e29e3d5660dd601dc9781188f

pending-20261122-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: e3e9c935e76c639ca7d32d094e9c9b5acaabe1a53a617b606d574ca0dd7789bb

Resolve the two-sided randomized zero-query transition tau_D<=epsilon<u_D.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 7170addc0845894342ab9774627877016aa836ef10ca8d5a029091bdb960f811

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/1; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/2; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/3; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/4; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 6359abfeb0056a3b989bc6b3c5cf507e5052940ce565d5a44fe6e1b20ec7be55

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 76133c8a4f70db7cde2f1df965265ee46901a1c240d1aab474ac03fcccb3bc14

pending-20261122-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: dc20c8f4bd53974f7ead38f9a6c0ea9e74ce7b0ced77a48d01e639beaca7285e

Reconcile different deterministic resource-projection IDs by an explicit reviewed transfer before a consolidated strongest envelope is claimed; keep r1/r2 constants and extreme dimension logarithms explicit.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 7170addc0845894342ab9774627877016aa836ef10ca8d5a029091bdb960f811

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/2; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/3; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/4; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 12765365dd894c667f703759b26d2963cb27ff96d40e340e258132d9531780ea

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: c96b9a83311385aff7047c91b3a6443135f0b4f349c602a377449aef6eed6f38

pending-20261122-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 9243e26e94e59999e1a877688ac54071b0a386a7b64440f043e5501a15701710

Assess compatible_candidates for CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c1 and CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 7170addc0845894342ab9774627877016aa836ef10ca8d5a029091bdb960f811

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/2; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/3; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/4; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 8cd3db48e040dd277cc0a8f1f08d7190a11d68de4fedfaaf3d550050fb830f15

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 628db5951a1f2f9656525d5519cf5518a562dbf2ac06fdf405a5d3afb919857b

pending-20261122-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 1887c357506a2737a33e372677e39157c911a2688661903104d5c89df75b6b85

Assess compatible_candidates for CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__c2 and CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b1, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b2, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b3, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b4, CV_S_SIMPLEX_MATRIX_GAME__deterministic_risk__b5

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 7170addc0845894342ab9774627877016aa836ef10ca8d5a029091bdb960f811

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 4cb19aa8b23e1400807d60352920324f84a936f12fb9cceadb75f4f1812d2c57

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 79b5d105f0a6b0457e4dc59a32c92ca1eedb6b6d10b1b7f4e6e14ab9b8aa4975

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_thin_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/2; canonical SHA-256: 5d290defc8f140ab3f5a9ae1a81a2206c843417c91f1a1a5d2e64d876655b740

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_hard_window_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/3; canonical SHA-256: 0511b75c5a239361f90a1f5c7e4e618f6854b981561f186dddedf7a6e85b8575

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_remaining_20261122

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/4; canonical SHA-256: cfa31ff545972a3f7fd11e7a55fef777f0bfa13c24979c8ae6b44d314231276f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__c_transition_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 9e723e776794e81baf07642a37bfd9909556bc6bc99797717cdaacbdd0ed5823

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 40f61d784d051d4ed059a39e555999eb5c84621ed7cf668832754f8fad5d22a2

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: bdbedfe3fbb2032f24dc2379c5942b1593834c8ab4ccdf5bf81ab8031b2fd416

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_target_reconstruction_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 2b62a5043ac3076d16da7772653b1a2af450fb3b0a2054ca5dab4eef1eb790f7

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: da1cda2218c0bed86ba6783759ca5c83bf560387c1269bddcaa12cc4951aaae3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: f44763f211165602d8f6629699c46c330a6a6cce267d0569d35c878a4edeb937

#### Native item 1

Native pointer: /joint_analysis/provenance/0/target_domain/0; canonical SHA-256: d6bd1e7355c14605120a810901de9d2cfee7ab87247bf690e9272a193ba3f7e3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__r_full_target_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 6165e3f90cde64845706dbb2e01416cf03f2cc158ceb27ca083d41baadf2e9b4

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 9347774c748cae842cea3e0dfe4010f2a9f07294ccac131ceb87eec6922de352

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_uniform_zero_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 452fc4cf3882a94925a0493ec314bb65b329767d79e72292537c7e68c3cad38f

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 96f915266ce47a4c29e75eaff43e8aaf9cfb092d52268b9604e9344b59c48ef0

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_uniform_threshold_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 8be28da7ba21a736968798b8ca026c3727a5b6c27aeca83b5058b0c1263854b5

#### Native item 1

Native pointer: /joint_analysis/provenance/1/target_domain/0; canonical SHA-256: c31efc75a2de3ce3f15287e7d1019991f88d0acfae04fec23cfbea90f10c6cdb

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__r_uniform_zero_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: f2172d47ddabe7ebcc3d0ffa2e0528f713cb51d7dc0b79ccd58ec4133693df94

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 89a82855e57a36cb0562d6505da0bb6f53a54339f0fbefe905fe512b80c0c3c3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_randomized_zero_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 6b72d8bea49b13615ee0941da39c4df49214eb9a874aba12bb3a51e10bfaac50

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: b72a5c5be102d35325bda1001d53ed808d86ab8f047546b7759c89e3c3e5b34c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 99c2a86f292d129be199d09f2036905978398801bc159cd62d96c8a65fcfaa33

#### Native item 1

Native pointer: /joint_analysis/provenance/2/target_domain/0; canonical SHA-256: 307db8cd18f139ec3afb664e31f59362dd2d142c703066884583c039f64aa5f3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__r_degenerate_zero_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 85668101c4c598fc4353fc6539f7292f21b3ef135b96a064f6c77a37fe061a5a

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: 19552b9326018707547eedcb28610b6bc9e08cfc6b555b880fcb22037fabce97

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_zero_lower_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 6b72d8bea49b13615ee0941da39c4df49214eb9a874aba12bb3a51e10bfaac50

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: b72a5c5be102d35325bda1001d53ed808d86ab8f047546b7759c89e3c3e5b34c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: f44763f211165602d8f6629699c46c330a6a6cce267d0569d35c878a4edeb937

#### Native item 1

Native pointer: /joint_analysis/provenance/3/target_domain/0; canonical SHA-256: d6bd1e7355c14605120a810901de9d2cfee7ab87247bf690e9272a193ba3f7e3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__r_full_target_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 8a11888cd7a43c53303ee4a6cf11ed7908c29253d24ff59984181c3dc0005be7

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: 1ce5aa9d949dd4006256f299820cec0cfdf20c13eebdda1e2865ea74569f46b3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_one_lower_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 6b72d8bea49b13615ee0941da39c4df49214eb9a874aba12bb3a51e10bfaac50

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: b72a5c5be102d35325bda1001d53ed808d86ab8f047546b7759c89e3c3e5b34c

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_randomized_thin_threshold_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 0b67f90dc19c35fcadab00903e7e19dfc71128c0629c9f7bc4fa19deea9943c5

#### Native item 1

Native pointer: /joint_analysis/provenance/4/target_domain/0; canonical SHA-256: 2fd5a61ef41e1da6d42ba558f2705c11d9f542604b378f7ae1f1a662ad869f07

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__r_positive_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: fc7bf32fc04caf4ddc10b60ace7b5881df4858f5b2edd2fa95939a9adf5feaa4

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: 48be827b97443259a31aad074305ca2d31c8d7c393abf8fb5a950265c750a0f7

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_one_upper_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 2b62a5043ac3076d16da7772653b1a2af450fb3b0a2054ca5dab4eef1eb790f7

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: da1cda2218c0bed86ba6783759ca5c83bf560387c1269bddcaa12cc4951aaae3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_target_reconstruction_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 4c7d077215e1c561075898264eae489adda4e6189b78d750b886f387b386dab0

#### Native item 1

Native pointer: /joint_analysis/provenance/5/target_domain/0; canonical SHA-256: dba51b44ff9c0855b1152f1b02583fa6f3a4e3a015aae27b1d213635697a6f2b

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__r_thin_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: 3429eff517fbf296bd71558c925b8662b0727caaacc7819cb63d1d71e6d4451a

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: 9c392ae2b179f9879ef589303abec0a61fd70883336db6d68effb655931b48bd

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__b_kos_full_target_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: f7a61f49ae5e60151d293133b29642f789e81e3d59dc194e683d14af3fdbef2b

source_theorem_with_analyst_transfer

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: c9253033238d8e8851b7b0d25d2324124b0baa1afe30a95f2cdcd0003eea09ec

#### Native item 1

Native pointer: /joint_analysis/provenance/6/source_refs/0; canonical SHA-256: e943536318ccb7c9310622727704c14d9634b8b2a9ebb06f646fbdad99afb067

CV_SRC_Karmarkar2026

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: 7da9452780da5b5b1226913418fb87be7539f46812bbe338dd82390147d9395f

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: 8de4f945635da63ef7db52589f2a701e854d643d3af52d964ed23f6ba2f7fd7f

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_kos_full_target_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: 8d0cf8cf772ecfcb274035e3b4c79399cc509b5e8c944e44f7dd9f61bf6489f4

KOS arXiv:2601.02347v3 Theorem 1.1: all normalized games; deterministic complete-gap algorithm.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: f44763f211165602d8f6629699c46c330a6a6cce267d0569d35c878a4edeb937

#### Native item 1

Native pointer: /joint_analysis/provenance/6/target_domain/0; canonical SHA-256: d6bd1e7355c14605120a810901de9d2cfee7ab87247bf690e9272a193ba3f7e3

CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__r_full_target_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: 6ac7c049d48965d8052556dc2653ddf8d7c41bcc1c86a7a3c93066a2b63b3760

Identity instance/output/gap; legal pair queries; deterministic pathwise cap; public accuracy clamp and singleton reconstruction.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: 81d1f1a824d1b535e157d7947b46d4f3940aae923bb8a2ae7525651e8b0f56d6

Section 1, Theorem 1.1, Footnote 3, Section 7.2 proof; https://arxiv.org/html/2601.02347v3

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
