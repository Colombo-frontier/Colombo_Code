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
\begin{aligned}&r_{\rm det}^{\star}(N;m,n)=\inf_{\substack{\mathcal A\in\mathfrak A_{\rm det}:\\ \sup_A N_{\rm matvec}(\mathcal A,A)\le N}}\\[4pt]&\sup_{A\in[-1,1]^{m\times n}}\bigl[\max_{v\in\Delta_m}v^{\mathsf T}A\widehat x-\min_{u\in\Delta_n}\widehat y^{\mathsf T}Au\bigr]\end{aligned}
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
\begin{aligned}&r_{\rm det}^{\star}(N;m,n)=\inf_{\substack{\mathcal A\in\mathfrak A_{\rm det}:\\ \sup_A N_{\rm matvec}(\mathcal A,A)\le N}}\\[4pt]&\sup_{A\in[-1,1]^{m\times n}}\bigl[\max_{v\in\Delta_m}v^{\mathsf T}A\widehat x-\min_{u\in\Delta_n}\widehat y^{\mathsf T}Au\bigr]\end{aligned}
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
\begin{aligned}&r_{\rm det}^{\star}(N;m,n)=\inf_{\substack{\mathcal A\in\mathfrak A_{\rm det}:\\ \sup_A N_{\rm matvec}(\mathcal A,A)\le N}}\\[4pt]&\sup_{A\in[-1,1]^{m\times n}}\bigl[\max_{v\in\Delta_m}v^{\mathsf T}A\widehat x-\min_{u\in\Delta_n}\widehat y^{\mathsf T}Au\bigr]\end{aligned}
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

**Local argument.** A1

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

**Local argument.** A2

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

**Local argument.** A3

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

**Local argument.** A4

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

**Local argument.** A6

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

**Local argument.** A5

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

**Local argument.** A5

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

**Local argument.** A5

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

**Local argument.** A4

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

**Local argument.** A7

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) section: Complete local proof CV_S_SIMPLEX_MATRIX_GAME__randomized_accuracy__proof_kos_full_target_20261122; theorem: Full-domain KOS-to-q2 transfer and integer envelope

The target transfer is distinct from the primary theorem and from the historical q1 source-scoped metric/resource record.

