# A finite public matrix family with relative Frobenius approximation.

**Setting ID.** `MX_S_finite_family`

Matrix computation

Minimize $\|A-B\|_{\mathrm{F}}$ over the finite public matrix family $\mathcal{F}$.

**Status.** Logarithmic gap present; Bounds missing

**TASK tags.** task family: Matrix computation

**MODEL tags.** structure: Public finite family

**ORACLE tags.** feedback quality: Exact; interface family: Exact two sided matvec; operation: Matrix right matvec; operation: Matrix transpose matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Matrix in finite family

**METRIC tags.** criterion: Relative finite family error

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** measure: N left; measure: N right

## 1. Setting specification

### Task

Minimize $\|A-B\|_{\mathrm{F}}$ over the finite public matrix family $\mathcal{F}$.

### Admissible model

The matrix $A\in\mathbb{R}^{d\times d}$ is arbitrary; $\mathcal{F}\subset\mathbb{R}^{d\times d}$ is finite, nonempty, and known, with $|\mathcal{F}|=M$. No assumption $A\in\mathcal{F}$ is imposed. The relative factor is $\gamma\ge1$.

### Oracle interface

The data $d,\mathcal{F},M,\gamma,\delta$ are public, while $A$ is hidden. The oracle separately returns exact $Av$ and $A^{\mathsf T}u$ for arbitrary query vectors. Candidate matrices, arithmetic involving candidates, and candidate search are freely available.

### Output

Return $\widehat B\in\mathcal F$. A candidate index must uniquely identify its matrix. No error certificate is required.

### Loss or accuracy criterion

$\operatorname{OPT}=\min_{B\in\mathcal{F}}\|A-B\|_{\mathrm{F}}$, with success criterion $\|A-\widehat{B}\|_{\mathrm{F}}\le\gamma\operatorname{OPT}$. Zero optimal error requires exact recovery.

### Resource accounting

Retain the joint budget $(N_{\mathrm{r}},N_{\mathrm{l}})$, whose coordinates count single-vector calls to $Av$ and $A^{\mathsf T}u$, respectively. This setting explicitly uses the equal-weight scalarization $N=N_{\mathrm{r}}+N_{\mathrm{l}}$. Each column of a block is charged separately.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using public inputs only. For every admissible input fixed before generation of the private seed, success probability over private randomness is at least $1-\delta$.

**Budget convention.** fixed worst-case joint budget; no expectation substituted

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$M$: Cardinality of the public finite candidate matrix family **Domain:** $M\in\mathbb N,\ M\ge1$.

$M=|\mathcal F|$

$\gamma$: Target factor relative to the smallest residual in the candidate family **Domain:** $\gamma\ge1$.

$\|A-\widehat B\|_F\le\gamma\min_{B\in\mathcal F}\|A-B\|_F$

$\delta$: The permitted failure probability for each fixed input and public candidate family. **Domain:** $0<\delta<1$.

Success probability is at least $1-\delta$.

$A$: The hidden arbitrary input matrix. **Domain:** $\mathbb R^{d\times d}$.

$\mathcal F$: Fully public nonempty finite candidate matrix family **Domain:** $\mathcal F\subset\mathbb R^{d\times d},\ |\mathcal F|=M$.

$\widehat B$: Candidate matrix returned by the algorithm **Domain:** $\widehat B\in\mathcal F$.

$\operatorname{OPT}$: Best Frobenius residual within the candidate family. **Domain:** A nonnegative real.

$\operatorname{OPT}=\min_{B\in\mathcal F}\|A-B\|_F$

$\eta$: Additional accuracy beyond the constant approximation factor 3 in the QSL upper bound. **Domain:** Used only within this upper-bound window.

$\eta=\gamma-3,\quad0<\eta<1$

$\widetilde O$: Suppresses the confidence, accuracy, and size logarithms explicitly stated in the QSL upper bound **Domain:** Retain the log log M, log(1/η), and log(1/δ) factors. Use the source truncation convention for small sizes.

$\|M\|_{\mathrm F}$: The Frobenius norm. **Domain:** An arbitrary real or complex matrix.

$\|M\|_{\mathrm F}=(\sum_{ij}|M_{ij}|^2)^{1/2}=(\sum_i\sigma_i(M)^2)^{1/2}$

$c,C$: Positive universal constants in the corresponding bound. Identically named constants in different theorems need not have the same value. **Domain:** Independent of the dimension, accuracy, and probability parameters tracked by this bound.

$\log$: Natural logarithm **Domain:** Positive real argument.

$\log x=\ln x$

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

$N_{\mathrm r},N_{\mathrm l}$: Single-vector counts for right products Av and transpose products Aᵀu. **Domain:** $\mathbb N_0^2$.

$N$: The worst-case call budget with equal costs for both product channels. **Domain:** $\mathbb N_0$.

