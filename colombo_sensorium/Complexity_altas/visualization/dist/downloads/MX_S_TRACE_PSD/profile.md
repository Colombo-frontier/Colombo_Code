# Positive semidefinite trace estimation with relative error

**Setting ID.** `MX_S_TRACE_PSD`

Matrix computation

Estimate $\tau=\operatorname{tr}(A)$.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Matrix trace; solution concept: Relative trace error; task family: Matrix computation

**MODEL tags.** spectral structure: Positive semidefinite; spectral structure: Real psd

**ORACLE tags.** feedback quality: Exact; interface family: Exact right matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; adaptivity: Nonadaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Scalar

**METRIC tags.** criterion: Relative trace error

**GUARANTEE tags.** confidence: Confidence parameter explicitly declared; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N right

## 1. Setting specification

### Task

Estimate $\tau=\operatorname{tr}(A)$.

### Admissible model

Assume $A=A^{\mathsf T}\succeq0$ and $A\in\mathbb{R}^{d\times d}$; the zero matrix is allowed.

### Oracle interface

The data $d,\varepsilon,\delta$ are public and $A$ is hidden. Any query $v\in\mathbb{R}^d$ returns exact $Av$. Responses have no sampling noise; randomized probes arise from the algorithm’s private randomness.

### Output

Return any real $\widehat\tau$, without an additional confidence interval or certificate.

### Loss or accuracy criterion

The success event is $|\widehat\tau-\tau|\le\varepsilon\tau$. For $\tau>0$ this corresponds to relative loss $|\widehat\tau-\tau|/\tau$; when $\tau=0$, require $\widehat\tau=0$. Positive semidefiniteness ensures $\tau\ge0$.

### Resource accounting

Count right products with single vectors only: $N=N_{\mathrm r}$. A block of width $q$ costs $q$ calls.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

#### Randomized adaptive

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using public inputs only. For every admissible input fixed before generation of the private seed, success probability over private randomness is at least $1-\delta$.

**Budget convention.** A fixed worst-case budget respected for every input and private seed.

#### Randomized nonadaptive

Randomization is allowed, but all query vectors must be chosen at once from public inputs and the private seed. Responses may be used only for final postprocessing and cannot alter the queries. No further span, internal-computation, storage, or communication restriction is imposed; parallel organization does not change per-column charging.

The algorithm is selected using public inputs only. For every admissible input fixed before generation of the private seed, success probability over private randomness is at least $1-\delta$.

**Budget convention.** A fixed worst-case budget respected for every input and private seed.

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$\varepsilon$: Absolute-error proportion relative to the nonnegative true trace **Domain:** $\varepsilon>0$.

$|\widehat\tau-\operatorname{tr}(A)|\le\varepsilon\operatorname{tr}(A)$

$\delta$: Allowed failure probability for each fixed admissible input **Domain:** $0<\delta<1/2$.

Success probability is at least $1-\delta$.

$A$: Hidden real symmetric positive semidefinite matrix, possibly zero **Domain:** $\mathbb R^{d\times d}$.

$\tau,\widehat\tau$: True trace and the estimator returned by the algorithm **Domain:** $\tau\ge0,\ \widehat\tau\in\mathbb R$.

$\tau=\operatorname{tr}(A)=\sum_{i=1}^d A_{ii}$

$n$: The hard-matrix order in the small-error embedding. **Domain:** An auxiliary proof quantity, distinct from the input dimension $d$.

$n=\min\{d,\lfloor1/(96\varepsilon)\rfloor\}\quad(0<\varepsilon\le1/384,\ d\ge4)$

$q$: Fixed query budget in the Wishart argument **Domain:** Auxiliary proof quantity only.

$0\le q\le n/2$

$G,W$: Standard Gaussian matrix and its Gram matrix in the Wishart argument **Domain:** $G,W\in\mathbb R^{n\times n}$.

$G_{ij}\stackrel{\mathrm{iid}}{\sim}\mathcal N(0,1),\quad W=G^{\mathsf T}G$

$\mathcal H$: Complete query history, including the private random seed, in the stated argument **Domain:** Sigma-algebra with respect to which the conditional distribution is defined.

$c(\mathcal H),Z,\nu$: The known trace contribution, independent residual trace, and residual degrees of freedom conditional on query history. **Domain:** An auxiliary quantity in the posterior lemma.

$\operatorname{tr}(W)\mid\mathcal H=c(\mathcal H)+Z,\quad Z\sim\chi^2_\nu,\quad\nu=(n-q)^2$

$\chi^2_\nu$: Distribution of the sum of squares of $\nu$ independent standard normal variables **Domain:** $\nu\in\mathbb N$.

$I_j,0_j$: Identity and zero matrices of order $j$ **Domain:** $\mathbb R^{j\times j}$.

$c,C$: Positive universal constants in the corresponding bound. Identically named constants in different theorems need not have the same value. **Domain:** Independent of the dimension, accuracy, and probability parameters tracked by this bound.

$\log$: Natural logarithm **Domain:** Positive real argument.

$\log x=\ln x$

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

$N,N_{\mathrm r}$: Single-vector query budget for exact right products Av. A block is charged by its column count. **Domain:** $\mathbb N_0$.

$N=N_{\mathrm r}$

$N^\star$: Minimum worst-case query budget attaining this profile's success guarantee **Domain:** $\mathbb N_0\cup\{+\infty\}$.

The quantity is $N^\star=\inf_{\mathcal A}\sup_{I,\omega}N_{\mathcal A}(I,\omega)$, where the infimum ranges over admissible algorithms satisfying this profile's success guarantee.

$\mathcal A,I,\omega$: The algorithm, fixed admissible input, and private algorithmic seed. **Domain:** Quantifiers for worst-case input and execution cost. Success probability is taken over ω.

$a_0$: Scale ratio in the two-scale construction for larger errors. **Domain:** A positive auxiliary proof parameter.

$a_0>(1+\varepsilon)/(1-\varepsilon)\quad(0<\varepsilon<1)$

$d_0(\varepsilon)$: Dimension threshold for the earlier nonadaptive lower bound in Hutch++, Lemmas 16–19 **Domain:** Positive integer-valued function of $\varepsilon$, determined by the source construction.

$d\ge d_0(\varepsilon)$

$c_0$: Accuracy crossover constant between the two hard constructions in the nonadaptive arbitrary-confidence lower bound **Domain:** Fixed universal positive constant.

$\varepsilon=c_0/\sqrt{\log(1/\delta)}$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Randomized adaptive

$$
N^\star(\varepsilon,\delta;d)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

#### Q2 - target accuracy cost

**View.** Randomized nonadaptive

$$
N^\star(\varepsilon,\delta;d)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - Basic arbitrary-confidence regime

**Region.** $d\ge1$, $0<\varepsilon<1$, $0<\delta<1/2$.

**Views.** Randomized adaptive

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries.

**Status.** Logarithmic gap

**Lower bound.** B13

$$
\Omega(\min\{d,1/\varepsilon\})
$$

**Upper bound.** B1, B2

$$
O(\min\{d,\sqrt{\log(1/\delta)}/\varepsilon+\log(1/\delta)\})
$$

**Gap or comparison.** $O(\sqrt{\log(1/\delta)}+\varepsilon\log(1/\delta))$, and therefore $O(\log(1/\delta))$; the dimension cap can reduce this ratio.

**Comparison argument.** The independent local proof MX_S_TRACE_PSD__proof_uniform_confidence_wishart converts the adaptive Wishart posterior into a success-probability lower bound. Its small-tolerance success ceiling is 5/12<1/2, so the lower bound applies to every 0<delta<1/2; zero-query indistinguishability covers small dimensions and larger nontrivial tolerances. This does not use a finite-bit lower bound or substitute mean-square error for probability. Retain the minimum of Hutch++ and deterministic reconstruction for the upper side. Writing L=log(1/delta), the envelope ratio is O(min{d,sqrt(L)/epsilon+L}/min{d,1/epsilon}), bounded by O(sqrt(L)+epsilon L), hence O(L). No sharp confidence-dependent lower rate is asserted.

### R2 - The complete nontrivial accuracy domain at fixed success probability.

**Region.** Require $d\ge1$, $0<\varepsilon<1$, and $\delta=1/10$. All dimensions are covered, including saturation by full reconstruction.

**Views.** Randomized adaptive; Randomized nonadaptive

**Quantity.** Q1; Q2

**Resource.** Number of right matrix-vector product queries

**Status.** Optimal

**Lower bound.** B3, B9

$$
\Omega(\min\{d,1/\varepsilon\})
$$

**Upper bound.** B1, B2, B6, B8

$$
O(\min\{d,1/\varepsilon\})
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** For fixed $\delta=1/10$, randomized trace estimation uses $O(1/\varepsilon)$ calls and deterministic reconstruction $d$. The explicit lower bound uses posterior anti-concentration for $0<\varepsilon\le1/384$ and two-scale zero-query indistinguishability for $1/384<\varepsilon<1$, giving the uniform bound $\Omega(\min\{d,1/\varepsilon\})$.

### R3 - Zero-query endpoint at coarse accuracy

**Region.** $d\ge1$, $\varepsilon\ge1$; $0<\delta<1/2$.

**Views.** Randomized adaptive; Randomized nonadaptive

**Quantity.** Q1; Q2

**Resource.** $N=N_{\mathrm{r}}$

**Status.** Optimal

**Lower bound.** B5, B12

$$
0
$$

**Upper bound.** B4, B11

$$
0
$$

**Gap or comparison.** The optimal query count is exactly $0$. No ratio with zero denominator is formed.

**Comparison argument.** Positive semidefiniteness gives $\tau\ge0$. When $\varepsilon\ge1$, outputting zero has error $\tau$, which is at most $\varepsilon\tau$. Since query counts are nonnegative, the optimum is exactly zero.

### R4 - Window of the earlier constant-success lower bound

**Region.** Assume $\delta=1/10$, $0<\varepsilon\le c$, and $d\ge d_0(\varepsilon)$. The quantity $d_0(\varepsilon)$ is the sufficient dimension threshold in Lemma 16 and Lemmas 17-19.

**Views.** Randomized nonadaptive

**Quantity.** Q2

**Resource.** Number of right matrix-vector product queries.

**Status.** Optimal

**Lower bound.** B7

$$
\Omega(1/\varepsilon)
$$

**Upper bound.** B6, B8

$$
O(1/\varepsilon)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** Use fixed δ and the source sufficient-dimension window. Matching for all d and δ does not follow automatically.

### R5 - Sufficiently large dimension regime for arbitrary confidence levels

**Region.** Assume $0<\delta\le e^{-4}$, $0<\varepsilon\le1/4$, and $d\ge C[\sqrt{\log(1/\delta)}/\varepsilon+\log(1/\delta)]$. The quantity $C$ is a sufficient universal dimension constant for both hard constructions.

**Views.** Randomized nonadaptive

**Quantity.** Q2

**Resource.** Number of right matrix-vector product queries

**Status.** Logarithmic gap

**Lower bound.** B10

$$
\Omega\!\left(\begin{cases}\sqrt{\log(1/\delta)}/\varepsilon,&\varepsilon\le c_0/\sqrt{\log(1/\delta)},\\\log(1/\delta)/\log\log(1/\delta),&\text{otherwise}.\end{cases}\right)
$$

**Upper bound.** B6, B8

$$
O\!\left(\frac{\sqrt{\log(1/\delta)}}{\varepsilon}+\log(1/\delta)\right)
$$

**Gap or comparison.** $O(\log\log(1/\delta))$

**Comparison argument.** In the first branch, the sampling upper-bound term $\log(1/\delta)$ is controlled by $\sqrt{\log(1/\delta)}/\varepsilon$, giving constant-factor matching. In the second branch, the upper bound is $O(\log(1/\delta))$ and the lower bound is $\Omega(\log(1/\delta)/\log\log(1/\delta))$. The overall ratio is $O(\log\log(1/\delta))$, subject to the stated branch conditions.

### R6 - Joint dimension, accuracy and confidence regime

**Region.** Integer d>=1, 0<epsilon<1, 0<delta<1/2.

**Views.** Randomized nonadaptive

**Quantity.** Q2

**Resource.** Number of right matrix-vector product queries.

**Status.** Logarithmic gap

**Lower bound.** B14, B10

$$
\Omega(\max\{\min\{d,1/\varepsilon\},F(\varepsilon,L)\text{ when }G\})
$$

**Upper bound.** B6, B8

$$
O(\min\{d,\sqrt{L}/\varepsilon+L\})
$$

**Gap or comparison.** O(min{d,U}/max{m,F when G}); O(1) for d<=1/epsilon. On G the first branch has O(1) ratio and the second O(log L); elsewhere the ratio is at most O(1+sqrt(L)+epsilon L).

**Comparison argument.** L=log(1/delta), m=min{d,1/epsilon}, U=sqrt(L)/epsilon+L. G is exactly native nonadaptive r4. Only on G use F=sqrt(L)/epsilon for epsilon<=c_0/sqrt(L), and F=L/log(L) otherwise; omit F outside G. The proof MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer establishes class inclusion, the guarded maximum, redundancy of older slice lower rates and endpoint checks. Old upper and confidence-dependent lower premises are retained conditionally. G is not asserted to be an intrinsic phase transition.

## 4. Bounds and supporting evidence

### B1 - Randomized adaptive Hutch++

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized adaptive

**Witness or lower-bound scope.** Randomized witness

$$
N\le C[\sqrt{\log(1/\delta)}/\varepsilon+\log(1/\delta)]
$$

