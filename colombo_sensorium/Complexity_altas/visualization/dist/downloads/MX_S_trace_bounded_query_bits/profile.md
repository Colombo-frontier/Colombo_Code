# PSD trace estimation with finite-bit integer queries.

**Setting ID.** `MX_S_trace_bounded_query_bits`

Matrix computation

Estimate $\tau=\operatorname{tr}(A)$ for an unknown positive semidefinite matrix.

**Status.** Fully optimal

**TASK tags.** task family: Matrix computation

**MODEL tags.** spectral structure: Explicit matrix class; spectral structure: Real psd

**ORACLE tags.** feedback quality: Exact; interface family: Bounded integer exact response; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Scalar

**METRIC tags.** criterion: Relative trace error

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** measure: N right

## 1. Setting specification

### Task

Estimate $\tau=\operatorname{tr}(A)$ for an unknown positive semidefinite matrix.

### Admissible model

Assume $A=A^{\mathsf T}\succeq0$ and $A\in\mathbb{R}^{d\times d}$, allow $A=0$, and use query-alphabet parameter $b_{\mathrm{q}}\in\mathbb{Z}_{\ge0}$.

### Oracle interface

Inputs $d,\varepsilon,b_{\mathrm{q}}$ are public and $A$ hidden. A query chooses $v\in\mathbb{Z}^d\cap[-2^{b_{\mathrm{q}}},2^{b_{\mathrm{q}}}]^d$ and returns the exact real vector $Av$. Responses are not quantized and always use the same fixed matrix.

### Output

Return a scalar $\widehat\tau\in\mathbb R$, without an additional certificate.

### Loss or accuracy criterion

The success event is $|\widehat\tau-\operatorname{tr}(A)|\le\varepsilon\operatorname{tr}(A)$. A zero-trace input requires an output of exactly zero.

### Resource accounting

Count right products with single vectors only: $N=N_{\mathrm r}$. A block of width $q$ costs $q$ calls.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using public inputs only. For every admissible input fixed before the private seed is drawn, the success event has probability at least $0.9$ over that seed.

**Budget convention.** fixed worst-case joint budget; no expectation substituted

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$\varepsilon$: Absolute-error proportion relative to the nonnegative true trace **Domain:** $\varepsilon>0$.

$|\widehat\tau-\operatorname{tr}(A)|\le\varepsilon\operatorname{tr}(A)$

$b_{\mathrm q}$: Amplitude exponent for permitted integer query coordinates **Domain:** $b_{\mathrm q}\in\mathbb Z_{\ge0}$.

$v_i\in\mathbb Z,\quad |v_i|\le2^{b_{\mathrm q}}$

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

$v$: One admissible integer query vector. **Domain:** $\mathbb Z^d\cap[-2^{b_{\mathrm q}},2^{b_{\mathrm q}}]^d$.

$e_i$: The $i$th standard basis vector **Domain:** $1\le i\le d$.

$(e_i)_j=\mathbf1\{i=j\}$

$\mathcal R$: Rademacher probe distribution **Domain:** Each coordinate independently equals +1 or −1 with probability 1/2.

$N,N_{\mathrm r}$: Single-vector query budget for exact right products Av. A block is charged by its column count. **Domain:** $\mathbb N_0$.

$N=N_{\mathrm r}$

$N^\star$: Minimum worst-case query budget attaining this profile's success guarantee **Domain:** $\mathbb N_0\cup\{+\infty\}$.

The quantity is $N^\star=\inf_{\mathcal A}\sup_{I,\omega}N_{\mathcal A}(I,\omega)$, where the infimum ranges over admissible algorithms satisfying this profile's success guarantee.

$\mathcal A,I,\omega$: The algorithm, fixed admissible input, and private algorithmic seed. **Domain:** Quantifiers for worst-case input and execution cost. Success probability is taken over ω.

$a_0$: Scale ratio in the two-scale construction for larger errors. **Domain:** A positive auxiliary proof parameter.

$a_0>(1+\varepsilon)/(1-\varepsilon)\quad(0<\varepsilon<1)$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon;d,b_{\mathrm q})
$$

**Scope.** Choose one algorithm, then require the relevant error guarantee for every fixed input in the complete specification. Cost is a worst-case hard budget.

**Optimization direction.** minimize

### R1 - Regime covered by the communication lower-bound reduction

**Region.** Assume $d\ge C/\varepsilon$, $0<\varepsilon<c$, and integer $b_{\mathrm{q}}\ge0$, with source sufficient dimension constant $C\ge1$ and accuracy constant $0<c\le1/2$. The communication-reduction bound is retained, but the explicit Wishart lower bound is stronger on this region.