$N=N_{\mathrm r}+N_{\mathrm l}$

$N^\star$: Minimum worst-case query budget attaining this profile's success guarantee **Domain:** $\mathbb N_0\cup\{+\infty\}$.

The quantity is $N^\star=\inf_{\mathcal A}\sup_{I,\omega}N_{\mathcal A}(I,\omega)$, where the infimum ranges over admissible algorithms satisfying this profile's success guarantee.

$\mathcal A,I,\omega$: The algorithm, fixed admissible input, and private algorithmic seed. **Domain:** Quantifiers for worst-case input and execution cost. Success probability is taken over ω.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(d,M,\gamma,\delta)
$$

**Scope.** The algorithm may use the complete public candidate family. For fixed d, M, gamma, and delta, take the worst case over all such public finite families and hidden input matrices. The lower bound asserts existence of a hard family only.

**Optimization direction.** minimize

### R1 - Worst-case comparison with the public family up to a fixed factor

**Region.** Fix $3<\gamma<4$ and $\delta=1/10$. Use the hard finite family in Appendix E of QSL26 with $M=|\mathcal{F}|$ and $\log M\le C d^2\log\gamma$, retaining its covering-net and integer-embedding construction. The upper bound holds for every public finite family; the lower bound asserts existence of a hard family.

**Quantity.** Q1

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(\sqrt{\log M})
$$

**Upper bound.** B1

$$
\widetilde{O}(\sqrt{\log M})
$$

**Gap or comparison.** $\operatorname{poly}(\log\log M)$

**Comparison argument.** Fix $\gamma\in(3,4)$ and $\delta=0.1$. Near matching is established only for worst-case families along the stated hard-family size curve. No lower bound is imposed on every fixed family or arbitrary $M$.

### R2 - Reconstruction baseline for the finite public family

**Region.** Require $d,M\ge1$, $\gamma\ge1$, and $0<\delta<1$. The public finite candidate family is nonempty.

**Quantity.** Q1

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

$$
O(d)
$$

**Comparison argument.** This is a baseline over the full domain. For 3 < γ < 4, a smaller finite-family algorithm may also apply, subject to separately stated conditions.

## 4. Bounds and supporting evidence

### B1 - Randomized adaptive two-sided sketch elimination, Amsel et al., Theorem 1

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le\widetilde{O}\!\left(\frac{\sqrt{\log M}}{(\gamma-3)^2}\right)
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v336/main/assets/amsel26a/amsel26a.pdf)

**Oracle correspondence.** Both A and Aᵀ queries are required. Search among public candidates is free.

**Resource conversion.** Sum of A and A^T vector products; family search costs uncharged.

**Constants.** Polylogarithms in log M, 1/eta and 1/delta_conf; no leading 1+eta claim.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v336/main/assets/amsel26a/amsel26a.pdf) pdf pages: 2; 3; 4; 10; 11; 12; 13; theorem or section: Problem 1; Theorem 1; Algorithm 4; theorem: Problem 1; Theorem 1; Algorithm 4

QSL Theorem 1 obtains a (3 + η)-factor Frobenius residual guarantee for any fully public finite matrix family using products with the matrix and its transpose. Set η = γ − 3. Candidate search and public-matrix arithmetic do not count as oracle queries.

### B2 - Hard public covering-net families and Wishart posterior anti-concentration, covering general randomized adaptive two-sided queries.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c\sqrt{\frac{\log M}{\log\gamma}}
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v336/main/assets/amsel26a/amsel26a.pdf)

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v336/main/assets/amsel26a/amsel26a.pdf) theorem: Theorem 2; Appendix E, PDF pp.34–37

The query lower bound also takes the worst case over the public family F. It does not imply that each fixed F requires this many queries. Exact endpoint realization for every prescribed integer M has not been established.

### B3 - Deterministic standard-basis reconstruction followed by candidate enumeration

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

**Derivation.** All public candidates may be processed freely. Returning the exact best candidate satisfies every γ ≥ 1.

**Local argument.** A1

## 5. Local arguments

### A1 - Deterministic standard-basis reconstruction and candidate enumeration

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Recover the $d$ columns by standard basis queries. Evaluate every public candidate's Frobenius residual internally and choose an exact minimizer, with a fixed public tie rule. This attains the family optimum and therefore satisfies every allowed multiplicative factor at least one, including zero optimal residual.

## References

[1] Noah Amsel; Pratyush Avi; Tyler Chen; Feyza Duman Keles; Chinmay Hegde; Christopher Musco; Cameron Musco; David Persson. Query Efficient Structured Matrix Learning. 2026. COLT 2026 PMLR 336, pp.158–194.

https://raw.githubusercontent.com/mlresearch/v336/main/assets/amsel26a/amsel26a.pdf