**Source location.** [1](https://arxiv.org/pdf/2601.02347v3) section: Section 1 (problem and oracle definition; Footnote 3) and Section 7.2 (proof of main results); theorem: Theorem 1.1; proof of Theorems 1.1 and 1.2; equations: (1)

The source explicitly counts matrix-vector products and hides only polylogarithmic factors in m,n,epsilon^(-1).

Primary HTML and the source main theorem definitions were re-read on 2026-11-22.

## 5. Local arguments

### A1 - Recover the matrix with basis queries, then solve the known linear program using uncharged internal computation.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

In each bundled two-sided query, set the unused input vector to zero. Standard basis queries recover all columns using the number of minimizing coordinates, or all rows using the number of maximizing coordinates. Choose the smaller direction for exactly $\min\{m,n\}$ calls. The complete payoff matrix is then known, and an exact equilibrium is obtainable by the allowed uncharged internal optimization. The saddle gap is zero. Transposing the matrix to the canonical row-maximizer convention only swaps the response blocks and does not change the call count.

### A2 - Return any public feasible strategy

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Under the declared matrix normalization and strategy domains, every feasible bilinear payoff lies in $[-1,1]$. The difference between its maximum against a fixed minimizing strategy and its minimum against a fixed maximizing strategy is therefore at most two. Return any publicly specified feasible strategy pair without querying. It meets every tolerance $\varepsilon\ge2$ deterministically. Nonnegativity of query cost certifies exact zero cost.

### A3 - Dimension-dependent zero-query saddle-gap guarantee

**Scope.** The randomized\_accuracy view, guarantee g1, target-accuracy quantity q2 and bundled exact two-sided call resource; m,n positive integers and epsilon>0.

Return x=(1/n,...,1/n) and y=(1/m,...,1/m) without information calls. For any row i and column j, (Ax)\_i-(A^T y)\_j = sum\_{k!=j} A\_{ik}/n - sum\_{l!=i} A\_{lj}/m + (1/n-1/m)A\_{ij}. The entry bound gives an upper bound (n-1)/n+(m-1)/m+|1/n-1/m| = 2-2/max(m,n). The full saddle gap is the maximum of these differences over i,j, so the same bound holds for every fixed admissible matrix. The output is feasible and deterministic, hence meets instancewise success probability at least 2/3 whenever epsilon>=2-2/max(m,n). It uses zero calls on every path. Nonnegativity of call cost implies N^\*(epsilon;m,n)=0 there. The non-strict inequalities include equality. If m=n=1 the threshold and gap are zero, so every allowed epsilon>0 qualifies. This proves a sufficient zero-cost region, not necessity of the threshold for randomized zero-query methods. All constants and inequalities are exact and uniform in m,n,epsilon.

### A4 - Exact reconstruction under the target query budget

The target randomized accuracy complexity is at most min(m,n).

If n<=m, query (e\_j,0) for j=1,...,n; each bundled response contains the j-th column A e\_j. If m<n, query (0,e\_i) for i=1,...,m and read each row from A^T e\_i. Each is a legal arbitrary-real-vector query and costs exactly one bundled call. The full matrix is then known. A saddle point exists by compact convex strategy sets and bilinearity; exact internal solution is uncharged in this oracle model. The returned feasible pair has gap zero on every instance and every execution, so it meets the target per-instance probability 2/3 for all positive tolerances with pathwise cap min(m,n). This is a direct derivation for q2, not an assertion that the legacy source-scoped q1 is definitionally the same quantity.

### A5 - Hidden-coordinate lower and exact singleton-side threshold

For D>=2 and epsilon<tau\_D, N\*>=1. If min(m,n)=1, N\*=0 for epsilon>=tau\_D and N\*=1 below it; D=1 is always zero.

Let D=max(m,n) and k\_D=ceil(2D/3). Suppose first n=D>=2. For each j in [n], take A^(j) with every row identical, entry -1 in column j and +1 elsewhere. The full gap of any output equals 2(1-x\_j), independent of y. If epsilon<tau\_D=2-2/k\_D, success requires x\_j>=1-epsilon/2>1/k\_D. Since the coordinates of x sum to one, at most k\_D-1 indices can satisfy this for any fixed output. For a zero-query randomized output, average success over these D fixed matrices is at most (k\_D-1)/D<2/3. At least one fixed matrix therefore violates the required confidence. If m=D instead, use matrices with identical columns, entry +1 in the distinguished row and -1 elsewhere. The gap is 2(1-y\_i), and the same argument applies. This is an indistinguishability proof for arbitrary private randomness, without any span restriction or finite-precision assumption.
If m=1, choose a uniformly random k\_D-subset S of the n=D column coordinates and output its uniform distribution. Fix an arbitrary matrix and one minimizing coordinate j\*. The chance that j\* belongs to S is k\_D/D>=2/3. Conditional on this event, the average loss in S minus its minimum is at most 2(k\_D-1)/k\_D=tau\_D, since every entry lies in [-1,1]. Thus zero queries meet the target for epsilon>=tau\_D, including equality. When n=1 use a uniformly random k\_D-subset of the maximizing rows; conditional on containing a maximizing row, the maximum minus subset average has the same bound. Below tau\_D, the proved one-query necessity and one-query exact reconstruction match. For D=1 the only strategy pair has gap zero, k\_D=1 and tau\_D=0, so all positive tolerances cost zero. The sufficiency argument requires one side to be a singleton. In general two-sided geometries only the lower for epsilon<tau\_D is claimed; the region between tau\_D and the deterministic uniform-strategy threshold remains unresolved here.

### A6 - Uniform-strategy zero-query certificate

For all m,n>=1, uniform strategies have full gap at most u\_D=2-2/D.

For x=(1/n)1 and y=(1/m)1, fix a maximizing row i and minimizing column j. Their difference is the inner product of A with e\_i x^T-y e\_j^T. The coefficient l1 norm is (1-1/n)+(1-1/m)+|1/n-1/m|=2-2/max(m,n). Since every matrix entry has magnitude at most one, this bounds the difference for every i,j and hence the full gap. The certificate is deterministic and valid for every matrix. This is a sufficient threshold in general; its optimality for arbitrary zero-query randomization is not asserted.

### A7 - Full-domain KOS v3 witness transfer to the randomized target quantity

For every positive integer m,n and every epsilon>0, the exact target q2 satisfies N\*(epsilon)<=min{min(m,n),K\_KOS}, where eta=min{epsilon,1/2}, ell\_KOS=1+log(2mn/eta), and K\_KOS=ceil(C\_KOS eta^(-2/3) ell\_KOS^(p\_KOS)) for universal C\_KOS>=1 and p\_KOS>=0. No lower-bound dimension window is required.

Source premise: Karmarkar--O'Carroll--Sidford, arXiv:2601.02347v3, Theorem 1.1, states a deterministic algorithm for every normalized game of this type with tilde-O(eta^(-2/3)) matvecs. Section 1 defines an eta-solution by the complete saddle gap, and its oracle returns the pair (A^T y,Ax). Footnote 3 limits the hidden factors to polylogarithms in m,n,eta^(-1). The source's Section 7.2 proof establishes this theorem without a lower bound on dimension depending on eta.

Class/output/metric map: the source class X=Delta\_n, Y=Delta\_m and max\_{i,j}|A\_{ij}|<=1 is exactly the present normalized class. Its feasible output pair is a legal target output, and its max\_y y^T A xhat - min\_x yhat^T A x metric is the target complete gap. Run the theorem at eta=min{epsilon,1/2}. Since eta<=epsilon, its deterministic gap guarantee implies target success probability one, hence at least 2/3, for every fixed admissible matrix. This is a one-way deterministic-witness inclusion into the randomized algorithm class; it transfers no deterministic lower bound.

Oracle/cost map: the source pair query is a legal target query because the target allows arbitrary real x,y. One such source pair is answered by exactly one target bundled response (Ax,A^T y), with order exchanged internally if needed. A source implementation that requests one directional product can obtain it using one target call with the other vector zero and discard the extra response. If two directions are requested sequentially, charge the actual two calls; do not divide directional counts by two or merge adaptively dependent queries. Thus the source count is an upper bound on target calls, up to at most a fixed convention factor absorbed in C\_KOS. Exact arithmetic, known-domain optimization, and computation from returned data are free in both query models. The source has a deterministic worst-case call bound, so its witness satisfies the target pathwise cap; there is no expectation-to-cap conversion.

Uniform integer budget: because m,n>=1 and 0<eta<=1/2, the positive quantity ell\_KOS=1+log(2mn/eta) dominates 1, log m, log n and log(1/eta). The source tilde-O bound can therefore be bounded by C\_KOS eta^(-2/3) ell\_KOS^(p\_KOS) for fixed universal C\_KOS>=1 and p\_KOS>=0, increasing the constant for finite endpoint ranges. Round upward to K\_KOS. For m,n>=2 use the source algorithm. When min(m,n)=1, use the separately proved one-call exact reconstruction instead, which is no greater than K\_KOS. This handles singleton dimensions without relying on an entropy bound with log(1)=0. The choice eta<=1/2 also handles epsilon>=1 and avoids a false vanishing logarithmic factor. All dimensions are finite and positive, and epsilon=0 is outside the native accuracy domain.

Envelope: independently, basis reconstruction costs at most min(m,n) and returns gap zero. Both witnesses are chosen using public dimensions and accuracy, so select the smaller of their public proved integer caps. This proves the displayed min bound directly for q2. The old q1 source-scoped resource record is not identified with q2, and the old narrow b2 record is not needed for the new envelope. On every nonzero comparison updated here, 0<epsilon<2; consequently epsilon/4<=eta<=epsilon and the same upper is written min{min(m,n),tilde-O(epsilon^(-2/3))}, with only the stated positive dimension/precision logarithms suppressed. Existing exact zero and exact one-query rows are sharper and remain selected unchanged. This proves only an upper bound; the separate claimed randomized growing lower remains excluded.

**Sources.** [1](https://arxiv.org/pdf/2601.02347v3)

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