**Sources.** [3](https://arxiv.org/pdf/2010.09649v5)

**Oracle correspondence.** Exact Av queries allow arbitrary randomized adaptive real vectors. All responses use the same fixed PSD matrix, and each vector costs one N_right call.

**Guarantee conversion.** For each fixed PSD matrix A, success probability is at least 1 − δ. Retain any fixed-δ or narrower-ε region of the bound. Mean-square error does not replace the high-probability target.

**Output rule.** Return a real scalar t_hat satisfying |t_hat-tr(A)|<=epsilon tr(A). For A=0, success requires t_hat=0.

**Resource conversion.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.**

$$
C[\sqrt{\log(1/\delta)}/\varepsilon+\log(1/\delta)]
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [3](https://arxiv.org/pdf/2010.09649v5) pdf pages: 2; section: main upper bound; theorem: Theorem 1

Each vector product costs one call. Apply the saturation min(d, algorithm budget).

### B2 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized adaptive

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Oracle correspondence.** Exact Av queries allow arbitrary randomized adaptive real vectors. All responses use the same fixed PSD matrix, and each vector costs one N_right call.

**Guarantee conversion.** For each fixed PSD matrix A, success probability is at least 1 − δ. Retain any fixed-δ or narrower-ε region of the bound. Mean-square error does not replace the high-probability target.

**Output rule.** Return a real scalar t_hat satisfying |t_hat-tr(A)|<=epsilon tr(A). For A=0, success requires t_hat=0.

**Resource conversion.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** d

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** Standard-basis queries reveal every matrix column.

**Local argument.** SIX_PROOF_7ed1f0347d6b

### B3 - standard Wishart posterior plus chi-square anti-concentration

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized adaptive

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c\min\{d,1/\varepsilon\}
$$

**Sources.** [2](https://arxiv.org/pdf/2402.09379v3) [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf)

**Conditions.** $d\ge1$, $0<\varepsilon<1$, $\delta=1/10$.

**Dimension conditions.** For all $d\ge1$. Use $n=\min\{d,\lfloor1/(96\varepsilon)\rfloor\}$ only in the proof branch $\varepsilon\le1/384$.

**Oracle correspondence.** Exact Av queries allow arbitrary randomized adaptive real vectors. All responses use the same fixed PSD matrix, and each vector costs one N_right call.

**Guarantee conversion.** The lower bound covers arbitrary randomized adaptive real-valued queries with success probability at least $2/3$. This view requires $0.9$. Restricting to nonadaptive algorithms only reduces the algorithm class, so the lower-bound transfer is valid.

**Output rule.** Return a real scalar t_hat satisfying |t_hat-tr(A)|<=epsilon tr(A). For A=0, success requires t_hat=0.

**Resource conversion.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge c\min\{d,1/\varepsilon\}
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** **Claim and scope.** For every integer $d\ge1$ and $0<\varepsilon<1$, any randomized adaptive exact matrix-vector algorithm with a fixed worst-case budget that guarantees
$$\Pr\bigl(|\widehat\tau-\operatorname{tr}(A)|\le\varepsilon\operatorname{tr}(A)\bigr)\ge2/3$$
for every real positive semidefinite matrix of order $d$ requires $\Omega(\min\{d,1/\varepsilon\})$ queries. Queries may be arbitrary real vectors and the output any measurable function of the transcript. This argument concerns constant success probability; it does not establish sharp dependence on arbitrary confidence levels.

**Posterior lemma.** Use Lemma 13 of Braverman, Hazan, Simchowitz, and Woodworth (2020), or the unnormalized formulation in Proposition 3 and Appendix B.1 of *Fixed-Sparsity Matrix Approximation* (arXiv:2402.09379v3). Let $W=G^{\mathsf T}G$, where $G\in\mathbb R^{n\times n}$ has independent standard Gaussian entries. After at most $q<n$ adaptive queries, include the private seed in the transcript $\mathcal H$. A transcript-measurable orthogonal basis expresses the conditional matrix as a known matrix plus the Gram matrix of an independent standard Gaussian block of size $(n-q)\times(n-q)$. Thus
$$\operatorname{tr}(W)\mid\mathcal H=c(\mathcal H)+Z,\qquad Z\sim\chi^2_{(n-q)^2},$$
where $Z$ is independent of the transcript. Remove the component in the previously queried subspace from a dependent query. If the algorithm stops early, extend the transcript to $q$ independent directions; its output remains measurable with respect to the extended transcript. This only provides additional information. For randomized algorithms, condition first on the independent private seed, apply the lemma, and then integrate. Adaptivity is preserved throughout.

**Hard distribution at small tolerance.** Assume $0<\varepsilon\le1/384$. For $d\ge4$, set $n=\min\{d,\lfloor1/(96\varepsilon)\rfloor\}$, so $n\ge4$, and let $A=\operatorname{diag}(W,0_{d-n})$. A query in dimension $d$ returns the $W$ product of its first $n$ coordinates and a zero tail, exactly simulating one query in dimension $n$. The matrix $A$ is positive semidefinite and $\mathbb E\operatorname{tr}(A)=n^2$.

**Anti-concentration.** Suppose $q\le n/2$. For $Z\sim\chi^2_\nu$ with $\nu\ge4$, the density is bounded by $1/\sqrt\nu$. Its maximum occurs at $\nu-2$; the standard Stirling lower bound for the Gamma function, with $a=\nu/2\ge2$, gives the bound $e(1-1/a)^{a-1}/(2\sqrt{2\pi a})\le1/\sqrt{2a}$. Here $\nu=(n-q)^2$, so the conditional trace density is at most $2/n$. Markov's inequality gives $\Pr(\operatorname{tr}(A)>4n^2)\le1/4$. On success and $\operatorname{tr}(A)\le4n^2$, the true trace lies in an interval of length $8\varepsilon n^2$ centered at the transcript-measurable estimate $\widehat\tau$. Integrating the conditional density yields
$$\Pr(\text{success})\le\frac14+(8\varepsilon n^2)\frac2n=\frac14+16\varepsilon n\le\frac5{12}<\frac23.$$
This contradicts success probability at least $2/3$ on every fixed input, which would imply average success at least $2/3$ under this admissible input distribution. Consequently the budget exceeds $n/2$, and $n$ is a universal constant multiple of $\min\{d,1/\varepsilon\}$.

**Small dimensions.** For $d<4$, the output distribution of a zero-query algorithm is independent of the matrix. The permitted relative-error intervals for $I_d$ and $2I_d$ are disjoint when $\varepsilon\le1/384$. Both success probabilities therefore cannot be at least $2/3$. One necessary query gives the required constant-factor lower bound.

**Remaining nontrivial tolerances.** Let $1/384<\varepsilon<1$ and take any $d\ge1$. Choose $a_0>(1+\varepsilon)/(1-\varepsilon)$. The acceptable output intervals for $I_d$ and $a_0I_d$ are
$$[(1-\varepsilon)d,(1+\varepsilon)d],\qquad [(1-\varepsilon)a_0d,(1+\varepsilon)a_0d],$$
and are disjoint. A zero-query algorithm has the same output distribution on both inputs, so its two success probabilities sum to at most $1$ and cannot both be at least $2/3$. The fixed budget is therefore at least $1$. Since $\min\{d,1/\varepsilon\}\le384$,
$$N\ge1\ge\frac1{384}\min\{d,1/\varepsilon\}.$$
Combining the constants gives the uniform lower bound $\Omega(\min\{d,1/\varepsilon\})$ for all $0<\varepsilon<1$. The scales of these inputs are neither revealed nor bounded, as required by the stated trace-estimation models.

**Transfers.** The bound applies to nonadaptive algorithms, a subclass of adaptive algorithms. Bounded integer-coordinate queries are likewise a subclass of arbitrary real queries. The lower bound also applies at success probability $0.9$, uniformly for $b_{\mathrm q}\ge0$. Together with the admissible Rademacher NA-Hutch++ upper bound and reconstruction in $d$ standard-basis queries, this yields $\Theta(\min\{d,1/\varepsilon\})$. This is an explicit consequence of the cited posterior lemma, rather than a trace-estimation theorem attributed directly to that source.

**Zero-query endpoint.** If $\varepsilon\ge1$, positive semidefiniteness implies $\operatorname{tr}(A)\ge0$, and the constant output $\widehat\tau=0$ satisfies
$$|\widehat\tau-\operatorname{tr}(A)|=\operatorname{tr}(A)\le\varepsilon\operatorname{tr}(A).$$
for every input. It works at every allowed confidence level, dimension, and integer query alphabet. Nonnegativity of query cost makes the optimum exactly $0$. The nontrivial-tolerance rate $\Theta(\min\{d,1/\varepsilon\})$ therefore does not extend to $\varepsilon\ge1$.

**Local argument.** SIX_PROOF_b3242221f506

**Source location.** [2](https://arxiv.org/pdf/2402.09379v3) pdf pages: 11; 22; 23; section: §3.1; Appendix B.1; theorem: Proposition 3; proof in Appendix B.1

FS Proposition 3 and Appendix B.1 state the unnormalized form of the same adaptive Wishart posterior. Conditional on the complete query transcript and independent private seed, the residual block remains an independent Wishart matrix.

**Source location.** [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf) pdf pages: 11; section: §3; theorem: Lemma 13; Appendix C.2

BH, Lemma 13 is the original adaptive Wishart-posterior lemma used by D10. Gaussian entries in the source have variance 1/d; deterministic scaling gives the standard-Gaussian form used here.

**Source location.** [2](https://arxiv.org/pdf/2402.09379v3) theorem: Proposition 3; Appendix B.1; report derivation MX_D10_REVIEWED_2026

The self-contained trace argument uses the original Wishart posterior for small errors. For 1/384 < epsilon < 1, it uses two positive semidefinite instances with different scales.

### B4 - Deterministically return zero.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized adaptive

**Witness or lower-bound scope.** Deterministic witness

$$
N\le0
$$

**Conditions.** $d\ge1$, $\varepsilon\ge1$; $0<\delta<1/2$.

**Guarantee conversion.** Deterministic success for every instance, satisfying the setting's probability requirement.

**Resource conversion.** No matrix-vector product is queried, and every resource count is zero.

**Constants.** No hidden constant

**Local argument.** SIX_PROOF_369230c34039

### B5 - Nonnegative query count

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized adaptive

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge0
$$

**Conditions.** $d\ge1$, $\varepsilon\ge1$; $0<\delta<1/2$.

**Guarantee conversion.** Deterministic success for every instance, satisfying the setting's probability requirement.

**Resource conversion.** No matrix-vector product is queried, and every resource count is zero.

**Constants.** No hidden constant

**Local argument.** SIX_PROOF_369230c34039

### B6 - Randomized nonadaptive NA-Hutch++

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized nonadaptive

**Witness or lower-bound scope.** Randomized witness

$$
N\le C[\sqrt{\log(1/\delta)}/\varepsilon+\log(1/\delta)]
$$

**Sources.** [4](https://proceedings.neurips.cc/paper/2021/file/c77bfda61a0204d445185053e6a9a8fe-Paper.pdf)

**Oracle correspondence.** Exact $Av$ responses. All real query vectors are fixed jointly from public parameters and the private seed before any response. Each vector costs one $N_{\mathrm{right}}$ call; blocks are charged by columns.

**Guarantee conversion.** For each fixed PSD matrix A, success probability is at least 1 − δ. Retain this bound’s δ, ε, and dimension window and its nonadaptivity restriction. The lower bound does not cover arbitrary adaptive algorithms.

**Output rule.** Return a real scalar $\widehat t$ with $|\widehat t-\operatorname{tr}(A)|\le\epsilon\operatorname{tr}(A)$. For the zero matrix, success requires output zero.

**Resource conversion.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.**

$$
C[\sqrt{\log(1/\delta)}/\varepsilon+\log(1/\delta)]
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [4](https://proceedings.neurips.cc/paper/2021/file/c77bfda61a0204d445185053e6a9a8fe-Paper.pdf) pdf pages: 3; 5; section: main upper bound; theorem: Theorem 1.1 / 3.1

Each vector product costs one call. Apply the saturation min(d, algorithm budget).

### B7 - An earlier lower bound for nonadaptive real queries.

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized nonadaptive

**Witness or lower-bound scope.** The stated restricted randomized class

$$
N\ge c/\varepsilon
$$

**Sources.** [3](https://arxiv.org/pdf/2010.09649v5)

**Dimension conditions.**

$$
d\ge d0(\varepsilon )
$$

**Oracle correspondence.** Exact $Av$ responses. All real query vectors are fixed jointly from public parameters and the private seed before any response. Each vector costs one $N_{\mathrm{right}}$ call; blocks are charged by columns.

**Guarantee conversion.** For each fixed PSD matrix A, success probability is at least 1 − δ. Retain this bound’s δ, ε, and dimension window and its nonadaptivity restriction. The lower bound does not cover arbitrary adaptive algorithms.

**Output rule.** Return a real scalar $\widehat t$ with $|\widehat t-\operatorname{tr}(A)|\le\epsilon\operatorname{tr}(A)$. For the zero matrix, success requires output zero.

**Resource conversion.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge c/\varepsilon
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [3](https://arxiv.org/pdf/2010.09649v5) pdf pages: 8; 21; 22; section: §4; Appendix B; theorem: Theorem 8; Lemmas 16–19

This is a nonadaptive real-query lower bound. The paper requires success probability greater than 3/4, which δ = 1/10 satisfies.

### B8 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized nonadaptive

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Oracle correspondence.** Exact $Av$ responses. All real query vectors are fixed jointly from public parameters and the private seed before any response. Each vector costs one $N_{\mathrm{right}}$ call; blocks are charged by columns.

**Guarantee conversion.** For each fixed PSD matrix A, success probability is at least 1 − δ. Retain this bound’s δ, ε, and dimension window and its nonadaptivity restriction. The lower bound does not cover arbitrary adaptive algorithms.

**Output rule.** Return a real scalar $\widehat t$ with $|\widehat t-\operatorname{tr}(A)|\le\epsilon\operatorname{tr}(A)$. For the zero matrix, success requires output zero.

**Resource conversion.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** d

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** Standard-basis queries reveal every matrix column.

**Local argument.** SIX_PROOF_7ed1f0347d6b

### B9 - standard Wishart posterior plus chi-square anti-concentration

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized nonadaptive

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c\min\{d,1/\varepsilon\}
$$

**Sources.** [2](https://arxiv.org/pdf/2402.09379v3) [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf)

**Conditions.** $d\ge1$, $0<\varepsilon<1$, $\delta=1/10$.

**Dimension conditions.** For all $d\ge1$. Use $n=\min\{d,\lfloor1/(96\varepsilon)\rfloor\}$ only in the proof branch $\varepsilon\le1/384$.

**Oracle correspondence.** The target interface permits strictly nonadaptive exact Av queries. The lower bound holds for the stronger class of arbitrary adaptive real-vector access and therefore also applies to this subclass. Upper-bound permissions are not enlarged.

**Guarantee conversion.** The lower bound covers arbitrary randomized adaptive real-valued queries with success probability at least $2/3$. This view requires $0.9$. Restricting to nonadaptive algorithms only reduces the algorithm class, so the lower-bound transfer is valid.

**Output rule.** Return a real scalar $\widehat t$ with $|\widehat t-\operatorname{tr}(A)|\le\epsilon\operatorname{tr}(A)$. For the zero matrix, success requires output zero.

**Resource conversion.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge c\min\{d,1/\varepsilon\}
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** **Claim and scope.** For every integer $d\ge1$ and $0<\varepsilon<1$, any randomized adaptive exact matrix-vector algorithm with a fixed worst-case budget that guarantees
$$\Pr\bigl(|\widehat\tau-\operatorname{tr}(A)|\le\varepsilon\operatorname{tr}(A)\bigr)\ge2/3$$
for every real positive semidefinite matrix of order $d$ requires $\Omega(\min\{d,1/\varepsilon\})$ queries. Queries may be arbitrary real vectors and the output any measurable function of the transcript. This argument concerns constant success probability; it does not establish sharp dependence on arbitrary confidence levels.

**Posterior lemma.** Use Lemma 13 of Braverman, Hazan, Simchowitz, and Woodworth (2020), or the unnormalized formulation in Proposition 3 and Appendix B.1 of *Fixed-Sparsity Matrix Approximation* (arXiv:2402.09379v3). Let $W=G^{\mathsf T}G$, where $G\in\mathbb R^{n\times n}$ has independent standard Gaussian entries. After at most $q<n$ adaptive queries, include the private seed in the transcript $\mathcal H$. A transcript-measurable orthogonal basis expresses the conditional matrix as a known matrix plus the Gram matrix of an independent standard Gaussian block of size $(n-q)\times(n-q)$. Thus
$$\operatorname{tr}(W)\mid\mathcal H=c(\mathcal H)+Z,\qquad Z\sim\chi^2_{(n-q)^2},$$
where $Z$ is independent of the transcript. Remove the component in the previously queried subspace from a dependent query. If the algorithm stops early, extend the transcript to $q$ independent directions; its output remains measurable with respect to the extended transcript. This only provides additional information. For randomized algorithms, condition first on the independent private seed, apply the lemma, and then integrate. Adaptivity is preserved throughout.

**Hard distribution at small tolerance.** Assume $0<\varepsilon\le1/384$. For $d\ge4$, set $n=\min\{d,\lfloor1/(96\varepsilon)\rfloor\}$, so $n\ge4$, and let $A=\operatorname{diag}(W,0_{d-n})$. A query in dimension $d$ returns the $W$ product of its first $n$ coordinates and a zero tail, exactly simulating one query in dimension $n$. The matrix $A$ is positive semidefinite and $\mathbb E\operatorname{tr}(A)=n^2$.

**Anti-concentration.** Suppose $q\le n/2$. For $Z\sim\chi^2_\nu$ with $\nu\ge4$, the density is bounded by $1/\sqrt\nu$. Its maximum occurs at $\nu-2$; the standard Stirling lower bound for the Gamma function, with $a=\nu/2\ge2$, gives the bound $e(1-1/a)^{a-1}/(2\sqrt{2\pi a})\le1/\sqrt{2a}$. Here $\nu=(n-q)^2$, so the conditional trace density is at most $2/n$. Markov's inequality gives $\Pr(\operatorname{tr}(A)>4n^2)\le1/4$. On success and $\operatorname{tr}(A)\le4n^2$, the true trace lies in an interval of length $8\varepsilon n^2$ centered at the transcript-measurable estimate $\widehat\tau$. Integrating the conditional density yields
$$\Pr(\text{success})\le\frac14+(8\varepsilon n^2)\frac2n=\frac14+16\varepsilon n\le\frac5{12}<\frac23.$$
This contradicts success probability at least $2/3$ on every fixed input, which would imply average success at least $2/3$ under this admissible input distribution. Consequently the budget exceeds $n/2$, and $n$ is a universal constant multiple of $\min\{d,1/\varepsilon\}$.

**Small dimensions.** For $d<4$, the output distribution of a zero-query algorithm is independent of the matrix. The permitted relative-error intervals for $I_d$ and $2I_d$ are disjoint when $\varepsilon\le1/384$. Both success probabilities therefore cannot be at least $2/3$. One necessary query gives the required constant-factor lower bound.

**Remaining nontrivial tolerances.** Let $1/384<\varepsilon<1$ and take any $d\ge1$. Choose $a_0>(1+\varepsilon)/(1-\varepsilon)$. The acceptable output intervals for $I_d$ and $a_0I_d$ are
$$[(1-\varepsilon)d,(1+\varepsilon)d],\qquad [(1-\varepsilon)a_0d,(1+\varepsilon)a_0d],$$
and are disjoint. A zero-query algorithm has the same output distribution on both inputs, so its two success probabilities sum to at most $1$ and cannot both be at least $2/3$. The fixed budget is therefore at least $1$. Since $\min\{d,1/\varepsilon\}\le384$,
$$N\ge1\ge\frac1{384}\min\{d,1/\varepsilon\}.$$
Combining the constants gives the uniform lower bound $\Omega(\min\{d,1/\varepsilon\})$ for all $0<\varepsilon<1$. The scales of these inputs are neither revealed nor bounded, as required by the stated trace-estimation models.

**Transfers.** The bound applies to nonadaptive algorithms, a subclass of adaptive algorithms. Bounded integer-coordinate queries are likewise a subclass of arbitrary real queries. The lower bound also applies at success probability $0.9$, uniformly for $b_{\mathrm q}\ge0$. Together with the admissible Rademacher NA-Hutch++ upper bound and reconstruction in $d$ standard-basis queries, this yields $\Theta(\min\{d,1/\varepsilon\})$. This is an explicit consequence of the cited posterior lemma, rather than a trace-estimation theorem attributed directly to that source.

**Zero-query endpoint.** If $\varepsilon\ge1$, positive semidefiniteness implies $\operatorname{tr}(A)\ge0$, and the constant output $\widehat\tau=0$ satisfies
$$|\widehat\tau-\operatorname{tr}(A)|=\operatorname{tr}(A)\le\varepsilon\operatorname{tr}(A).$$
for every input. It works at every allowed confidence level, dimension, and integer query alphabet. Nonnegativity of query cost makes the optimum exactly $0$. The nontrivial-tolerance rate $\Theta(\min\{d,1/\varepsilon\})$ therefore does not extend to $\varepsilon\ge1$.

**Local argument.** SIX_PROOF_b3242221f506

**Source location.** [2](https://arxiv.org/pdf/2402.09379v3) pdf pages: 11; 22; 23; section: §3.1; Appendix B.1; theorem: Proposition 3; proof in Appendix B.1

FS Proposition 3 and Appendix B.1 state the unnormalized form of the same adaptive Wishart posterior. Conditional on the complete query transcript and independent private seed, the residual block remains an independent Wishart matrix.

**Source location.** [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf) pdf pages: 11; section: Appendix C.2; theorem: Lemma 13

**Source location.** [2](https://arxiv.org/pdf/2402.09379v3) section: Appendix B.1; theorem: Proposition 3

### B10 - Hard family using nonadaptive Gaussian shifts and random rank-one perturbations

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized nonadaptive

**Witness or lower-bound scope.** The stated restricted randomized class

$$
N\ge c\begin{cases}\sqrt{\log(1/\delta)}/\varepsilon,&\varepsilon\le c_0/\sqrt{\log(1/\delta)},\\\log(1/\delta)/\log\log(1/\delta),&\varepsilon>c_0/\sqrt{\log(1/\delta)}.\end{cases}
$$

**Sources.** [4](https://proceedings.neurips.cc/paper/2021/file/c77bfda61a0204d445185053e6a9a8fe-Paper.pdf)

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

**Source location.** [4](https://proceedings.neurips.cc/paper/2021/file/c77bfda61a0204d445185053e6a9a8fe-Paper.pdf) theorem: Theorem 4.1; Theorems 4.2–4.3; Sections 4.1–4.2, PDF pp.6–7

The first construction requires dimension $\Theta(\sqrt{\log(1/\delta)}/\varepsilon)$ and $\varepsilon\le c/\sqrt{\log(1/\delta)}$. In the remaining region the second construction controls the target sum up to the stated iterated-logarithm factor. Retain all source threshold constants and choose a sufficiently large universal $C$.

### B11 - Deterministically return zero.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized nonadaptive

**Witness or lower-bound scope.** Deterministic witness

$$
N\le0
$$

**Conditions.** $d\ge1$, $\varepsilon\ge1$; $0<\delta<1/2$.

**Guarantee conversion.** Deterministic success for every instance, satisfying the setting's probability requirement.

**Resource conversion.** No matrix-vector product is queried, and every resource count is zero.

**Constants.** No hidden constant

**Local argument.** SIX_PROOF_369230c34039

### B12 - Nonnegative query count

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized nonadaptive

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge0
$$

**Conditions.** $d\ge1$, $\varepsilon\ge1$; $0<\delta<1/2$.

**Guarantee conversion.** Deterministic success for every instance, satisfying the setting's probability requirement.

**Resource conversion.** No matrix-vector product is queried, and every resource count is zero.

**Constants.** No hidden constant

**Local argument.** SIX_PROOF_369230c34039

### B13 - Adaptive Wishart posterior plus chi-square anti-concentration with success ceiling below one half

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized adaptive

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge\frac{1}{384}\min\{d,1/\varepsilon\}
$$

**Sources.** [2](https://arxiv.org/pdf/2402.09379v3)

**Conditions.** d>=1, 0<epsilon<1, 0<delta<1/2.

**Dimension conditions.** All integer dimensions d>=1. The embedded dimension n=min{d,floor(1/(96 epsilon))} is used only when d>=4 and epsilon<=1/384.

**Oracle correspondence.** One exact right product Av per query, with arbitrary real vectors. Embedding W as diag(W,0) simulates each query using one native W product; no additional oracle operation is used.

**Guarantee conversion.** The hard-distribution average success ceiling is 5/12 for the small-tolerance branch. Every target guarantee has success at least 1-delta>1/2, yielding a contradiction. Conditioning on the independent private seed covers randomized adaptive algorithms.

**Output rule.** Any real transcript-measurable trace estimate is allowed.

**Resource conversion.** N is the fixed worst-case number of right single-vector products for every input and private seed. A block costs its number of columns; internal arithmetic and postprocessing remain free.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge(1/384)\min\{d,1/\varepsilon\}
$$

**Constants.** The displayed constant 1/384 is universal and independent of d, epsilon, and delta.

**Local argument.** MX_S_TRACE_PSD__proof_uniform_confidence_wishart

**Source location.** [2](https://arxiv.org/pdf/2402.09379v3) pdf pages: 11; 22; 23; section: Section 3.1; Appendix B.1; theorem: Proposition 3; proof in Appendix B.1

Primary version: arXiv:2402.09379v3, revision dated 2024-03-26. Archived source SHA256 efb3338e536779388499ff92beee30a07154993989b2a743138f51d620d246c1. Decisive source_read ranges: [26800,31000) and [51800,59600).

The square specialization gives a transcript-measurable known matrix plus an independent (n-q)-by-(n-q) Gaussian Gram block after q adaptive directions. Known deterministic scaling accommodates normalized Gaussian conventions.

The source sparsity-approximation theorem is not asserted as a trace-estimation lower bound; the separate local proof supplies the probability bound, dimension embedding, private-seed conditioning, and endpoint cases.

### B14 - Cost-preserving inclusion of nonadaptive algorithms into adaptive algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized nonadaptive

**Witness or lower-bound scope.** The stated restricted randomized class

$$
N\ge\frac{1}{384}\min\{d,1/\varepsilon\}
$$

**Conditions.** Integer d>=1, 0<epsilon<1, 0<delta<1/2

**Dimension conditions.** All integer d>=1.

**Oracle correspondence.** Each preselected exact Av query is executed once, using no additional oracle capability.

**Guarantee conversion.** The simulator preserves every per-fixed-input success event and its probability; apply the retained adaptive lower uniformly in delta.

**Output rule.** Identical scalar output and relative-trace success event, including exact zero output on A=0.

**Resource conversion.** Identical fixed worst-case single-vector query count for every input and private seed; a block costs its columns.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** (1/384)*min{d,1/epsilon}

**Constants.** The displayed constant 1/384 is universal and independent of d, epsilon and delta.

**Derivation.** Complete conditional baseline derivation in MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer; no unseen external theorem is used.

**Local argument.** MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: e652ac54d304498b379b451d4f3eabdc8e18729a11695d425dedc12943c1f2ae

### Native proof: SIX_PROOF_7ed1f0347d6b

Native pointer: /proofs/0; canonical SHA-256: bb0af96cee5292670a15a1662b4f48f8dd6c8c4be52d24f39d26c668cf994c08

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 9d558506777cd0a83e9229d13285bfc19855c8b202ecc0a6df43a5a4c55004c3

Query all $d$ standard basis vectors, fixed before any response if nonadaptivity is required. These responses recover all columns. Summing their diagonal entries returns the exact trace. The argument applies to the stated matrix class, including zero trace, and uses $d$ right queries with deterministic success.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: de4aba6a5aececf2b87ac96892553f0760aa9b3853604f5860917f8145704881

Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

### Native proof: SIX_PROOF_b3242221f506

Native pointer: /proofs/1; canonical SHA-256: a5666d9149d2f0d8ad731cd9e890edbeeff4b0a53b3b1faf8fcbb069fc74005a

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 829031cb74a102ed98948ae4234f2ae0d111a259b503a585d197b1cbe11d9224

**Claim and scope.** For every integer $d\ge1$ and $0<\varepsilon<1$, any randomized adaptive exact matrix-vector algorithm with a fixed worst-case budget that guarantees
$$\Pr\bigl(|\widehat\tau-\operatorname{tr}(A)|\le\varepsilon\operatorname{tr}(A)\bigr)\ge2/3$$
for every real positive semidefinite matrix of order $d$ requires $\Omega(\min\{d,1/\varepsilon\})$ queries. Queries may be arbitrary real vectors and the output any measurable function of the transcript. This argument concerns constant success probability; it does not establish sharp dependence on arbitrary confidence levels.

**Posterior lemma.** Use Lemma 13 of Braverman, Hazan, Simchowitz, and Woodworth (2020), or the unnormalized formulation in Proposition 3 and Appendix B.1 of *Fixed-Sparsity Matrix Approximation* (arXiv:2402.09379v3). Let $W=G^{\mathsf T}G$, where $G\in\mathbb R^{n\times n}$ has independent standard Gaussian entries. After at most $q<n$ adaptive queries, include the private seed in the transcript $\mathcal H$. A transcript-measurable orthogonal basis expresses the conditional matrix as a known matrix plus the Gram matrix of an independent standard Gaussian block of size $(n-q)\times(n-q)$. Thus
$$\operatorname{tr}(W)\mid\mathcal H=c(\mathcal H)+Z,\qquad Z\sim\chi^2_{(n-q)^2},$$
where $Z$ is independent of the transcript. Remove the component in the previously queried subspace from a dependent query. If the algorithm stops early, extend the transcript to $q$ independent directions; its output remains measurable with respect to the extended transcript. This only provides additional information. For randomized algorithms, condition first on the independent private seed, apply the lemma, and then integrate. Adaptivity is preserved throughout.

**Hard distribution at small tolerance.** Assume $0<\varepsilon\le1/384$. For $d\ge4$, set $n=\min\{d,\lfloor1/(96\varepsilon)\rfloor\}$, so $n\ge4$, and let $A=\operatorname{diag}(W,0_{d-n})$. A query in dimension $d$ returns the $W$ product of its first $n$ coordinates and a zero tail, exactly simulating one query in dimension $n$. The matrix $A$ is positive semidefinite and $\mathbb E\operatorname{tr}(A)=n^2$.

**Anti-concentration.** Suppose $q\le n/2$. For $Z\sim\chi^2_\nu$ with $\nu\ge4$, the density is bounded by $1/\sqrt\nu$. Its maximum occurs at $\nu-2$; the standard Stirling lower bound for the Gamma function, with $a=\nu/2\ge2$, gives the bound $e(1-1/a)^{a-1}/(2\sqrt{2\pi a})\le1/\sqrt{2a}$. Here $\nu=(n-q)^2$, so the conditional trace density is at most $2/n$. Markov's inequality gives $\Pr(\operatorname{tr}(A)>4n^2)\le1/4$. On success and $\operatorname{tr}(A)\le4n^2$, the true trace lies in an interval of length $8\varepsilon n^2$ centered at the transcript-measurable estimate $\widehat\tau$. Integrating the conditional density yields
$$\Pr(\text{success})\le\frac14+(8\varepsilon n^2)\frac2n=\frac14+16\varepsilon n\le\frac5{12}<\frac23.$$
This contradicts success probability at least $2/3$ on every fixed input, which would imply average success at least $2/3$ under this admissible input distribution. Consequently the budget exceeds $n/2$, and $n$ is a universal constant multiple of $\min\{d,1/\varepsilon\}$.

**Small dimensions.** For $d<4$, the output distribution of a zero-query algorithm is independent of the matrix. The permitted relative-error intervals for $I_d$ and $2I_d$ are disjoint when $\varepsilon\le1/384$. Both success probabilities therefore cannot be at least $2/3$. One necessary query gives the required constant-factor lower bound.

**Remaining nontrivial tolerances.** Let $1/384<\varepsilon<1$ and take any $d\ge1$. Choose $a_0>(1+\varepsilon)/(1-\varepsilon)$. The acceptable output intervals for $I_d$ and $a_0I_d$ are
$$[(1-\varepsilon)d,(1+\varepsilon)d],\qquad [(1-\varepsilon)a_0d,(1+\varepsilon)a_0d],$$
and are disjoint. A zero-query algorithm has the same output distribution on both inputs, so its two success probabilities sum to at most $1$ and cannot both be at least $2/3$. The fixed budget is therefore at least $1$. Since $\min\{d,1/\varepsilon\}\le384$,
$$N\ge1\ge\frac1{384}\min\{d,1/\varepsilon\}.$$
Combining the constants gives the uniform lower bound $\Omega(\min\{d,1/\varepsilon\})$ for all $0<\varepsilon<1$. The scales of these inputs are neither revealed nor bounded, as required by the stated trace-estimation models.

**Transfers.** The bound applies to nonadaptive algorithms, a subclass of adaptive algorithms. Bounded integer-coordinate queries are likewise a subclass of arbitrary real queries. The lower bound also applies at success probability $0.9$, uniformly for $b_{\mathrm q}\ge0$. Together with the admissible Rademacher NA-Hutch++ upper bound and reconstruction in $d$ standard-basis queries, this yields $\Theta(\min\{d,1/\varepsilon\})$. This is an explicit consequence of the cited posterior lemma, rather than a trace-estimation theorem attributed directly to that source.

**Zero-query endpoint.** If $\varepsilon\ge1$, positive semidefiniteness implies $\operatorname{tr}(A)\ge0$, and the constant output $\widehat\tau=0$ satisfies
$$|\widehat\tau-\operatorname{tr}(A)|=\operatorname{tr}(A)\le\varepsilon\operatorname{tr}(A).$$
for every input. It works at every allowed confidence level, dimension, and integer query alphabet. Nonnegativity of query cost makes the optimum exactly $0$. The nontrivial-tolerance rate $\Theta(\min\{d,1/\varepsilon\})$ therefore does not extend to $\varepsilon\ge1$.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: ad9486d8ffa44d7d528fde185cc1a241de3dfb3991254375c6cb02fe722d4f28

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: fe2720c39605ebb591edb442844498d28d4ea50ef83279241cd33619181bcc9b

MX_SRC_FS

#### Native item 2

Native pointer: /proofs/1/source_refs/1; canonical SHA-256: fc8389352f8fe8aa765d983280ab1e22a9e1392914083a648f803c48ae870522

MX_SRC_BH

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: a9f288fbb6c9a12d6977d9764fb03675433e8b36de50e986e12d4c71942999bf

standard Wishart posterior plus chi-square anti-concentration

### Native proof: SIX_PROOF_369230c34039

Native pointer: /proofs/2; canonical SHA-256: 891c922be9532e347ad7098a4054d956e827cc36e2ffbc26429d2ad1b870be5e

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: c8b54f0bc2c539c7a6857a6ac91268134f242d3916a7d2d99ef832b940dd8048

For epsilon>=1, positive semidefiniteness gives tr(A)>=0, and the deterministic output zero satisfies |0-tr(A)|=tr(A)<=epsilon tr(A). No query is used. Since query cost is nonnegative, the optimum is exactly zero.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 1147c59d65c221de9986637fa89ebd98fdca702a8b9383275d585fa625464c1c

Deterministically return zero.

### Native proof: MX_S_TRACE_PSD__proof_uniform_confidence_wishart

Native pointer: /proofs/3; canonical SHA-256: d53440c5ae92d8938e60070893c939b7ab8ba8064c980ab1b2c25f44a49f9819

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: b7515a5fcf20d70b32eafb8fc6c82c0d7d354d288ff6d7148e2e9e0797633056

Use Proposition 3 of Amsel et al., arXiv:2402.09379v3, archived SHA256 efb3338e536779388499ff92beee30a07154993989b2a743138f51d620d246c1, PDF p.11 and Appendix B.1, pp.22–23; read character ranges [26800,31000) and [51800,59600). Only its adaptive Wishart posterior lemma is used. Let G have n-by-n independent standard normal entries and W=G^T G. Any deterministic normalization in the source can be removed by known scaling, preserving relative error and query count. Condition on the independent private seed. After q<n independent adaptive query directions, the conditional trace is c(H)+Z, where c(H) is transcript-measurable and Z is independent chi-square with (n-q)^2 degrees of freedom. Dependent query directions provide no new information and can be removed; an early-stopping transcript can be extended to q independent directions, only giving additional information.
For 0<epsilon<=1/384 and d>=4, set n=min{d,floor(1/(96 epsilon))}>=4 and A=diag(W,0). Each dimension-d query simulates one W query by taking its first n coordinates. Suppose the fixed budget q<=n/2. The density of chi-square_nu for nu>=4 is at most 1/sqrt(nu): writing a=nu/2, its maximum is (a-1)^(a-1) exp(-(a-1))/(2 Gamma(a)); the Stirling lower bound gives at most e/(2 sqrt(2 pi a))<=1/sqrt(2a). Thus the conditional trace density is at most 2/n. Since E trace(A)=n^2, Markov gives Pr(trace(A)>4n^2)<=1/4. On success with trace(A)<=4n^2, the true trace lies within 4 epsilon n^2 of the transcript-measurable output. Integrating the conditional density over that interval gives Pr(success)<=1/4+8 epsilon n^2(2/n)<=5/12. Integrating over the private seed preserves this bound. A per-input guarantee of 1-delta>1/2 would imply average success greater than 1/2 under this PSD input distribution, a contradiction. Hence q>n/2. Since floor(1/(96 epsilon))>=1/(192 epsilon), this implies q>=(1/384) min{d,1/epsilon}.
For any d>=1 and epsilon<1, a zero-query algorithm has the same output distribution on A=0 and A=I_d. Their successful output sets are {0} and [(1-epsilon)d,(1+epsilon)d], which are disjoint. Their success probabilities sum to at most one, contradicting both being at least 1-delta>1/2. Thus N>=1. If d<4, this gives N>=(1/384) min{d,1/epsilon}; if epsilon>1/384, it gives the same bound because min{d,1/epsilon}<384. Combining cases proves the claimed uniform lower bound. This establishes no growing dependence on log(1/delta). For epsilon>=1, the existing zero-output proof instead gives exact optimum zero.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: 97d79464ee7e5acfa8af1160ea6caa04621d73d16e0af4c8288d8337068d98d5

Randomized adaptive exact-real right-matvec trace estimation of every real PSD d-by-d matrix; d>=1, 0<epsilon<1, 0<delta<1/2; fixed worst-case query budget.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: 1662960571cf29476b13324157a82327772e7ecc0f5e0795a79f39c40bb89bac

#### Native item 1

Native pointer: /proofs/3/source_refs/0; canonical SHA-256: fe2720c39605ebb591edb442844498d28d4ea50ef83279241cd33619181bcc9b

MX_SRC_FS

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 965d7da307cdacfaae7b1f4d2495f0d64a0f8f06d39cef6d31ed881b14e0e834

Wishart anti-concentration uniformly for every delta below one half

### Native proof: MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

Native pointer: /proofs/4; canonical SHA-256: e686f0484d460e6e2a0418943ed854563d49c04af2801d6c1fefe7ae70fa4593

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: 4a8a28f7f6f15e749df25ea46c01fd3b75c7128b2c0a99339f44511cc65f14d7

Conditional premises: frozen /bounds/12, canonical hash 99191570a108dc5104236c31ea376e5016d1bbf81d98dea6f3c6129567dc949a, and /proofs/3, canonical hash d53440c5ae92d8938e60070893c939b7ab8ba8064c980ab1b2c25f44a49f9819, assert N_ad>=min{d,1/epsilon}/384 uniformly on the stated domain. These accepted premises are retained conditionally, not independently recertified. The complete native views, common specification, quantities and resource projections establish identical inputs, exact Av feedback, scalar relative-trace output, per-fixed-input probability and fixed worst-case single-vector query cost; only adaptivity differs.
Given any nonadaptive algorithm, an adaptive simulator samples the identical private seed, generates the same public-parameter-dependent query list, executes it in order without altering vectors from responses, and applies identical final postprocessing. Every fixed input and seed produces the same transcript, output and charged number of vector products. Blocks remain charged by columns. Thus N*_nonadaptive>=N*_adaptive pointwise in (d,epsilon,delta), proving the new nonadaptive lower with the unchanged constant 1/384. This is a directional comparison of distinct native quantities, not an identity merge. No external theorem, probability amplification or parameter substitution is introduced.
For the envelope retain native nonadaptive /bounds/5 and /bounds/7: upper O(min{d,U}), where L=log(1/delta), U=sqrt(L)/epsilon+L and m=min{d,1/epsilon}. Retain /bounds/9 only on its exact native G=/regimes/6: delta<=exp(-4), epsilon<=1/4 and d>=C*U. On G, F=sqrt(L)/epsilon if epsilon<=c_0/sqrt(L), and F=L/log(L) otherwise. The combined lower is Omega(max{m,F when G}), omitting F outside G. Since L>=4 on G, its first branch has F>=2m. In its second branch 1/epsilon<sqrt(L)/c_0 and log(L)<=sqrt(L), so F>=sqrt(L)>c_0*m. Hence the guarded lower is equivalently Omega(F) on G and Omega(m) elsewhere, with universal constants. The old /bounds/8 slice lower has the same m rate. On the /bounds/6 source window, its accepted inequality N*>=c_H/epsilon and reconstruction N*<=d imply d>=c_H/epsilon, whence m>=min{1,c_H}/epsilon. Thus that older lower is also redundant in asymptotic rate; exact constant dominance is not claimed.
For d<=1/epsilon the upper d and lower d/384 give Theta(d), uniformly in delta. At d=1 the positive lower and integer budget force one query, attained by reconstruction. On G's first branch, L<=c_0*sqrt(L)/epsilon implies U<=(1+c_0)F, so the gap is constant. In the second branch U<=(1+1/c_0)L, giving O(log L) gap. Outside G the ratio is O(min{d,U}/m), at most O(1+sqrt(L)+epsilon L). G is a sufficient source guard, not an intrinsic phase boundary; d~U is only an asymptotic crossover. epsilon=1 is excluded, and the retained endpoint comparisons give exact zero cost for epsilon>=1. Old populated comparisons are unchanged. Constant-success lower bounds also imply lower bounds for stronger success requirements, so newly registered coverage is not a claim of a novel rate for every newly displayed parameter tuple.

#### Native field: scope

Native pointer: /proofs/4/scope; canonical SHA-256: d1e44fd63fc5705e7b0db28289140053489ce08b7b1405912133cdaf744b980d

The fixed nonadaptive PSD relative-trace contract, with integer d>=1, 0<epsilon<1 and 0<delta<1/2.

#### Native field: source_refs

Native pointer: /proofs/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: 45bb0181c92fb1d68ab8dd3124a731a3c75965bd29cbef977d4fbb247001f561

Uniform-confidence adaptive-to-nonadaptive class transfer and guarded synthesis

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: e53961cbf7b3214030b0517551a2234cc917f8e34644cffb406501e25d5d299a

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: f43accdf77b26af07d4d875011097f4a56f157d95e6a80a04cb2dced5bd4108f

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 8322ceb5c79c3112aa42e58887fd5af5c84a1d0673b591fd9e6c9e097db46199

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: f07f721bd2eee2478c86829838979b469a6dbcd2d5363db1b35759a5e2dd657c

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 744d95d4b8b2af74a428b625912b363ee039f27baf1d7985b6dd7715ee470209

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 2f0156adff42ef581328cd85593ef712c41250e940cfea824a6148e65d28c754

MX_S_TRACE_PSD__randomized_adaptive__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 767ecc016badc49085670b5bec104481003f9657ff6f9700256f8a0142c6fd48

Conditionally retain the native Hutch++ upper branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 40b6eb4fe90a2fca0aeedbd6f6bc3fcd9f5720abeeca0b6b7c2855c32df33965

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 3e69e3715b7256da62149876e495f4a1e36b0c2bf45062c89176528b5b19951f

MX_S_TRACE_PSD__randomized_adaptive__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 637f2ab43967ab815a459128c928993adcef02c537259ea40c96c47769aac943

Conditionally retain reconstruction in d calls.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 58eeb3495541b264ea038585e248095275057e0b55ec4d548339d03be104f62d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 4412bdeae414db1f76d3b75d981614e1631fd25f38c812a8634c407269f6871e

MX_S_TRACE_PSD__randomized_adaptive__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: ee81f9a052d811d5bd1f6576bda669521e6fe09ef1a4c74f951c8996efb5c43a

Same lower rate on its slice as the selected uniform b6; no constant improvement asserted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: 5facb93fb33d2e945c2ab360bbfd57887b537cf5920c6b323e47c525716cee6c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: e078e74e3b7ba87947c418dc94710de8a32dda6d5533fb192015a96172654066

MX_S_TRACE_PSD__randomized_adaptive__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 2cc10fc75d25a8ab23ef4eb592772e9a63c7706cc6564fa05b231c5a0df8d349

Accuracy guard disjoint from B.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: dbc5c46280c17a4d585e1e6e3c3994ac77188a7aa7d20ac68fa5b6b741100221

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: ebfd4116c4045acbeaf84de067dff48ac014d1d84cce01052e4b9454af31389b

MX_S_TRACE_PSD__randomized_adaptive__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: 2cc10fc75d25a8ab23ef4eb592772e9a63c7706cc6564fa05b231c5a0df8d349

Accuracy guard disjoint from B.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/bound_uses/5; canonical SHA-256: 647a09be7873c0cbdcf26d386d1b0fdb5999aa28121de2cf0b390e9fd517b367

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/adopted_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/bound_id; canonical SHA-256: f8858599c91dbf01faa97c6b8afbb27c680441d29122d8e2e6ea7b8effe39622

MX_S_TRACE_PSD__randomized_adaptive__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/reason; canonical SHA-256: 0b4c00ec08796c5c9d38a00239369414e4671f80a09637a6407e7bb471e7fc48

Conditionally retain the accepted uniform-confidence lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: be0fe713105ff3da8146a70950e3b636d5eef3488f4db3826bc9c4491c8218be

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: ef38e16907e5e98833f5df3ac7bc9862812007efa5a1b0d4c610bc0551eddadf

For d<=1/epsilon, the retained envelopes match at Theta(d).

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: a838bc25f2a4b62c033e58dbd93e18d59fdd8fcab1fb4f21f96249b94125a561

d asymptotic to U is an upper-envelope crossover, not an exact minimax threshold.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 9c99df2b4037e870a4d56aedd896ec6e99b55169d31f26ee3f76ddf21345985b

epsilon=1 belongs to Z; epsilon=0 and delta=1/2 are excluded.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 154ee447def8330d2f7365302ff0d5d1e430cfe9fde8aa283ba81e3353419eb9

Retained O(min{d,U}/m), bounded by O(1+sqrt(L)+epsilon L).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 218ce7856d331569f8be5b8a809900c7466a707011a9cf3957650e62c99ee0a2

Omega(m)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: f00aa033ead1188ef1c4aa62aaeecd6a0f27c4d8d1683619fa6fba9a9e1556d0

Retained confidence-dependent gap; sharper confidence dependence is not resolved by this investigation.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 23e599f3f190cb50f18b1e85e408d995b9d212ad1bd57792a23b1c6fd8894711

O(min{d,U})

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: f609a4b2df7697d5e5697b2d278111f687b7ec2676b7822dd5bd2417f005b7f6

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 71a2fe2e8ba1862b386259fd52d91f423ea3035c406fbbaae18b7f9ace7ee24a

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: f5c3f29745b559ab6139e2338ffecaddf04beb11573f80cd7975ca071a0e0c42

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 2f0156adff42ef581328cd85593ef712c41250e940cfea824a6148e65d28c754

MX_S_TRACE_PSD__randomized_adaptive__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: c767afb990df9af2c301a0de5e2654c316c307dd50300df36600386236bf3e3d

Retain the upper bound restricted to fixed confidence.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: f0ee38d165b9cb79bf9c707797fcfce8fdd4060a3839f1afd718ec7dfebe891d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 3e69e3715b7256da62149876e495f4a1e36b0c2bf45062c89176528b5b19951f

MX_S_TRACE_PSD__randomized_adaptive__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: efc54ad29faf9cd43e37c8393f280e8d11ba35a7bed28e88ca25a7043cbfb40a

Retain the dimension cap.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: ee5da1d26a0228ab2bb0b3dfdba00a66432e4539875771b06c9043b4ca10fdd0

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 4412bdeae414db1f76d3b75d981614e1631fd25f38c812a8634c407269f6871e

MX_S_TRACE_PSD__randomized_adaptive__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 6f2f0a5f16853c5e26dfa5a523b049569e339bd6c7135567b66bde6dd718d245

Preserve the native selected constant-confidence lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: bd92456df47ef8772fff420fccd4a636a5184c6eca8d608894e66d36d24fb181

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: e078e74e3b7ba87947c418dc94710de8a32dda6d5533fb192015a96172654066

MX_S_TRACE_PSD__randomized_adaptive__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 03e49d33ac33585f016eb3ce82fbccf97561e58a7cab274621f1702349fb1155

Accuracy guard disjoint from S.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: ac39e985be956f5d386670205978b365f2303a52d76a970407dfcd32a29a0fbf

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: ebfd4116c4045acbeaf84de067dff48ac014d1d84cce01052e4b9454af31389b

MX_S_TRACE_PSD__randomized_adaptive__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 03e49d33ac33585f016eb3ce82fbccf97561e58a7cab274621f1702349fb1155

Accuracy guard disjoint from S.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: 8dd9fdb65bb5cfd93b0ba4fb5dbd970c2a6c55472d07aef35642858366f0ca3e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: f8858599c91dbf01faa97c6b8afbb27c680441d29122d8e2e6ea7b8effe39622

MX_S_TRACE_PSD__randomized_adaptive__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: ddb32bbe02c6638bcec3ba25d540b8bb8094a63b003ec0314e263d5bc4aa80b6

Redundant in rate with the retained selected lower on S.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 9f531fbe5146a34cfeedbaa5e720e279c983de004f4eae954fa5f019e2e3648e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: a1c55515dc13b4eaeb4ccaf203301bb52c846a15ff123db9e03f7a6aa1fc6fb0

This is a fixed-confidence slice, not a uniform-confidence conclusion.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 8601636be30755dbc3a8a225ed95085869c2d6fe0ffbd3c5624749021dfe8d27

Finite-dimensional saturation is retained; epsilon=1 is excluded.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: fe35e51a7ebedaacf183182a5d6be8680bae544a7c5047fd9d7cf7632890fafa

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/0; canonical SHA-256: b1b705fa457ecaac854a89b70946c31c0f55472fd6aab25af18c757cac7646e4

MX_S_TRACE_PSD_p_c8bdef7655

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 130c5e78cbaacb2af30fa4de81b23e8ae42f27df8cbbf58339b0ae17f4acc57b

O(1)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 218ce7856d331569f8be5b8a809900c7466a707011a9cf3957650e62c99ee0a2

Omega(m)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: c9473bc0604ac78f21cbbe6483d819b9ac22157333cdfbb8a0eae70cbd907b55

No multiplicative rate gap on this slice; surrounding confidence dependence remains separate.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 35525d5d40a09924d91a2f911b519c20c8e1c02742d539b9174b17c95a3ba925

S: delta=1/10, integer d>=1 and 0<epsilon<1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 2771bb48f20c9723b6289bda2964f13f684b29aa5466e7d4acdd52e3ea92725f

O(min{d,1/epsilon})

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 411b3961ac11348c76ea4910171c32da0826e9ff8612cf93abae06ba39f41e26

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 6d1a465728077867c3cad9e63bf5981d3cd2254fb213901b7efb015c72816d91

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 97f56f3fff2a1cc3a7c911e8a857ed1455f43d847eb2dffeaa99cac29e6e83b5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 2f0156adff42ef581328cd85593ef712c41250e940cfea824a6148e65d28c754

MX_S_TRACE_PSD__randomized_adaptive__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 55b73d0d42999bf7e5fd00dd26238ff29743593dd48c8c612891c92d06adfb81

Its registered accuracy guard excludes Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: bdef1e92fe1d86137b9a9e75c7b8f5d9d85d625636e1edc038196626e1fc08de

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 3e69e3715b7256da62149876e495f4a1e36b0c2bf45062c89176528b5b19951f

MX_S_TRACE_PSD__randomized_adaptive__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: b6699556e7d39d5e2b716fef2ec33059e2b01ff0538219cace7b8200c32b8695

Its registered accuracy guard excludes Z; zero output already attains zero cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: cc4be83d5e44babbe9d129b7e78505864df4af9f7b1e78c37bc8f660d68503a3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: 4412bdeae414db1f76d3b75d981614e1631fd25f38c812a8634c407269f6871e

MX_S_TRACE_PSD__randomized_adaptive__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: d39a7fef6d7c6b9a40d0b3a8f989dd1f35bf231270f213b599c1b9f670e293ae

Accuracy guard disjoint from Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: ba596bc48c5e3bb4d56bbfa467be4c6c0ac6f7bb6cced4f9240b899c071c18a6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: e078e74e3b7ba87947c418dc94710de8a32dda6d5533fb192015a96172654066

MX_S_TRACE_PSD__randomized_adaptive__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 76986cf11435ecd6ce69cc7081f38f3cdbad83ab25c05b4fbfe3461b19349369

Retain zero-output upper bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: 8d83cd9e5cb67d700d1fb15815ef0b9de2133dc5bb448607eeab1e193dbbfbcb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: ebfd4116c4045acbeaf84de067dff48ac014d1d84cce01052e4b9454af31389b

MX_S_TRACE_PSD__randomized_adaptive__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 9202f2a0b7ffd1067c148e3ca9d5b2de4cea278d4b134e87e3d276a39f174ff7

Retain nonnegative-cost lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 6

Native pointer: /joint_analysis/comparisons/2/bound_uses/5; canonical SHA-256: 392a2829f6ebfd89d026df30e7fab5f7dce4544102d2e76f3d4cbf3e741074a5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/bound_id; canonical SHA-256: f8858599c91dbf01faa97c6b8afbb27c680441d29122d8e2e6ea7b8effe39622

MX_S_TRACE_PSD__randomized_adaptive__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/reason; canonical SHA-256: fdbfa50bc86d9b65e1b0c5e4c6f928c9155dcb34f9aebbc60a3a46bc3d2934c8

The nontrivial-accuracy lower bound excludes Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 8bd5ab1786ad72b0a4e122fe680bd51207d482cbb62716f8d7cbe3bd301da054

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: e8c9c5837335799c1e4189d8dba1cabd23c703aebcc77efb8d577e728b91f382

epsilon=1 is included.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 0bc954ac30265807e9ffd4b4be7060ee4b1846ec1ecbac5423842bade067c283

Zero output also satisfies the required exact output on A=0.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: 8d55565f61579a2d3924d4c9a4452571f17eceff050d29776194ec7fdd7e4966

Exact cost zero; ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: a55292c379250cb75304f80140937a712fcc5b973f9e47a9f0870f70b88df146

None for the exact zero-cost task.

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

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 9fdf62f2b85827d60b75641f1110f3031fab313967debafafa9a37f91608f398

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: ba7ef61eefbfbabee4fc34a969ff3ad9d94f5b9d0f2281577298935154bce2ad

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: c04f896f9b9b63116fdeb3db8955b4e6232d5e34c8057cb982738baeefca245f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 4d8153fc164f5af03c8cd5b7bde488ca21acd00836f9db3deb3c29b595d16c0e

Retain the native nonadaptive upper branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 5666056537b90077970c91fcf6cc8d2ee502a1333f1d14ec3dc4bf993d76dd3c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: dcfb92aebcc0264d5a8d576f79b4eb814cf3ca340245f52e7c29091615443366

Preserve the older selected lower bound and its source window.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 29dc898b3a915d55be6dac720a5bfb7cb34598abc2f7f6f497ced79f8ea01609

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 1b97a227a31d4ddb08a352b42678bc25475edd0b6ad72e208722606ae03d8eeb

Retain reconstruction cap.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: e1b4d744827bd9675640b07f57435e429fd7d1c01d302932263f99ddc8f3aee0

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: 543f1fe492fa3da7cdc1964887df38b7c0e56ef0dad0c9b5971ad96af89c6b6d

No stronger rate than the selected Omega(1/epsilon) lower on H.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: 9883f468634b555ca847b34158ad9b084ec45a6ca46d6b6d54c4f5e3cc4b5f4e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: 47ca108475d3a6a7c226b6e865125981aa4aa7b465d1b56d7214c67f5f4cc0d9

delta=1/10 is outside delta<=exp(-4).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/bound_uses/5; canonical SHA-256: d85a0790db250e00bee932d8d62571b42e811eafd3c0598f9df19e41f28eb858

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/bound_id; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/reason; canonical SHA-256: 58c7ac5f75d13db0f086bc41b77b2dbd577a9453c7ef7ba546722d61cc60c185

Accuracy guard disjoint from H.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 7

Native pointer: /joint_analysis/comparisons/3/bound_uses/6; canonical SHA-256: 9cec025353971037f92cb063e3028eddc42c9f96de4e539ef23b1dd84b8de67f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/bound_id; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/reason; canonical SHA-256: 58c7ac5f75d13db0f086bc41b77b2dbd577a9453c7ef7ba546722d61cc60c185

Accuracy guard disjoint from H.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/3/bound_uses/7; canonical SHA-256: fae9b7be9dc8c4f59f5f67efa0e408a493f09d67626d465dc60f584300c03c8d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/bound_id; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs; canonical SHA-256: 67aa6a1393f7c376ea8fa7c4b5240b0b9bd359e5ac540437b3a6784e5f64cd28

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/reason; canonical SHA-256: 447ffd1d3e4ebc29402d80c0f325ba7d1c159f95484a73bf2c72cf922cdf49e3

Redundant in rate on H; no overlap improvement.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: 1b4874f75afb751c192ae002cabfe4fb7a48fb7654fe97b1dbe7e542a362077e

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: b9dcc7ac85fa3d597aa3240217a5a1a81b3cbd667fdd6b42eb0de59a29ff7613

d_0(epsilon) is a sufficient source threshold, not an intrinsic transition.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: f792354f88c6d73e7dad0748284bba940b06354759f166dbb66ad3372163e253

The valid older lower and reconstruction imply d>=c_H/epsilon on H.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: fe35e51a7ebedaacf183182a5d6be8680bae544a7c5047fd9d7cf7632890fafa

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/0; canonical SHA-256: b1b705fa457ecaac854a89b70946c31c0f55472fd6aab25af18c757cac7646e4

MX_S_TRACE_PSD_p_c8bdef7655

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 130c5e78cbaacb2af30fa4de81b23e8ae42f27df8cbbf58339b0ae17f4acc57b

O(1)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 12ef52d83eb3f1faec46b96eeee6a12be2e5535760c8127c8c090dae94b75dfa

Omega(1/epsilon)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 31ea9b6a143409fdb20257b550d06e07b1897b6bdd95b37b2878bea31cecdf70

No multiplicative rate gap within this retained source slice.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: fb5c227105cc88def4f3f35d4d2fe48b5ed02de09f76086c3f9f2ef9563465a3

H: delta=1/10, 0<epsilon<=c and d>=d_0(epsilon), within B

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: b17a09ba8ece92bfec62eb492392373dd340bc9f3a0bd2753ef6f545f2eada64

O(1/epsilon)

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: 1bfe07ceaec34f7b50871ea8cb66d8ce165418bed830d3a39d2ea99f232bd4d0

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: 9ea239e415799950efc8a5809854dd250925fa33952a1f8ad153e0f9a5207d0f

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: 4b63b974173c1d1a78313cf247f8ecb872f4a446cd615623182c54c8b07f8bfd

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: f727055a1dd574e1fd0bd3e8508305c56650a806a65c7ea13d26dba2ecb96233

Retain the fixed-confidence upper restriction.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: 72c3f1b7cf825b54a0449d5dfbc325219f195d9fa54089a7bf635169bb4a3f54

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 67aa6a1393f7c376ea8fa7c4b5240b0b9bd359e5ac540437b3a6784e5f64cd28

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: b8d071b118ca3e5288aa9c9e85398761d5ab7fcd0d2d90d678d5e4068411dbc8

Redundant in rate on H: reconstruction and its valid lower imply d>=c_H/epsilon.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: b0384697d81f5ae17f4fc86eaf56164a39ffd0b9f7d0aa0a890f36d6d0dbba72

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: 872cf876ea48aea3b77e07a83f6077949b6a02bd2e70ed1fb62d5ac0212b0dc5

Retain dimension cap.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/bound_uses/3; canonical SHA-256: ee2ca0031e69a3b5924cae367212a6ef7c29b2019a4cdbb7d9d7165b5f58084d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/adopted_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/bound_id; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/reason; canonical SHA-256: 88d09103cc9f3dcc7276195de024686010f01c1a2d7912a99c7bf3870ebf7b94

Preserve the selected all-dimension slice lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/validity_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/bound_uses/4; canonical SHA-256: 44cafe8fc0e1bf1cd9de11f2bf789b46eaa5b57fea1dd1652510a1cbf0dd355b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/bound_id; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/reason; canonical SHA-256: ab66e7b4423fcbc7b6e7d2de7a5fc818757f72cce0d47f8511282040b1502e16

The confidence guards are disjoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/validity_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native item 6

Native pointer: /joint_analysis/comparisons/4/bound_uses/5; canonical SHA-256: fafb3710c41799077e7a0a32442f04184ffff607f99a2ae11dbedacc8697c12c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/bound_id; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/reason; canonical SHA-256: 03e49d33ac33585f016eb3ce82fbccf97561e58a7cab274621f1702349fb1155

Accuracy guard disjoint from S.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 7

Native pointer: /joint_analysis/comparisons/4/bound_uses/6; canonical SHA-256: 8fd9bac51eb1c4654c19b8ae080275786d5a958d6ec0e978c2f158ab53a8113b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/bound_id; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/reason; canonical SHA-256: 03e49d33ac33585f016eb3ce82fbccf97561e58a7cab274621f1702349fb1155

Accuracy guard disjoint from S.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/4/bound_uses/7; canonical SHA-256: 21e93fce3f60e9afac5e9027ae851b45d6b61c2a97fe97d794642827e3263f09

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/bound_id; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/mapping_proof_refs; canonical SHA-256: 67aa6a1393f7c376ea8fa7c4b5240b0b9bd359e5ac540437b3a6784e5f64cd28

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/reason; canonical SHA-256: 2c9c4c471562f24c555714d871a8d45191b2dcd750f60d2566c9c23cc41519d3

Same lower rate as the retained selected b4 on S.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: cbe96177e36ab98ed55041694a74fbdcfff6a4a04f1186f59200fee2fe7b4885

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: 7d95591c6a1966e74099f606240c669ead50e65f40f5c0342d0cff992da2372c

This fixed-confidence slice includes every integer dimension.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/boundary_checks/1; canonical SHA-256: 8601636be30755dbc3a8a225ed95085869c2d6fe0ffbd3c5624749021dfe8d27

Finite-dimensional saturation is retained; epsilon=1 is excluded.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: fe35e51a7ebedaacf183182a5d6be8680bae544a7c5047fd9d7cf7632890fafa

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/fixed_parameters/0; canonical SHA-256: b1b705fa457ecaac854a89b70946c31c0f55472fd6aab25af18c757cac7646e4

MX_S_TRACE_PSD_p_c8bdef7655

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: 130c5e78cbaacb2af30fa4de81b23e8ae42f27df8cbbf58339b0ae17f4acc57b

O(1)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: 218ce7856d331569f8be5b8a809900c7466a707011a9cf3957650e62c99ee0a2

Omega(m)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: eae111cd8b1de61cb1cbf1d097f16faad22b0efc90a323735a36717b7b4f5d0b

No multiplicative rate gap within the slice.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 35525d5d40a09924d91a2f911b519c20c8e1c02742d539b9174b17c95a3ba925

S: delta=1/10, integer d>=1 and 0<epsilon<1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: 2771bb48f20c9723b6289bda2964f13f684b29aa5466e7d4acdd52e3ea92725f

O(min{d,1/epsilon})

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: d968a7653303a02358bd0964e6da4f5410e8d4b0894d16c1a7912b720aff8efe

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: 6b81bc6ccd67fb747b3f6c540577b102fa1695ae93c8b99ec2f836ea29107a49

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: d23d1ba3eef418de11756cd8a8e2682f40278a1432c46b619ab7b579036bde73

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: f4878965f22915bc78664653762dc3ec3828e161b2f4db108e0a71a4c95f7cfc

Retain the nonadaptive upper branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: ca33ac0438737baf639d197c3c97ce7b78658fab0b88aad8571ade6b27a7a2fa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: ab66e7b4423fcbc7b6e7d2de7a5fc818757f72cce0d47f8511282040b1502e16

The confidence guards are disjoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: 43cdf9a80d328f3c4dd30a3059f55617d9e0ce67d6e4490b6d99cf3ac6298456

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: d832b4b1628689074463565eba8bb4a49debe6c4efa4175185b28f39b9e647a7

Retain the native reconstruction branch; the sufficient-dimension guard prevents a stronger rate cap here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/bound_uses/3; canonical SHA-256: b5e92a63e476e21e79b1cec4d3472ba485d1ec05d8306c61b3cb3b6453f2cce1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/bound_id; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/reason; canonical SHA-256: ab66e7b4423fcbc7b6e7d2de7a5fc818757f72cce0d47f8511282040b1502e16

The confidence guards are disjoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/validity_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native item 5

Native pointer: /joint_analysis/comparisons/5/bound_uses/4; canonical SHA-256: 6ad12187f0c105a7ac9c48f116980ddb58df018dcbe9386cc82453ef950aa510

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/adopted_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/bound_id; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/reason; canonical SHA-256: cc8165877f9835fdaac1af285d3c5909d56e31dea6296db0c1c75b99c200917d

Preserve the selected piecewise confidence lower and exact registered guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/validity_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native item 6

Native pointer: /joint_analysis/comparisons/5/bound_uses/5; canonical SHA-256: ce36f5ddedd1796d8f28f652da494ade1fae2e90eff7c6ace6db3fa6a9d00e9e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/bound_id; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/reason; canonical SHA-256: 2c5bd88cbf79ee35c4ee0b3264338cf9a7e1b3c0e78ece59a59b6d4224dee5d4

Accuracy guard disjoint from G.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 7

Native pointer: /joint_analysis/comparisons/5/bound_uses/6; canonical SHA-256: a79bf042dbc020470040f9b93e036ea994377a7a600f9b05f2e7668e6a0b9eab

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/bound_id; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/reason; canonical SHA-256: 2c5bd88cbf79ee35c4ee0b3264338cf9a7e1b3c0e78ece59a59b6d4224dee5d4

Accuracy guard disjoint from G.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/5/bound_uses/7; canonical SHA-256: 0771d01684db607ed58a36926208384a0898b335e8adb487de7b0e2dec7e9dd5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/bound_id; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/mapping_proof_refs; canonical SHA-256: 67aa6a1393f7c376ea8fa7c4b5240b0b9bd359e5ac540437b3a6784e5f64cd28

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/reason; canonical SHA-256: e1dcba71716270805e68aa3aeb7bbd2509dd957e263b7094fc749546ba5cb0e6

On G, F dominates m up to universal constants; no overlap improvement.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: 06e61c382f43e3e42e29462b21aca8da3e53a74099b1c3d6b5caecefc42d19f8

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: d7bc1b5f0c1cce5272760d6dacf24a43fd1cbbbdd24300648f36237bf1dbaefa

G is a source-activation guard, not a phase boundary.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/boundary_checks/1; canonical SHA-256: 02b4ea6f8d4d11758ede316b00b9fd8bb82d6faedb9dc3da656c36ca5b45c69f

At epsilon=c_0/sqrt(L), use the first branch; U<=(1+c_0)F.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/boundary_checks/2; canonical SHA-256: 2c027926dbf722f1a20c3cd8a22327352b2f05e2169c75dbe646365dbb16ca77

In the second branch U<=(1+1/c_0)L, giving O(log L) ratio.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: cc0b1dcc8b60ee1f80d82e4e52199c65aa13c445ab5dabe9f5ebd7d5f99c46f6

O(1) in the first branch and O(log L) in the second; retained overall O(log L).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: 2421967708e16fe630728219dc4795f067e44a2c6d11557242b3d3e7571925e6

Omega(F)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: 98326c4028b0a4a6cff915d71cb2c0bcbdc1c01587dc0286190a671d1779bf6a

The retained second-branch log L ratio remains; no global optimality claim.

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: 26ee8108c9f439920a34dba32baa6e732fa7d06aa19de602a1288d8144b479f3

O(U)

#### Native item 7

Native pointer: /joint_analysis/comparisons/6; canonical SHA-256: 77d591164b54f290e50b2e4ad6e6627d79860bcc410230a96975d850c99aae05

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/6/bound_uses; canonical SHA-256: 0d5c14918b261b411e5a61357bc19453f51c010fdbc26f8b70cc14031814fca5

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0; canonical SHA-256: c53fb6300bc158ea6df860b521506f3d173ed65ba844abc71834aa222601082a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/bound_id; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/reason; canonical SHA-256: 0711c24cd6fbe0134e9e4597bddb58c5ec5d7c020c604090bdcfe6a3d256f8ac

Registered accuracy guard excludes Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/1; canonical SHA-256: 51f117cc244d08f74f5348778948e502e6b53bf2f6d21dd89e73f7509fe75882

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/bound_id; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/reason; canonical SHA-256: d39a7fef6d7c6b9a40d0b3a8f989dd1f35bf231270f213b599c1b9f670e293ae

Accuracy guard disjoint from Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/bound_uses/2; canonical SHA-256: bbf0c5fc0eee58f854b3e1544471cdd3530d46ca22273c45707cbf399922a079

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/bound_id; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/reason; canonical SHA-256: 9cff65b8599361ffb02e5fecc80e5040a6f3c26e4969c61a7b75a18eb2983fcf

Registered guard excludes Z; zero output already attains zero cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/bound_uses/3; canonical SHA-256: d12550b0f6ee21fe3a64bb7e48d266db7967f62f7da44a08eb51faf05755042d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/bound_id; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/reason; canonical SHA-256: d39a7fef6d7c6b9a40d0b3a8f989dd1f35bf231270f213b599c1b9f670e293ae

Accuracy guard disjoint from Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/validity_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native item 5

Native pointer: /joint_analysis/comparisons/6/bound_uses/4; canonical SHA-256: 7edaae89119176c3ce5a69cb8b4e367ce557f17b09f895f6473917a8f1fc826a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/bound_id; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/reason; canonical SHA-256: d39a7fef6d7c6b9a40d0b3a8f989dd1f35bf231270f213b599c1b9f670e293ae

Accuracy guard disjoint from Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/validity_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native item 6

Native pointer: /joint_analysis/comparisons/6/bound_uses/5; canonical SHA-256: 87e21b9fe8b01bc9f6828192cce091979c37f8670cc6e37e7409db74411acaae

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/bound_id; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/reason; canonical SHA-256: e2830fc779816001eacbff004e27537411c5fe0c31e915f9e6352db115da9e7e

Retain zero-output upper.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 7

Native pointer: /joint_analysis/comparisons/6/bound_uses/6; canonical SHA-256: f860e3026e0f892fd52465754d49d57edaa4099c34430aba57684fd697a0b8b1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/bound_id; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/reason; canonical SHA-256: 1d7b1f95e4b8189bc0d5866935698f0a498052362e94a0a7b23af898592110ec

Retain nonnegative-cost lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/6/bound_uses/7; canonical SHA-256: 43f4834d17479b57b6a268f0cd2aea8d4cb001a806435edcf5cfa3e1910708ab

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/bound_id; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/mapping_proof_refs; canonical SHA-256: 67aa6a1393f7c376ea8fa7c4b5240b0b9bd359e5ac540437b3a6784e5f64cd28

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/reason; canonical SHA-256: b5a968f598ae6e024c99fe76867189c5e84d94fb3777d7672da1ddc48a2cb868

The new bound expressly excludes epsilon>=1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/6/boundary_checks; canonical SHA-256: a16673e2b96207e44e32b34c4e1f8a21fe3c1ec3d816cd4f1b32b89641e03ded

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/boundary_checks/0; canonical SHA-256: e8c9c5837335799c1e4189d8dba1cabd23c703aebcc77efb8d577e728b91f382

epsilon=1 is included.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/boundary_checks/1; canonical SHA-256: 0c3e29aa5729a6abcafedeabbf32a85720fb63b3daebd48095f1c0434371b9cd

Zero output remains valid on A=0.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/6/comparison_id; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/6/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/6/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/6/gap; canonical SHA-256: 8d55565f61579a2d3924d4c9a4452571f17eceff050d29776194ec7fdd7e4966

Exact cost zero; ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/6/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/6/remaining_gap; canonical SHA-256: a55292c379250cb75304f80140937a712fcc5b973f9e47a9f0870f70b88df146

None for the exact zero-cost task.

#### Native field: role

Native pointer: /joint_analysis/comparisons/6/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/6/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/6/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native item 8

Native pointer: /joint_analysis/comparisons/7; canonical SHA-256: 0d897b822d99c82f03052d058070af27297f4c83c8f0e337f4966e8c7b3dff48

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/7/bound_uses; canonical SHA-256: 8208901c4615375fda5d0f9da580b721adab4ea3fe0e0c044d5c6be69542a113

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/0; canonical SHA-256: d38bf649b1ce15e62d29ce045261986751ea590b873cdcaa1d93792d84102776

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/adopted_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/bound_id; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/reason; canonical SHA-256: 8e3ab88cb97347b40dfc9ecb24e7b9e5cfc8df610e100e586e997a291a87185e

Conditionally retain the native nonadaptive upper branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/bound_uses/1; canonical SHA-256: 754cc338263072abb7e428efc3a4d258ce6833b32b1a930520efeb6911198139

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/bound_id; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs; canonical SHA-256: 67aa6a1393f7c376ea8fa7c4b5240b0b9bd359e5ac540437b3a6784e5f64cd28

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/reason; canonical SHA-256: 328f6ac3e15e7d966036ef5d893f833337df7b45498a089230a7ccceed22acaa

Its inverse-accuracy rate is redundant on H: its valid lower and reconstruction imply d>=c_H/epsilon.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/bound_uses/2; canonical SHA-256: 35ac605a385fc77bd0aece4a4f75f361b8b88bc8021094dbec3d975fdf9970cd

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/adopted_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/bound_id; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/reason; canonical SHA-256: 19b87cfc7b0d52d4c540765824f4bc36e878f08b4eef757405be2f27022b9225

Conditionally retain reconstruction in d preselected calls.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 4

Native pointer: /joint_analysis/comparisons/7/bound_uses/3; canonical SHA-256: 43006c24bd0c68faad4323e112c49d57149e24289ec4e0823601e01470f7ad3a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/bound_id; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/mapping_proof_refs; canonical SHA-256: 67aa6a1393f7c376ea8fa7c4b5240b0b9bd359e5ac540437b3a6784e5f64cd28

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/reason; canonical SHA-256: 12d7b883e04687466a97e0294aff1c2c49f892d098c0f2ed5825f670b2c9ebe6

The uniform new lower has the same rate on S.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/validity_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native item 5

Native pointer: /joint_analysis/comparisons/7/bound_uses/4; canonical SHA-256: 66bdfdae9508f7762164f96f178319822a5423896eec2e776d11926b1bad3582

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/adopted_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/bound_id; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/mapping_proof_refs; canonical SHA-256: 67aa6a1393f7c376ea8fa7c4b5240b0b9bd359e5ac540437b3a6784e5f64cd28

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/reason; canonical SHA-256: f898be8244e2228e47bbcfa174929f39fbac1d603189861b9c675bfe0f09a8c9

Retain the stronger confidence lower only on its original guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/validity_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native item 6

Native pointer: /joint_analysis/comparisons/7/bound_uses/5; canonical SHA-256: 22f6c7ed30adbccff533f8e866539ded545b68f74b38cdaa214634145488c2f9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/bound_id; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/reason; canonical SHA-256: 2cc10fc75d25a8ab23ef4eb592772e9a63c7706cc6564fa05b231c5a0df8d349

Accuracy guard disjoint from B.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 7

Native pointer: /joint_analysis/comparisons/7/bound_uses/6; canonical SHA-256: 2f27834217ded07afd6551383aa113349cd4df79f6b70adbfc092f791af4d960

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/bound_id; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/reason; canonical SHA-256: 2cc10fc75d25a8ab23ef4eb592772e9a63c7706cc6564fa05b231c5a0df8d349

Accuracy guard disjoint from B.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/7/bound_uses/7; canonical SHA-256: 1ab0c0f87d951de97341a80f7a467cdebb0da9434c8b5283786f970a92b288b1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/adopted_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/bound_id; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/mapping_proof_refs; canonical SHA-256: 67aa6a1393f7c376ea8fa7c4b5240b0b9bd359e5ac540437b3a6784e5f64cd28

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/reason; canonical SHA-256: 0993db762f8e16c607d93985c143e564f460170526c6f69bc576bcec316eace5

New cost-preserving class-transfer lower; redundant in rate with F on G.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/validity_region; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/7/boundary_checks; canonical SHA-256: c8116684b893a265429467de09ee2e8321ebee06549d6bf205c9f597884996eb

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/boundary_checks/0; canonical SHA-256: 0e73134300de2983afefdefdc504437b5cef41802728c2c1a30fe86b2db40981

Integer d=1 has exact cost one on B: a positive lower bound forces one query and reconstruction uses one.

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/boundary_checks/1; canonical SHA-256: d26fd338d5a61eed8c5472bbe1ee1e9bb30cbe44e28f68316e7a32d08c521f34

d<=1/epsilon gives Theta(d) uniformly in delta.

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/boundary_checks/2; canonical SHA-256: ff8fba0d05daafdf0380b0c28ca606a09b9258d939eea2ecb730549975d9729f

d asymptotic to U is only an upper-envelope crossover.

#### Native item 4

Native pointer: /joint_analysis/comparisons/7/boundary_checks/3; canonical SHA-256: 6fa2ed70bec120956ab935911770785019c865976a20b8959523608370802af8

G is a retained sufficient source guard; use the first branch at epsilon=c_0/sqrt(L).

#### Native item 5

Native pointer: /joint_analysis/comparisons/7/boundary_checks/4; canonical SHA-256: 89b843169162bb06f4c0157edba2e63ef14f1b8bd4c901ec39dd746b96fbc30c

epsilon=1 belongs to Z, not B.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/7/comparison_id; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/7/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/7/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/7/gap; canonical SHA-256: 9f36097b206ead9a8f0216c99b5cd560b59e9a39c81d37f1bb114053046826b3

O(min{d,U}/max{m,F when G}); constant for d<=1/epsilon and for G's first branch; O(log L) for G's second branch; at most O(1+sqrt(L)+epsilon L) elsewhere.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/7/lower_envelope; canonical SHA-256: 5b7aae304b5c87817312b3cb3480d78c6c841d6c026afc4364e2cb3889a0a93a

Omega(max{m,F when G}); omit F outside G

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/7/remaining_gap; canonical SHA-256: 1c91caeba52dd32d7929e3e99bc31a99e49620f3fe1cbce0897fd8e7d7a5ad69

Sharper confidence dependence outside G and the second-branch log L ratio on G remain unresolved by this local derivation and unfinished literature assessment.

#### Native field: role

Native pointer: /joint_analysis/comparisons/7/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/7/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/7/upper_envelope; canonical SHA-256: 23e599f3f190cb50f18b1e85e408d995b9d212ad1bd57792a23b1c6fd8894711

O(min{d,U})

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 8f2f7f4a2afee7f1d7ed96d976101d9b0644bbe9c5c0d379e1987d3ba10b62ac

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 6b49a5ce19ff27294c505b3badfba64cf86b88615cb952577d7b3640ec136057

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: eb68551ddc88c6c3947b061f2bef09d1ba30858e104cf3fca9a70592eba37e6e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 0ec68adf809989d52e3973f362cd97556014eb0e00bcac644654eb34dbf90802

adaptive_joint

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: c6f7433292f1766896006a1e20df6212ee39ded1c88dd641d00828a2e59aa705

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 54bd864da837e52a3d42075a2ab861ef032867510948beab52f8907fd1798f80

Retained joint bracket; sharp confidence dependence is not certified.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 0facd05b187a64db10373e89b3098b393736cbfbe7dbd5722c0aa670517572c7

adaptive view; B AND delta!=1/10

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: c3b4e858d01e62c6ab4b9d8d0e4abf38d91e734291d15a8c4a0aad92b30c54f1

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 8f34bb6dad2079c9ff27b692684965c6742de939c118c25f70f83fbf7b3a293c

adaptive_slice

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 5cfc3cf37cfad20dd4aa01a7f6d1a260bbe1350a3bdcc0cd2fe86e5160c01855

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: d260115cc023f287b4d93de105005c6f95fe3f3cc09da8733479547c6b0874fe

Fixed-confidence diagnostic slice of the joint target.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: a5ff711b7b1969e1d36edd8e6ff227f6bc893fbe1661d136498cc346031eaf86

adaptive view; S

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: ccf93c129ebf5075444b7509309758fde011352c7937f5fd1effabfab48abb1a

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: f37915a7b91dffd5ff3871276aacfda3b4b95748a1ace23e8fbf018fb3131765

adaptive_zero

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: e649f22df3ad00177b4cf9d89e5a6dca3c6880624065b00aa68d173495f7813e

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs/0; canonical SHA-256: 12b3c71176961dc7cb645db1566057cf450be952200b163554e3674455b68977

SIX_PROOF_369230c34039

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: bc9a904605c4007dffe2a827e5ef9bf03a1a90555d96c0118583325b3253349d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 8d55565f61579a2d3924d4c9a4452571f17eceff050d29776194ec7fdd7e4966

Exact cost zero; ratio inapplicable.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: b52b541a485039cca18112817cfab1cfd9c1232761c4ef78a294562e0a6b3a57

adaptive view; Z

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: bec7fba652d52228ceffde7712a4147a64d430735ab1b726bad2c48aa5988fb3

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: 6e24ab6fcbbc4d8130d12099597b82065ffe19986698aca12d7d0701a09f1bb5

nonadaptive_earlier_slice

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 9b1c6783e11455e9292a15cc07b34d8e4c06d21d66fb67822206286fcb3d498f

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/1; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/2; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: 58be9e77bc0632d2cc050a97eabcbaba8b201a0332d081d25148e19127ad59c6

Older sufficient-dimension window retained without a rate improvement.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: d302945132f194d92704741f667b2942a0639460ff9520c0276a1ed7d5bb46af

nonadaptive view; H

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: cf2e794b4f266d4d1e3a757740f990a62bca9671403bedb3bbed7c3c4e48f4a2

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: f990a3178fa7f9677180086cb9011b183b80210ef57f9a411eb338838ad60e9d

nonadaptive_other_slice

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: cc1c258bea74dac90ad5dc6770c7ca788016b0ffbf676ff2e94ab250e8fb18a0

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/1; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: 5a0c108ea411b22d0d48c184ce716a3960d8fe7eeda17769b01017358d13971e

Remaining fixed-confidence slice, including finite-dimensional saturation.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: c8b1d62502d3ac3e2f039336c32402fde568bc12fcfe5d56dc0603a623ec46ed

nonadaptive view; S AND NOT H

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 6

Native pointer: /joint_analysis/domain_map/cells/5; canonical SHA-256: 97fbe1863ae9578808450656b5ae7f72d948a44b5782dbd98a9a41cd8a5a2faa

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/5/cell_id; canonical SHA-256: 232f0835178c5f56e40956f13e2cc4683096849db6d35fa694291cebfe703626

nonadaptive_confidence

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/5/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids; canonical SHA-256: ab3cd3a86e9c0dc0085f12e42f471d776d9fca6d598377936277994a15d4939c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids/0; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids/1; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/5/note; canonical SHA-256: 2b8df28cb7d88520146c3c296849f3799c5d6a2c9be330ab9310471bf2960f00

Retain the stronger lower bound only inside its original source guard.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/5/predicate; canonical SHA-256: 995adf37cc4c24d29085d1fbb1596ec2ae952a6e7cb124a720450deab6e1ee20

nonadaptive view; G

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/5/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/5/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/5/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 7

Native pointer: /joint_analysis/domain_map/cells/6; canonical SHA-256: 8b9696010dfad549508f955bc4b1510bf29a4be43d34a4d0dd741283362c5278

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/6/cell_id; canonical SHA-256: a18bceeef026595b759013f1c8429d57ec8a8011d63afe049b32d1f4c9d3a735

nonadaptive_remainder

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/6/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids; canonical SHA-256: 197d864436f42e30608f6db8d3e759883201557392fe1f84ee29746a8eaf777f

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids/0; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/6/note; canonical SHA-256: 116ab4e630c54f40b861ac08b9e003eaa61991396715d4e50512c06a140ae8cd

Newly registered joint bracket; sharper rates remain unassessed by the unfinished literature investigation.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/6/predicate; canonical SHA-256: 5059bdba5124c828ee79a8892a865364db5b1c19e29431003f608e2b16b4842c

nonadaptive view; B AND delta!=1/10 AND NOT G

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/6/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/6/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/6/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 8

Native pointer: /joint_analysis/domain_map/cells/7; canonical SHA-256: a2d945e9eff44bcd05b3c4a085b0e494a596a9499944cf0cb64fc460d0cb8f41

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/7/cell_id; canonical SHA-256: c964620f83feded3d4c06453693d662f3b3f5640c2d48afe41044d5f9ed20008

nonadaptive_zero

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/7/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/7/closure_proof_refs; canonical SHA-256: e649f22df3ad00177b4cf9d89e5a6dca3c6880624065b00aa68d173495f7813e

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/7/closure_proof_refs/0; canonical SHA-256: 12b3c71176961dc7cb645db1566057cf450be952200b163554e3674455b68977

SIX_PROOF_369230c34039

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids; canonical SHA-256: 0c448c0cf35868e1a8979bfff9cbaf79ebc8e93239402a68bd93e610fc20a6db

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids/0; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/7/note; canonical SHA-256: 8d55565f61579a2d3924d4c9a4452571f17eceff050d29776194ec7fdd7e4966

Exact cost zero; ratio inapplicable.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/7/predicate; canonical SHA-256: b1724320609ccb8e1d5008a4b3587b753afc4b0b4bf5bec438187c4445047686

nonadaptive view; Z

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/7/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/7/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/7/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: d8831ac52e90de56314660a63809a10423f90a5567a19b1d6bb46835cda918e8

Within each view epsilon>0 splits disjointly into B and Z. Adaptive B splits by delta=1/10. Nonadaptive S splits into H and S outside H. G is disjoint from S because exp(-4)<1/10; the remaining cell is B outside S union G. The two views are distinct contracts. The symbolic source constants do not define an asserted intrinsic phase transition.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: feffdbd489406ca79b6ebb70acd72f6706c491f460d8ad4ec630b6f0995a8193

Empty as a parameter-coverage complement for recorded bounds in either fixed view. This does not establish sharpness or completed literature research.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 6bb804c8f9dad3ba434777f5866342b9a6becaf5b18bdbb6f2645432377315fd

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 88c3965171d23de073ea906ddbf240df7a9c66e7ea4e505922be3230f2cdb9c9

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: ebb94a1544f16db7823d71ce7564958fe046020457291a133a58fb349171bef1

Algorithm inclusion preserves queries, outputs, probability and fixed worst-case cost. Retain the stronger F only on G. The exact epsilon=1 endpoint is separately retained, and d~U is only a rate crossover.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: e9048eb65f2cf0edf646d98435865aa8d9948ce06aa01a93639ed2a274d5a8c9

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 3

Native pointer: /joint_analysis/impact/0/comparison_ids/2; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 4

Native pointer: /joint_analysis/impact/0/comparison_ids/3; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: e79f7e801316a9fb5792dc36a7e8e4354e99ff3f626e647b809b3aedc5cac834

#### Native field: new_domain

Native pointer: /joint_analysis/impact/0/extension_witness/new_domain; canonical SHA-256: d8b71a4114780aad456b75d987858afa2ec3b0bff64aaabbf9f8e9dac13c3088

B for the new lower; G alone for F.

#### Native field: old_domain

Native pointer: /joint_analysis/impact/0/extension_witness/old_domain; canonical SHA-256: 8755f0d09fab0af3606458d96b24a3092c09d9bbb0632767ae2042cd60e9bd96

Nonadaptive upper O(min{d,U}) valid on B; populated native lowers Omega(1/epsilon) on H, Omega(m) on S and Omega(F) on G. No full-B nonadaptive comparison.

#### Native field: outside_old_argument

Native pointer: /joint_analysis/impact/0/extension_witness/outside_old_argument; canonical SHA-256: 42130b3d4ad62068ec2344d921426de1665049b04c46740f241fd36c4a0267f1

The old accepted S/G high-confidence windows require delta<1/e. The displayed delta=2/5>1/e lies outside both, while the newly registered B requires only delta<1/2 and contains it. The chosen epsilon=1/(2d) is in (0,1) for every positive integer d. This proves a nonempty new registered validity region, not a claim of a new minimax theorem.

#### Native field: outside_old_witness

Native pointer: /joint_analysis/impact/0/extension_witness/outside_old_witness; canonical SHA-256: e95a5330e3d073dee9eb807b1704c5e044f19cda628fd29b1a5e8f98aae3c5cb

delta=2/5 and epsilon=1/(2d), integer d>=1: outside S and G, c5 records d/384<=N*<=d, hence Theta(d); d=1 has exact cost one.

#### Native field: proof_refs

Native pointer: /joint_analysis/impact/0/extension_witness/proof_refs; canonical SHA-256: 89be8c8b44e7d654f11656c8077da852b207595f325192e5d84eddaaeea75c63

#### Native item 1

Native pointer: /joint_analysis/impact/0/extension_witness/proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native item 2

Native pointer: /joint_analysis/impact/0/extension_witness/proof_refs/1; canonical SHA-256: aee8f51cfdd095f53b836439070df847ec39582a2ebb521efbcfe9b33677349d

SIX_PROOF_7ed1f0347d6b

#### Native item 3

Native pointer: /joint_analysis/impact/0/extension_witness/proof_refs/2; canonical SHA-256: 5d7cde343e7066e436463b1bf1e6d75b1d4c787e1aa8cf733362b1f0980dd9f0

SIX_PROOF_b3242221f506

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 61ca17edb2c7b1fcf50757a986655ffd05bf854d02d510ed7e7e88333ddb9ffc

MX_S_TRACE_PSD__nonadaptive_uniform_confidence_transfer

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 5c3c1b577bbb396a8582db75c2d5a105172747c4ed066ffb333f553bc80c7af7

Newly registered nonadaptive coverage B outside S union G. This is a domain and registration extension, not a stricter rate on an old populated bracket; old consequences of guarantee containment are not claimed as novel rates.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: 6c09510eb937226bbc6ce35656f44dccd8607964af9f29cac4e5cd5bd9bdc3c4

domain_extension

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 25073dcdce4d9306290de3d9a060b1d686e9d6a7f2bf76a9e8e3f44f937a9389

New c5 has upper O(min{d,U}) and lower Omega(max{m,F when G}); all old populated comparisons are unchanged.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 8755f0d09fab0af3606458d96b24a3092c09d9bbb0632767ae2042cd60e9bd96

Nonadaptive upper O(min{d,U}) valid on B; populated native lowers Omega(1/epsilon) on H, Omega(m) on S and Omega(F) on G. No full-B nonadaptive comparison.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: ed10d4d33bf8b81c7e849884c7576459ac331a450a168496ad96c2ae510fb05d

All adaptive comparisons, S, G and both zero-cost regions Z.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: d8b71a4114780aad456b75d987858afa2ec3b0bff64aaabbf9f8e9dac13c3088

B for the new lower; G alone for F.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: e95a5330e3d073dee9eb807b1704c5e044f19cda628fd29b1a5e8f98aae3c5cb

delta=2/5 and epsilon=1/(2d), integer d>=1: outside S and G, c5 records d/384<=N*<=d, hence Theta(d); d=1 has exact cost one.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: e39d810a636404cc8703c81b9a8a37fda8161d090fa783fc167dd9299c31070c

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: bfebd5150bc671e3ea11bd290c5259973deaa4a259f55cf129149deafc3ae437

Native quantities already track dimension, accuracy and confidence with no fixed parameters. No normalization is needed. Presentation restructuring supplies no new scientific premise.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: bc5214744a5f511b7d585367bdd12dfb93a68fa55392d96d07146d5001c8c0ca

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native item 4

Native pointer: /joint_analysis/impact/1/comparison_ids/3; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 5

Native pointer: /joint_analysis/impact/1/comparison_ids/4; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 6

Native pointer: /joint_analysis/impact/1/comparison_ids/5; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 7

Native pointer: /joint_analysis/impact/1/comparison_ids/6; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: b73a87de86f7b0c58c8ff9263f8e10dcae579086cbe3b4608fa7fefbb0253d0c

MX_S_TRACE_PSD__joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 71909d4528b1980c359a095629673dce531ecc34d053f31047e22922560725a9

None for the preserved scientific rows.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 00552091e2600f858ef46ab32ad3113eab60bd7d387d4fed953e3df2322dc0fe

The same seven envelopes and guards, with explicit joint variables, secondary slices, candidate dispositions and domain accounting. The c5 scientific delta is supported separately.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 50c55facf8f19f3d8d732c85ed5ecf0a0efb0a928f07d103823c12effcc0b69d

All seven frozen native envelopes and guards.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 3dca52ce7bf5e4b62ebc6065de885f3337e37fb9056fd138cd999fc60275cb10

Every previously registered bracket and status.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 7e5a55e896898594d3675d5c9e2f4917c661a605aa75b0b2bbc21a2e74959fea

The fixed domain in both views under conditional retention.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 6170f59367715cf8b36bc9b78ce1de97125c2ac86d0ff1ccccdc99ed0e8a1ff1

delta=1/10 rows are explicitly secondary slices; epsilon>=1 remains exact zero.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: eb895e722bfb7bcbc486994a7dcc3f58bd4e0db7773a2cf26531e6cd6a3b5282

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 82ad21831e5823d21add25baf8dbc12b0bbe0afc6c9339aedbb1202444ba4cfb

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 0762f72fe77f76454ac8da2f909b1c42551948a8197d4de473bf5c027f16c524

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native item 3

Native pointer: /joint_analysis/impact/2/comparison_ids/2; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native item 4

Native pointer: /joint_analysis/impact/2/comparison_ids/3; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 5

Native pointer: /joint_analysis/impact/2/comparison_ids/4; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 6

Native pointer: /joint_analysis/impact/2/comparison_ids/5; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 7

Native pointer: /joint_analysis/impact/2/comparison_ids/6; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native item 8

Native pointer: /joint_analysis/impact/2/comparison_ids/7; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 7147dd6c4b9de002d82a84fdf78cdec035511125d607e0f683240b825c058843

curated_feedback_MX_S_TRACE_PSD_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 96ba1db06ac590c41ca30eb921b08bb21f8492b1ce87474205455697191883f5

Both registered views separately: integer d>=1, epsilon>0, 0<delta<1/2. B denotes integer d>=1, 0<epsilon<1, 0<delta<1/2. Z denotes integer d>=1, epsilon>=1, 0<delta<1/2. S denotes B AND delta=1/10. H denotes S AND epsilon<=c AND d>=d_0(epsilon), with the retained universal source constant and threshold. G denotes B AND delta<=exp(-4) AND epsilon<=1/4 AND d>=C*(sqrt(L)/epsilon+L), exactly the retained nonadaptive r4 guard. Set m=min{d,1/epsilon}, U=sqrt(L)/epsilon+L. Only on G define F=sqrt(L)/epsilon when epsilon<=c_0/sqrt(L), and F=L/log(L) otherwise; C and c_0 are retained universal constants, not varying structural parameters. The native adaptive and nonadaptive quantities remain distinct minimax fixed worst-case N_right costs.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: eda1912754fb5dbd40af25eb226bd92b3d4c852f8414152bf6f3be05880f4c63

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 27f13269515265b1342c5f746170f0138e34ac988e3697d1c69e363782cc4706

The exact previously adopted science is conditionally retained. Correct only open-cell closure-publication metadata to the current explicit unassessed convention; no bound, guard, comparison, scientific contract or summary changes. Grouped cross-ID opportunities remain unassessed pending work, without any adopted reduction. This is presentation restructuring, not a new theorem or blind research.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 0762f72fe77f76454ac8da2f909b1c42551948a8197d4de473bf5c027f16c524

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 5

Native pointer: /joint_analysis/impact/3/comparison_ids/4; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 6

Native pointer: /joint_analysis/impact/3/comparison_ids/5; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 7

Native pointer: /joint_analysis/impact/3/comparison_ids/6; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native item 8

Native pointer: /joint_analysis/impact/3/comparison_ids/7; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 25078cb486d82a69d72c2607bf60f99b00ceda0ee4df4618416bb4018a926a66

curated_feedback_MX_S_TRACE_PSD_20261116_42b1a1bbfb

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 96ba1db06ac590c41ca30eb921b08bb21f8492b1ce87474205455697191883f5

Both registered views separately: integer d>=1, epsilon>0, 0<delta<1/2. B denotes integer d>=1, 0<epsilon<1, 0<delta<1/2. Z denotes integer d>=1, epsilon>=1, 0<delta<1/2. S denotes B AND delta=1/10. H denotes S AND epsilon<=c AND d>=d_0(epsilon), with the retained universal source constant and threshold. G denotes B AND delta<=exp(-4) AND epsilon<=1/4 AND d>=C*(sqrt(L)/epsilon+L), exactly the retained nonadaptive r4 guard. Set m=min{d,1/epsilon}, U=sqrt(L)/epsilon+L. Only on G define F=sqrt(L)/epsilon when epsilon<=c_0/sqrt(L), and F=L/log(L) otherwise; C and c_0 are retained universal constants, not varying structural parameters. The native adaptive and nonadaptive quantities remain distinct minimax fixed worst-case N_right costs.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 2a271f0e155a11d81da116ff9e5f6e3db14640fb8f24c2a6e1275f0bdeddfb70

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: bb2e91ac0444646d75c34ba803288aa836998eebfade8f29e64a4a1f3bd750ed

Independent review of the new class transfer and guarded synthesis, retaining rather than recertifying the exact cited baseline premises.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 5eaf5e9aca4aa8ad3e56045a91acae9f74082e3c71ebe21b4fe37bfdce85e4df

Complete the formal static lower-bound and PSD-transfer investigation for arXiv:2209.15219v1, source e8895c0e3a4005a745fbee15eb91acafbdfbe5be855e9dd976b8cc96c254059f. Ranges [9000,19000) and [26000,36000) were read; formal Theorem 4.2 around PDF pp.8-9 and its proof were not read. No result from this paper is adopted.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 39941816445188760cb5755fa747852be66b4857556eb190737fd84a7145d1f4

Read potentially relevant theorem and parameter dependence in arXiv:2109.10659v3, 2505.12289v2 and 2506.22701v1. Metadata is not theorem evidence.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: ef2dfc27fbdb97cebf6743ef9e795df45c6ed07472d24cdc42eccbcf20debce6

All 18 records of terminal metadata search 2556a242906f562713c1c68b6202d4cc09e638590a405a07d821d2d9bf8d8756 were exposed. Relevant source assessment and a complete correction/version investigation remain unfinished; no exhaustive literature or globally sharp confidence claim.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 069d3aa84ff65bf0db18bbbd6417242b2fb09b7fc4c1eecb0f0913bcbd9b2d5a

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: bf3effa3ad59c5e649b015bd9f0132c9ce0df5160a2df88e73a03d4d7f397855

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 2f0156adff42ef581328cd85593ef712c41250e940cfea824a6148e65d28c754

MX_S_TRACE_PSD__randomized_adaptive__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 3f61f2f2a68e6403a5521e845cd47e2e9a294d2b421235149c325ad314565a2f

Conditional retention of the unchanged native adaptive bound.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 5fda625c1f906193c8163e6c323261c688bea2ebf696b395263eb064d22590c7

Accepted native guard B; original theorem is not recertified.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 7f6512009c325905f06cd30e7d657768161cbf9bb2b4a7c0d34216354987d4b4

Frozen adaptive b1 and its native evidence dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 89d7cf9474659f43f064745f0e046e2dcdd5d5fc292aa52d2c71c98d1df7b14e

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 61babcf8875d3875227c52b040567845f43aa824fc6543f39b9c6f1dd645d8bc

MX_SRC_HPP

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 7c2e5b232b0d597e20cd3363d05e282eb50c72999d40aeacf9eedbf3c4a79893

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 3e69e3715b7256da62149876e495f4a1e36b0c2bf45062c89176528b5b19951f

MX_S_TRACE_PSD__randomized_adaptive__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 7845b6482f4c2dd8f75e0e6f24a314e1e340d0cda879a85e1ccdf452cab58b81

Conditional retention; no new transfer asserted.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 2f186a46b1d9be40e4cfbac5bfbc3f48f1c6969a440c20c234d191c2ee3cde34

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: aee8f51cfdd095f53b836439070df847ec39582a2ebb521efbcfe9b33677349d

SIX_PROOF_7ed1f0347d6b

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: ae9c9256a568e1ec7be8c75887b81bfd56a1e15ee9fea32974d15ea1b82c2877

Accepted native guard B.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 4668599f8a2da8a29ba4973804d76c4faea507cdd6578f7580ffc3d06915f5a2

Frozen adaptive b2 and its native reconstruction proof.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: c820b1b84e5887225e26f3e03c70c10f0a9029a13c897fd1f4c47f8c8edb9f47

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 4412bdeae414db1f76d3b75d981614e1631fd25f38c812a8634c407269f6871e

MX_S_TRACE_PSD__randomized_adaptive__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 15f9dd609295796ecdf859d67160c2351e121fcb1197fac4010bc3ec8ce52f26

Conditional retention of the unchanged slice lower.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: be0f58720543eabcdd516b831c07b68be3e31fbbead8057e5fd8d34e6f5ebbdf

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 5d7cde343e7066e436463b1bf1e6d75b1d4c787e1aa8cf733362b1f0980dd9f0

SIX_PROOF_b3242221f506

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 04fafc07089ea8d74b737c12e11311f6f3809547a4396d229679b361dba5300b

Accepted native guard S; external premises are not recertified.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 47719283e62ccda714826434502f82ef4656b4e353f3c51288e437c9c2baeed6

Frozen adaptive b3 and its registered proof/evidence.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: ad9486d8ffa44d7d528fde185cc1a241de3dfb3991254375c6cb02fe722d4f28

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: fe2720c39605ebb591edb442844498d28d4ea50ef83279241cd33619181bcc9b

MX_SRC_FS

#### Native item 2

Native pointer: /joint_analysis/provenance/2/source_refs/1; canonical SHA-256: fc8389352f8fe8aa765d983280ab1e22a9e1392914083a648f803c48ae870522

MX_SRC_BH

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 18aeb832401e2c330742d3ff9974e8084d1b3ac4007ad7e676f4dd6458a63686

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: e078e74e3b7ba87947c418dc94710de8a32dda6d5533fb192015a96172654066

MX_S_TRACE_PSD__randomized_adaptive__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 2bf43f089160d9cf0fd22cfe650ad569badf32e274bfa9aef5d4683a64d49319

Conditional retention of exact zero upper cost.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: e649f22df3ad00177b4cf9d89e5a6dca3c6880624065b00aa68d173495f7813e

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: 12b3c71176961dc7cb645db1566057cf450be952200b163554e3674455b68977

SIX_PROOF_369230c34039

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: ba87e317fbc161249bac8091dae38beac0600a10d467885eccf0ae27b10841de

Frozen adaptive zero-output bound.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 52cc3c354db5c040055aead7d8e7daf676bf091acba9421738f475620761ea31

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: ebfd4116c4045acbeaf84de067dff48ac014d1d84cce01052e4b9454af31389b

MX_S_TRACE_PSD__randomized_adaptive__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: 8375035318a86ed75eef33a46082b6288936c8903370017f75a673824e1e4399

Conditional retention of exact zero lower cost.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: e649f22df3ad00177b4cf9d89e5a6dca3c6880624065b00aa68d173495f7813e

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: 12b3c71176961dc7cb645db1566057cf450be952200b163554e3674455b68977

SIX_PROOF_369230c34039

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: ac06f2a1f678b4ebc9b6e25148c43bd8f47613ac3bb14a72877284b45d2b001a

Frozen adaptive nonnegative-cost bound.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: cdb6d0dc455891352b2a136a4bbaeeb4325059dd50d9b40d20281306219f951c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: f8858599c91dbf01faa97c6b8afbb27c680441d29122d8e2e6ea7b8effe39622

MX_S_TRACE_PSD__randomized_adaptive__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 948825153b7d1542c8ba21a181967990ad1558e8cc47befc97b297a1690d7a7a

Retain the explicit universal constant 1/384 conditionally.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 801ad9bc834fd7f487ef71ba55c06324ee0b001fad8711ed6521fcb6bda6f221

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: 8b7c98546042f386487b2f940cefc4f0e6e15493f216a78e0bd3cd6178fea048

MX_S_TRACE_PSD__proof_uniform_confidence_wishart

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: defcad83993a8af7b1dfdbde4620ebe06e688427e5deeff9d79bb227c970356d

Accepted adaptive domain B; the historical posterior premise is not freshly recertified.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: b03554efe79dcc01c3446a0f9e34209131223097608bf45d05b3e4355c6ac45e

Frozen /bounds/12, hash 99191570a108dc5104236c31ea376e5016d1bbf81d98dea6f3c6129567dc949a; /proofs/3, hash d53440c5ae92d8938e60070893c939b7ab8ba8064c980ab1b2c25f44a49f9819.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 1662960571cf29476b13324157a82327772e7ecc0f5e0795a79f39c40bb89bac

#### Native item 1

Native pointer: /joint_analysis/provenance/5/source_refs/0; canonical SHA-256: fe2720c39605ebb591edb442844498d28d4ea50ef83279241cd33619181bcc9b

MX_SRC_FS

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: e1b6aa3eac87dc607cf262ea1dd54dc04b7b464a35f62a890ae582817d1dd61c

Adaptive B

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: 25832555df0dec37646275675c630f92cc53c6dfedf05dd1de81fe3d06af3241

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: 425a843c14c99bba18119fd9734504abe6a38a1633ca2361037028691bd47ee3

Retain the same native nonadaptive quantity and cost; add only c5 participation.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: 13fdbe3b11ca9b0a6ac59dff759e67129ed036d4e42c3f46479fe3c1ab17a147

Accepted native guard B; source theorem is not freshly recertified.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: b6f6cce3b457fa3a4cc6d3de739ab0cd869909191e2da6e680875e124c1db1db

Frozen /bounds/5, hash fc3b9f926b5ccbd2dce3cd72e02521be31d523fc523b7aa582e823f0ac3f6d8d.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: 762c7ba2c144631b14d7d2c1207918505744c751d87e6c0c3569537daf6bb7f7

#### Native item 1

Native pointer: /joint_analysis/provenance/6/source_refs/0; canonical SHA-256: 88548f1c0b63a134560cb2d59a92a94c287eaf5ed6a8a133b369b0cd7551e5dd

MX_SRC_NA

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 8

Native pointer: /joint_analysis/provenance/7; canonical SHA-256: 1a8c418a301d5f1ca12d94eb520463827bcfbfad61b627aad8b7acf4a93946ac

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/7/bound_id; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/7/mapping; canonical SHA-256: df3ba84735cd58f2c79f7003573c0e61960da11698f40761e3d5b9b8849340e9

Unchanged historical lower; redundancy in c5 is proved separately.

#### Native field: origin

Native pointer: /joint_analysis/provenance/7/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/7/source_domain; canonical SHA-256: af0b1236483b6d4b155e996474d8288cad9dbfd7072f37e4fb6741be60eb6c24

Accepted native source window H.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/7/source_locator; canonical SHA-256: 7553d1ca177e7c64b74154bfdddd4adbc7c919cbccb0fa5c9ced7df43d3c4b28

Frozen /bounds/6 and its native evidence.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/7/source_refs; canonical SHA-256: 89d7cf9474659f43f064745f0e046e2dcdd5d5fc292aa52d2c71c98d1df7b14e

#### Native item 1

Native pointer: /joint_analysis/provenance/7/source_refs/0; canonical SHA-256: 61babcf8875d3875227c52b040567845f43aa824fc6543f39b9c6f1dd645d8bc

MX_SRC_HPP

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/7/target_domain; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 9

Native pointer: /joint_analysis/provenance/8; canonical SHA-256: fedd978c020d07c72c9b7641c6ca78cb86b0ea9994488d92112bb7ae47b7eb78

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/8/bound_id; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/8/mapping; canonical SHA-256: 96e302f6fab88087fd9bef91ed38408b126322e62c84b5d9fbe6951ee46d4d1b

Retain exact reconstruction with d preselected vector products; add c5 participation.

#### Native field: origin

Native pointer: /joint_analysis/provenance/8/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/8/proof_refs; canonical SHA-256: 2f186a46b1d9be40e4cfbac5bfbc3f48f1c6969a440c20c234d191c2ee3cde34

#### Native item 1

Native pointer: /joint_analysis/provenance/8/proof_refs/0; canonical SHA-256: aee8f51cfdd095f53b836439070df847ec39582a2ebb521efbcfe9b33677349d

SIX_PROOF_7ed1f0347d6b

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/8/source_domain; canonical SHA-256: ae9c9256a568e1ec7be8c75887b81bfd56a1e15ee9fea32974d15ea1b82c2877

Accepted native guard B.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/8/source_locator; canonical SHA-256: 8011528c12ee6425db03db19f8650052c3ba8124557c977ac568f09aa1f2c942

Frozen /bounds/7, hash 4fcc5123c7a8149063d87ce8302817aff35f7deff767927005822efcca19d7a4.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/8/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/8/target_domain; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native item 10

Native pointer: /joint_analysis/provenance/9; canonical SHA-256: ad2f49aadac7f18cbca2674de87882584d659ea80eca13002098649a0d55a0c2

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/9/bound_id; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/9/mapping; canonical SHA-256: 99f91bd53645a75920df16add9c4d72e8db5f9d747b00ed5114ba6c6f5b4f4a3

Conditionally retain the unchanged all-dimension slice lower.

#### Native field: origin

Native pointer: /joint_analysis/provenance/9/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/9/proof_refs; canonical SHA-256: be0f58720543eabcdd516b831c07b68be3e31fbbead8057e5fd8d34e6f5ebbdf

#### Native item 1

Native pointer: /joint_analysis/provenance/9/proof_refs/0; canonical SHA-256: 5d7cde343e7066e436463b1bf1e6d75b1d4c787e1aa8cf733362b1f0980dd9f0

SIX_PROOF_b3242221f506

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/9/source_domain; canonical SHA-256: d8169e118707c7e2de40a45c811beeb0d08c34e42cc27921a9558032d711a716

Accepted native guard S.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/9/source_locator; canonical SHA-256: aa01d75a9a0019f69c155f9ab40ce044d5512814d89f361bf4fcab5ff7d55246

Frozen /bounds/8 and its registered derivation.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/9/source_refs; canonical SHA-256: ad9486d8ffa44d7d528fde185cc1a241de3dfb3991254375c6cb02fe722d4f28

#### Native item 1

Native pointer: /joint_analysis/provenance/9/source_refs/0; canonical SHA-256: fe2720c39605ebb591edb442844498d28d4ea50ef83279241cd33619181bcc9b

MX_SRC_FS

#### Native item 2

Native pointer: /joint_analysis/provenance/9/source_refs/1; canonical SHA-256: fc8389352f8fe8aa765d983280ab1e22a9e1392914083a648f803c48ae870522

MX_SRC_BH

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/9/target_domain; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native item 11

Native pointer: /joint_analysis/provenance/10; canonical SHA-256: 2d839c7fbd622ea045963a5e85fb7b7f730d474119ed64903725238f166d4735

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/10/bound_id; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/10/mapping; canonical SHA-256: 59291074c975fb8714fb84589ae320b757eaca7c23a106b6f9d979c7c3ad2a78

Retain F on exactly G; c5 does not extend its source applicability.

#### Native field: origin

Native pointer: /joint_analysis/provenance/10/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/10/source_domain; canonical SHA-256: d0e4835403d586be83ad1b8221450bde8225ac680a38a62a95cbd3d78676a562

Accepted native guard G and its original piecewise branch threshold.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/10/source_locator; canonical SHA-256: 59dd0defaa9e921c076496c1554126fb1abe31249748cad278d930e285e77d8f

Frozen /bounds/9, hash d75972c10cba06095ec799e36bf959467c21902662bbcffd1750fb0bdafc2801, with /regimes/6.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/10/source_refs; canonical SHA-256: 762c7ba2c144631b14d7d2c1207918505744c751d87e6c0c3569537daf6bb7f7

#### Native item 1

Native pointer: /joint_analysis/provenance/10/source_refs/0; canonical SHA-256: 88548f1c0b63a134560cb2d59a92a94c287eaf5ed6a8a133b369b0cd7551e5dd

MX_SRC_NA

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/10/target_domain; canonical SHA-256: cb12e0f869002fc63cc2bba949c3b8b42b95c3b1a315f35f9dd07f9062da317b

G only

#### Native item 12

Native pointer: /joint_analysis/provenance/11; canonical SHA-256: 25d963160cd5325864e51624bbc707d53f261f2b68a1d624849389854f282359

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/11/bound_id; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/11/mapping; canonical SHA-256: 2bf43f089160d9cf0fd22cfe650ad569badf32e274bfa9aef5d4683a64d49319

Conditional retention of exact zero upper cost.

#### Native field: origin

Native pointer: /joint_analysis/provenance/11/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/11/proof_refs; canonical SHA-256: e649f22df3ad00177b4cf9d89e5a6dca3c6880624065b00aa68d173495f7813e

#### Native item 1

Native pointer: /joint_analysis/provenance/11/proof_refs/0; canonical SHA-256: 12b3c71176961dc7cb645db1566057cf450be952200b163554e3674455b68977

SIX_PROOF_369230c34039

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/11/source_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/11/source_locator; canonical SHA-256: 1676d5f3a6c3c40bf5a2f992fe5db6abfd26356b65eda4bd95fa3a76a7bbe32a

Frozen nonadaptive zero-output bound.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/11/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/11/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 13

Native pointer: /joint_analysis/provenance/12; canonical SHA-256: 42f19b83001388d8c3a2ff177534ae533ce8ab26cd63df9a8cfff85c1e0208f7

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/12/bound_id; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/12/mapping; canonical SHA-256: 8375035318a86ed75eef33a46082b6288936c8903370017f75a673824e1e4399

Conditional retention of exact zero lower cost.

#### Native field: origin

Native pointer: /joint_analysis/provenance/12/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/12/proof_refs; canonical SHA-256: e649f22df3ad00177b4cf9d89e5a6dca3c6880624065b00aa68d173495f7813e

#### Native item 1

Native pointer: /joint_analysis/provenance/12/proof_refs/0; canonical SHA-256: 12b3c71176961dc7cb645db1566057cf450be952200b163554e3674455b68977

SIX_PROOF_369230c34039

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/12/source_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/12/source_locator; canonical SHA-256: a87813ba6d0ffee280ed31e64ec9e1921aa185f635cf4910932f43fc1bed2c53

Frozen nonadaptive nonnegative-cost bound.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/12/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/12/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 14

Native pointer: /joint_analysis/provenance/13; canonical SHA-256: cbed642853b995c02391c01a7858813e6e3aaf5cc4a4897fb27bb181377f82ed

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/13/bound_id; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: mapping

Native pointer: /joint_analysis/provenance/13/mapping; canonical SHA-256: d27ea892cc74a7672e8e1afc014f7aee7b1eacb99d280edd46204684d4c9c8a8

N*_nonadaptive>=N*_adaptive by identical-seed, identical-query, identical-output simulation preserving every fixed-input probability and worst-case query count. Native quantity identities are not merged.

#### Native field: origin

Native pointer: /joint_analysis/provenance/13/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/13/proof_refs; canonical SHA-256: 67aa6a1393f7c376ea8fa7c4b5240b0b9bd359e5ac540437b3a6784e5f64cd28

#### Native item 1

Native pointer: /joint_analysis/provenance/13/proof_refs/0; canonical SHA-256: 546ac7803c4ddd5e1b9ed40f6ba2b2ab3abb00942fa68c56e9ad552cfde66305

MX_S_TRACE_PSD__randomized_nonadaptive__proof_uniform_confidence_transfer

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/13/source_domain; canonical SHA-256: 931e507d2d94b12a9e0ab50c1f932a6ff8161918ae8c4836051139752c5f9aa5

Adaptive B, conditionally retained.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/13/source_locator; canonical SHA-256: b13778fcc30a60ccf2ea7687f4f489dcdcc946f68516026a7ee434ad791af8fa

Exact retained premises /bounds/12 and /proofs/3, with both fully read native views and the unchanged common contract.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/13/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/13/target_domain; canonical SHA-256: 7e3ee3e8d772d26c8c33ef67b478c263aa91a81772fe58a8e45523fffd301c02

Nonadaptive B

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 8686ea154e87685de9a5370a374b6e71889d6b17ba7046590c56b564efeb198c

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 0762f72fe77f76454ac8da2f909b1c42551948a8197d4de473bf5c027f16c524

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/6; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/7; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: cdcb5bcdd8602956a6e2633f01efc2cf561a82c14cdcbc5b99ba84e6eb62530d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 849a95f13a4142be8c4a32d3594dce103e12061eabe76d8429f6bbe86d1e6b6a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 98dc4c01164956635ebf7414c07b691b979a5f25e25f00309d826ac083c46604

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 2f0156adff42ef581328cd85593ef712c41250e940cfea824a6148e65d28c754

MX_S_TRACE_PSD__randomized_adaptive__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 3e69e3715b7256da62149876e495f4a1e36b0c2bf45062c89176528b5b19951f

MX_S_TRACE_PSD__randomized_adaptive__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 4412bdeae414db1f76d3b75d981614e1631fd25f38c812a8634c407269f6871e

MX_S_TRACE_PSD__randomized_adaptive__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: e078e74e3b7ba87947c418dc94710de8a32dda6d5533fb192015a96172654066

MX_S_TRACE_PSD__randomized_adaptive__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/4; canonical SHA-256: ebfd4116c4045acbeaf84de067dff48ac014d1d84cce01052e4b9454af31389b

MX_S_TRACE_PSD__randomized_adaptive__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/5; canonical SHA-256: f8858599c91dbf01faa97c6b8afbb27c680441d29122d8e2e6ea7b8effe39622

MX_S_TRACE_PSD__randomized_adaptive__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: c6f7433292f1766896006a1e20df6212ee39ded1c88dd641d00828a2e59aa705

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: cbd717faae83a18dcd0984f69326879d0fe1418a4573e90441638e7d8eb23ec6

synthesis-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: e40b5c504f3bafd7c7475ef08a3fa7f06175d2501e8cc404ed179833619cbcf5

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 98dc4c01164956635ebf7414c07b691b979a5f25e25f00309d826ac083c46604

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 2f0156adff42ef581328cd85593ef712c41250e940cfea824a6148e65d28c754

MX_S_TRACE_PSD__randomized_adaptive__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 3e69e3715b7256da62149876e495f4a1e36b0c2bf45062c89176528b5b19951f

MX_S_TRACE_PSD__randomized_adaptive__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 4412bdeae414db1f76d3b75d981614e1631fd25f38c812a8634c407269f6871e

MX_S_TRACE_PSD__randomized_adaptive__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: e078e74e3b7ba87947c418dc94710de8a32dda6d5533fb192015a96172654066

MX_S_TRACE_PSD__randomized_adaptive__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/4; canonical SHA-256: ebfd4116c4045acbeaf84de067dff48ac014d1d84cce01052e4b9454af31389b

MX_S_TRACE_PSD__randomized_adaptive__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/5; canonical SHA-256: f8858599c91dbf01faa97c6b8afbb27c680441d29122d8e2e6ea7b8effe39622

MX_S_TRACE_PSD__randomized_adaptive__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 49a94edc9c411e04827423e8892de96f0e83ec4fb458bf3e246216d0b23af207

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: ebcba919e62a1ab3932a5511960ae541204ef3e4e612a3e2b58eaa7aea342c2d

synthesis-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: a4c958a40c5ebe10df0990f0f85b543e5ceb99f5066c372a0e95a659d6d161c8

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 98dc4c01164956635ebf7414c07b691b979a5f25e25f00309d826ac083c46604

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: 2f0156adff42ef581328cd85593ef712c41250e940cfea824a6148e65d28c754

MX_S_TRACE_PSD__randomized_adaptive__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 3e69e3715b7256da62149876e495f4a1e36b0c2bf45062c89176528b5b19951f

MX_S_TRACE_PSD__randomized_adaptive__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 4412bdeae414db1f76d3b75d981614e1631fd25f38c812a8634c407269f6871e

MX_S_TRACE_PSD__randomized_adaptive__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: e078e74e3b7ba87947c418dc94710de8a32dda6d5533fb192015a96172654066

MX_S_TRACE_PSD__randomized_adaptive__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: ebfd4116c4045acbeaf84de067dff48ac014d1d84cce01052e4b9454af31389b

MX_S_TRACE_PSD__randomized_adaptive__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/5; canonical SHA-256: f8858599c91dbf01faa97c6b8afbb27c680441d29122d8e2e6ea7b8effe39622

MX_S_TRACE_PSD__randomized_adaptive__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: bc9a904605c4007dffe2a827e5ef9bf03a1a90555d96c0118583325b3253349d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: eecc36923da93fc169f44f255e81f6fb35dab18e1d6dd53caf186a6ad6dd5a34

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 70d219e1a5f7c099a40d944da19a229b7416f11874de1dd2ddb1b48607f973a1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/3; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/4; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/5; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/6; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/7; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: aaf70ef0907925e194e054eb5d061c1b7b06379829f9aa158e998d53fc7e4aeb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 64086e23e4a79d242245e030112900f5b07242d346577c3261e432904c932a39

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 70d219e1a5f7c099a40d944da19a229b7416f11874de1dd2ddb1b48607f973a1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/3; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/4; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/5; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/6; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/7; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: d1fcb61ff18a2af1ff4ee55a5d53978ad303cf4a0aa5f3748dbfcb25b09ad32a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: ff826fbeddde135e8fb4fdeb406ca932a4bb89a2994ae07975ddc47f4ba8bd93

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 70d219e1a5f7c099a40d944da19a229b7416f11874de1dd2ddb1b48607f973a1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/0; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/1; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/2; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/3; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/4; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/5; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/6; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/7; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 3710f4759b3165c69f24d2f4f57d5b70a959cf9eec07414cb8b1c46056f51701

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 24f6b1ca503a88ccab47226cd3751e0fafb80a364be083110d4c565bd2017c07

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 70d219e1a5f7c099a40d944da19a229b7416f11874de1dd2ddb1b48607f973a1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/0; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/1; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/2; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/3; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/4; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/5; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/6; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/7; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 0c448c0cf35868e1a8979bfff9cbaf79ebc8e93239402a68bd93e610fc20a6db

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 70acb55b992a0e80c9ffb36f8a1b5d6a7ba663b4561a6c58a7441071ecefad3b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 70d219e1a5f7c099a40d944da19a229b7416f11874de1dd2ddb1b48607f973a1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/0; canonical SHA-256: 651d8acc17ef1534a435ea5b4e1eff500d48f00645c80a32e9839e749ac958bd

MX_S_TRACE_PSD__randomized_nonadaptive__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/1; canonical SHA-256: d0e50500959262a17f7e2c8d245f450b1dd2a0611b3386d6f16ac44348f5716f

MX_S_TRACE_PSD__randomized_nonadaptive__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/2; canonical SHA-256: 7f951644197e96205e0eb66b747e35470cf93cc21abda0da7b954073da85fae0

MX_S_TRACE_PSD__randomized_nonadaptive__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/3; canonical SHA-256: de4241e3e9eb57cbc85cc62e9604932da913ed6e1e53b139d1f64d1ce605d136

MX_S_TRACE_PSD__randomized_nonadaptive__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/4; canonical SHA-256: a5cad6971345e2a38ebc0b4c727623d1f987b896bc7f3e09b3e8970eb07cd569

MX_S_TRACE_PSD__randomized_nonadaptive__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/5; canonical SHA-256: 1dad71adcdad219e11b29367b30844af821179477cfff6cd18d58a59eb4537a1

MX_S_TRACE_PSD__randomized_nonadaptive__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/6; canonical SHA-256: 9e7c3be875fbedbd213bdbf13ee7c7ef1a5145991d42a2799061adaec571ad47

MX_S_TRACE_PSD__randomized_nonadaptive__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/7; canonical SHA-256: b7fc12f1478d382b501f174cbfb3309e4fcf576d55c46c9c00cf9857712e2319

MX_S_TRACE_PSD__randomized_nonadaptive__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 197d864436f42e30608f6db8d3e759883201557392fe1f84ee29746a8eaf777f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: f1d7c1b829959acf5fd8b22ab6c75fdbf1b3810e2c3ef78a394693a9a0260546

synthesis-7

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: f9311c9522b1bf1f9679a2bf19c548e3806b84b391bb6638d716e2e6e56214c9

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 0762f72fe77f76454ac8da2f909b1c42551948a8197d4de473bf5c027f16c524

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/2; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/3; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/4; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/5; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/6; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/7; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: bb2e91ac0444646d75c34ba803288aa836998eebfade8f29e64a4a1f3bd750ed

Independent review of the new class transfer and guarded synthesis, retaining rather than recertifying the exact cited baseline premises.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 9695a0d33ed17c06ea05b564152208df4f7abb13e6718af3238ca7a2de2f328e

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 0762f72fe77f76454ac8da2f909b1c42551948a8197d4de473bf5c027f16c524

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/2; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/3; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/4; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/5; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/6; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/7; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 5eaf5e9aca4aa8ad3e56045a91acae9f74082e3c71ebe21b4fe37bfdce85e4df

Complete the formal static lower-bound and PSD-transfer investigation for arXiv:2209.15219v1, source e8895c0e3a4005a745fbee15eb91acafbdfbe5be855e9dd976b8cc96c254059f. Ranges [9000,19000) and [26000,36000) were read; formal Theorem 4.2 around PDF pp.8-9 and its proof were not read. No result from this paper is adopted.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: 8f069fbcd8b7f226586622ddc98ad1c01ea0e9a32fbdced64bf22680d3bd70c8

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 0762f72fe77f76454ac8da2f909b1c42551948a8197d4de473bf5c027f16c524

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/1; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/2; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/3; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/4; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/5; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/6; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/7; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 39941816445188760cb5755fa747852be66b4857556eb190737fd84a7145d1f4

Read potentially relevant theorem and parameter dependence in arXiv:2109.10659v3, 2505.12289v2 and 2506.22701v1. Metadata is not theorem evidence.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: 13db854dd14b7579f33e60741c5f5495fd5cd8481f08d8809fc2ccf28914f757

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: 0762f72fe77f76454ac8da2f909b1c42551948a8197d4de473bf5c027f16c524

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/1; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/2; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/3; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/4; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/5; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/6; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/7; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: ef2dfc27fbdb97cebf6743ef9e795df45c6ed07472d24cdc42eccbcf20debce6

All 18 records of terminal metadata search 2556a242906f562713c1c68b6202d4cc09e638590a405a07d821d2d9bf8d8756 were exposed. Relevant source assessment and a complete correction/version investigation remain unfinished; no exhaustive literature or globally sharp confidence claim.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/obligations/12; canonical SHA-256: 766db3c727e17bc92c22e723b3131fb4949c3c569ef01ae3131755040b3abfe5

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids; canonical SHA-256: 0762f72fe77f76454ac8da2f909b1c42551948a8197d4de473bf5c027f16c524

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/0; canonical SHA-256: dc86d044a1ea2b4f9df2a910d3ed72238c50fe5e96ed2dcd7d948ddfcd72619d

MX_S_TRACE_PSD__randomized_adaptive__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/1; canonical SHA-256: fbbe86b66ceef996160e3f4d75e0c87a259e4b2df69f14f9c99c22b0fe90258a

MX_S_TRACE_PSD__randomized_adaptive__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/2; canonical SHA-256: 863dd20bc140e63750b3211c7761132b276f950dfae9f300984df88ad5d30c6b

MX_S_TRACE_PSD__randomized_adaptive__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/3; canonical SHA-256: ebab259398f47bf508c451f104487a7ef443afa087476ca3c25f96f69cc763ef

MX_S_TRACE_PSD__randomized_nonadaptive__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/4; canonical SHA-256: 7d2171205b34d1e93bd27887bac15145937889ced6102ce48d7c8f82685112a1

MX_S_TRACE_PSD__randomized_nonadaptive__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/5; canonical SHA-256: 54be5b72b81a9a30c38d24d4b8443ede4c1ac14837a1cbd990f364569102f279

MX_S_TRACE_PSD__randomized_nonadaptive__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/6; canonical SHA-256: 6ed11a9730b93897fab015a08168a89b624b85259570bb32f830f567ae2a2d45

MX_S_TRACE_PSD__randomized_nonadaptive__c4

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/7; canonical SHA-256: 46a069534d87fa8047216420b16c6bfd5530240f61102fa337f90a0f98b6b846

MX_S_TRACE_PSD__randomized_nonadaptive__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 682cdf0aaaefb2345f60efa76031e63ce49eec1af9bba92205718cf72d558365

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 69f57556becd56db7b5380274964cab8de295f67066d8d16881d27807b170d4d

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 96ba1db06ac590c41ca30eb921b08bb21f8492b1ce87474205455697191883f5

Both registered views separately: integer d>=1, epsilon>0, 0<delta<1/2. B denotes integer d>=1, 0<epsilon<1, 0<delta<1/2. Z denotes integer d>=1, epsilon>=1, 0<delta<1/2. S denotes B AND delta=1/10. H denotes S AND epsilon<=c AND d>=d_0(epsilon), with the retained universal source constant and threshold. G denotes B AND delta<=exp(-4) AND epsilon<=1/4 AND d>=C*(sqrt(L)/epsilon+L), exactly the retained nonadaptive r4 guard. Set m=min{d,1/epsilon}, U=sqrt(L)/epsilon+L. Only on G define F=sqrt(L)/epsilon when epsilon<=c_0/sqrt(L), and F=L/log(L) otherwise; C and c_0 are retained universal constants, not varying structural parameters. The native adaptive and nonadaptive quantities remain distinct minimax fixed worst-case N_right costs.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 34e62a40073a427a384f80948993f97d1003b047db90d7416e19c844aa1cbb28

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 3ebf62be93481b0b519a3c2f9bbdf6f1de7443960f0501388e2ad9af76bcabbe

MX_S_TRACE_PSD_p_1d1d52d4bc

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: e1b7aa89e5bf7ae3cdac89ab2c85e63f4d04fdf92719293d0df87cefbae6b494

MX_S_TRACE_PSD_p_790a70d659

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: b1b705fa457ecaac854a89b70946c31c0f55472fd6aab25af18c757cac7646e4

MX_S_TRACE_PSD_p_c8bdef7655

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 2c038c3aa0f894a332a8d212dbc4fca8600e696fb6ae5dc1ab66b3e0ade61174

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 2e34e004bc77d9107fc1305bd3b45478b6f94a2000acbd20926c68cd86103e7e

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: 9d4c962b29573370e2c7ce71eb54008964683ecf0c2631695c500c13e577abbd

L=log(1/delta), natural logarithm. This dimensionless confidence coordinate has inverse delta=exp(-L), with L>log(2); uniformity remains in the native delta parameter.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: fe35e51a7ebedaacf183182a5d6be8680bae544a7c5047fd9d7cf7632890fafa

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: b1b705fa457ecaac854a89b70946c31c0f55472fd6aab25af18c757cac7646e4

MX_S_TRACE_PSD_p_c8bdef7655

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 8463f556f97cf8fdcda977c053a5ff1b530500723772b0f884160d04256ad2fa

L

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 34e62a40073a427a384f80948993f97d1003b047db90d7416e19c844aa1cbb28

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 3ebf62be93481b0b519a3c2f9bbdf6f1de7443960f0501388e2ad9af76bcabbe

MX_S_TRACE_PSD_p_1d1d52d4bc

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: e1b7aa89e5bf7ae3cdac89ab2c85e63f4d04fdf92719293d0df87cefbae6b494

MX_S_TRACE_PSD_p_790a70d659

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: b1b705fa457ecaac854a89b70946c31c0f55472fd6aab25af18c757cac7646e4

MX_S_TRACE_PSD_p_c8bdef7655

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Mark Braverman; Elad Hazan; Max Simchowitz; Blake Woodworth. The Gradient Complexity of Linear Regression. 2020. COLT 2020 PMLR 125 PDF, 21 pages.

https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf

[2] Noah Amsel; Tyler Chen; Feyza Duman Keles; Diana Halikias; Cameron Musco; Christopher Musco. Fixed-sparsity matrix approximation from matrix-vector products. 2026. Mathematical text checked in arXiv:2402.09379v3 (2024-03-26); SIMAX 47(2), 2026 publication.

https://arxiv.org/pdf/2402.09379v3

[3] Raphael A. Meyer; Cameron Musco; Christopher Musco; David P. Woodruff. Hutch++: Optimal Stochastic Trace Estimation. 2021. arXiv:2010.09649v5; 2021-06-11 (PDF dated June 14).

https://arxiv.org/pdf/2010.09649v5

[4] Shuli Jiang; Hai Pham; David P. Woodruff; Qiuyi (Richard) Zhang. Optimal Sketching for Trace Estimation. 2021. NeurIPS 2021 proceedings PDF, 13 pages.

https://proceedings.neurips.cc/paper/2021/file/c77bfda61a0204d445185053e6a9a8fe-Paper.pdf