**Quantity.** Q1

**Resource.** $N=N_{\mathrm{r}}$

**Status.** Optimal

**Lower bound.** B3

$$
\Omega(1/\varepsilon)
$$

**Upper bound.** B1, B4

$$
O(1/\varepsilon)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** This window satisfies $0<\varepsilon<1$, so Rademacher NA-Hutch++ and the explicit Wishart lower bound apply. Since $d\ge C/\varepsilon$ and $C\ge1$, we have $\min\{d,1/\varepsilon\}=1/\varepsilon$. The communication lower bound remains an individual evidence record; the stronger posterior lower bound and admissible upper bound determine the status.

### R2 - Nontrivial full-accuracy regime with integer query counts

**Region.** Require $d\ge1$, integer $b_{\mathrm{q}}\ge0$, and $0<\varepsilon<1$. The fixed success probability is $0.9$.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Optimal

**Lower bound.** B3

$$
\Omega(\min\{d,\varepsilon^{-1}\})
$$

**Upper bound.** B1, B4

$$
O(\min\{d,\varepsilon^{-1}\})
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** Rademacher and standard-basis queries are admissible when $b_{\mathrm{q}}=0$. The explicit Wishart lower bound holds for all $0<\varepsilon<1$ in the broader class of arbitrary randomized adaptive real queries, hence also for the integer-box interface.

### R3 - Zero-query endpoint at coarse accuracy

**Region.** Assume $d\ge1$, $\varepsilon\ge1$, and integer $b_{\mathrm{q}}\ge0$, with fixed success probability $0.9$.

**Quantity.** Q1

**Resource.** $N=N_{\mathrm{r}}$

**Status.** Optimal

**Lower bound.** B6

$$
0
$$

**Upper bound.** B5

$$
0
$$

**Gap or comparison.** The optimal query count is exactly $0$. No ratio with zero denominator is formed.

**Comparison argument.** Positive semidefiniteness gives $\tau\ge0$. When $\varepsilon\ge1$, outputting zero has error $\tau$, which is at most $\varepsilon\tau$. Since query counts are nonnegative, the optimum is exactly zero.

## 4. Bounds and supporting evidence

### B1 - Nonadaptive Hutch++ with Rademacher probes and fixed failure probability 0.1

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le C\varepsilon^{-1}
$$

**Sources.** [3](https://arxiv.org/pdf/2010.09649v5)

**Oracle correspondence.** All probe coordinates are $\pm1$, hence legal for every $b_{\mathrm q}\ge0$. Internal postprocessing may use reals.

**Resource conversion.** Each matrix-vector product has unit cost; this is not communication bit complexity.

**Constants.** Fixed declared regularity and initialization budgets; no unlisted joint-parameter optimality is asserted.

**Source location.** [3](https://arxiv.org/pdf/2010.09649v5) pdf pages: 7; 8; 9; theorem or section: Algorithm 2; Theorems 6–7; proof of Theorem 7; theorem: Algorithm 2; Theorems 6–7; proof of Theorem 7

NA-Hutch++ in HPP Algorithm 2 and Theorem 6 queries only Rademacher vectors and uses $O(1/\varepsilon)$ products at fixed success probability; these queries are admissible for every $b_q\ge0$. The communication reduction in Theorem 7 restricts integer query coordinates to magnitude at most $2^{b_q}$ while keeping responses exact. Its hard instances have dimension of order $\varepsilon^{-1}$.

**Source location.** [3](https://arxiv.org/pdf/2010.09649v5) theorem: Algorithm 2 lines 2–4; Theorem 6; pdf pages: 7

In arXiv:2010.09649v5, page 7, line 2 of Algorithm 2 chooses all entries of $S,R,G$ independently from $\pm1$. The only native queries are $AS,AR,AG$. Pseudoinverses and composite matrices in line 4 are internal computations on these responses, without queries along new real vectors. Theorem 6 gives $O(\log(1/\delta)/\varepsilon)$ calls. Setting $\delta=0.1$ yields an admissible $O(1/\varepsilon)$ upper bound for every $b_{\mathrm q}\ge0$.

### B2 - A Gap-Hamming communication reduction allowing randomized adaptive integer queries.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge\frac{c}{\varepsilon\,[b_{\mathrm{q}}+\log(1/\varepsilon)]}
$$

**Sources.** [3](https://arxiv.org/pdf/2010.09649v5)

**Oracle correspondence.** Query coordinates are restricted while responses remain exact. The lower bound applies only in the source construction's dimension window.

**Constants.** Fixed declared regularity and initialization budgets; no unlisted joint-parameter optimality is asserted.

**Source location.** [3](https://arxiv.org/pdf/2010.09649v5) pdf pages: 7; 8; 9; theorem or section: Algorithm 2; Theorems 6–7; proof of Theorem 7; theorem: Algorithm 2; Theorems 6–7; proof of Theorem 7

NA-Hutch++ in HPP Algorithm 2 and Theorem 6 queries only Rademacher vectors and uses $O(1/\varepsilon)$ products at fixed success probability; these queries are admissible for every $b_q\ge0$. The communication reduction in Theorem 7 restricts integer query coordinates to magnitude at most $2^{b_q}$ while keeping responses exact. Its hard instances have dimension of order $\varepsilon^{-1}$.

### B3 - Conditional Wishart trace anti-concentration and transfer from arbitrary real queries to bounded integer queries.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c\min\{d,\varepsilon^{-1}\}
$$

**Sources.** [2](https://arxiv.org/pdf/2402.09379v3) [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf)

**Oracle correspondence.** Integer-box queries form a subset of arbitrary real queries, so the lower bound transfers from the stronger to the weaker interface.

**Guarantee conversion.** Success probability $0.9$ is stronger than $2/3$ in D10. D10's large-error branch extends this result to all $0<\varepsilon<1$.

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

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

**Local argument.** A1

**Source location.** [2](https://arxiv.org/pdf/2402.09379v3) theorem: Proposition 3; section: Appendix B.1

**Source location.** [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf) theorem: Lemma 13; section: Appendix C.2; pdf pages: 11

**Source location.** [2](https://arxiv.org/pdf/2402.09379v3) theorem: Proposition 3; proof in Appendix B.1; section: §3.1; Appendix B.1; pdf pages: 11; 22; 23

FS Proposition 3 and Appendix B.1 state the unnormalized form of the same adaptive Wishart posterior. Conditional on the complete query transcript and independent private seed, the residual block remains an independent Wishart matrix.

### B4 - Deterministic standard-basis reconstruction.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

**Derivation.** Query every standard basis vector, collect all columns, then sum the diagonal with free internal computation.

**Local argument.** A2

### B5 - Deterministically return zero.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le0
$$

**Conditions.** Assume $d\ge1$, $\varepsilon\ge1$, and integer $b_{\mathrm q}\ge0$, with fixed success probability $0.9$.

**Guarantee conversion.** Deterministic success for every instance, satisfying the setting's probability requirement.

**Resource conversion.** No matrix-vector product is queried, and every resource count is zero.

**Constants.** No hidden constant

**Local argument.** A3

### B6 - Nonnegative query count

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge0
$$

**Conditions.** Assume $d\ge1$, $\varepsilon\ge1$, and integer $b_{\mathrm q}\ge0$, with fixed success probability $0.9$.

**Guarantee conversion.** Deterministic success for every instance, satisfying the setting's probability requirement.

**Resource conversion.** No matrix-vector product is queried, and every resource count is zero.

**Constants.** No hidden constant

**Local argument.** A3

## 5. Local arguments

### A1 - standard Wishart posterior plus chi-square anti-concentration

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

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

**Sources.** [2](https://arxiv.org/pdf/2402.09379v3) [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf)

### A2 - Deterministic standard-basis reconstruction.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Every standard basis vector is a valid bounded-integer query for all allowed $b_{\rm q}\ge0$. Query all $d$ basis vectors and sum the returned diagonal entries. This gives exact trace with deterministic success and uses $d$ queries.

### A3 - Deterministically return zero.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

For epsilon>=1, positive semidefiniteness gives tr(A)>=0, and the deterministic output zero satisfies |0-tr(A)|=tr(A)<=epsilon tr(A). No query is used. Since query cost is nonnegative, the optimum is exactly zero.

## References

[1] Mark Braverman; Elad Hazan; Max Simchowitz; Blake Woodworth. The Gradient Complexity of Linear Regression. 2020. COLT 2020 PMLR 125 PDF, 21 pages.

https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf

[2] Noah Amsel; Tyler Chen; Feyza Duman Keles; Diana Halikias; Cameron Musco; Christopher Musco. Fixed-sparsity matrix approximation from matrix-vector products. 2026. Mathematical text checked in arXiv:2402.09379v3 (2024-03-26); SIMAX 47(2), 2026 publication.

https://arxiv.org/pdf/2402.09379v3

[3] Raphael A. Meyer; Cameron Musco; Christopher Musco; David P. Woodruff. Hutch++: Optimal Stochastic Trace Estimation. 2021. arXiv:2010.09649v5; 2021-06-11 (PDF dated June 14).

https://arxiv.org/pdf/2010.09649v5
