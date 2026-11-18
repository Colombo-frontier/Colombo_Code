# Fixed-sparsity-pattern approximation with relative Frobenius error.

**Setting ID.** `MX_S_fixed_sparsity`

Matrix computation

Approximate $A$ within the public support pattern $S$, using the comparison $\min_{B:S\circ B=B}\|A-B\|_{\mathrm{F}}$.

**Status.** Fully optimal

**TASK tags.** formulation: Structured matrix approximation; solution concept: Relative fixed pattern error; task family: Matrix computation

**MODEL tags.** spectral structure: S regular public pattern

**ORACLE tags.** feedback quality: Exact; interface family: Exact two sided matvec; operation: Matrix left matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Matrix

**METRIC tags.** criterion: Relative frobenius pattern

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N left; measure: N right

## 1. Setting specification

### Task

Approximate $A$ within the public support pattern $S$, using the comparison $\min_{B:S\circ B=B}\|A-B\|_{\mathrm{F}}$.

### Admissible model

The matrix $A\in\mathbb{R}^{d\times d}$ is arbitrary. Every row and column of $S\in\{0,1\}^{d\times d}$ contains exactly $s$ ones, and $1\le s\le d$ holds. The operation $\circ$ denotes entrywise multiplication.

### Oracle interface

The quantities $d,s,S,\varepsilon$ are public; $A$ is hidden. Exact products $Av$ and $A^{\mathsf T}u$ are available. Reading and processing the public sparsity pattern are free.

### Output

Return a matrix $\widehat{B}$ satisfying $S\circ\widehat{B}=\widehat{B}$. Neither the full $A$ nor an error certificate is required.

### Loss or accuracy criterion

Define $\|M\|_{\mathrm{F}}=(\sum_{ij}M_{ij}^2)^{1/2}$. The optimal error is $\operatorname{OPT}=\|A-S\circ A\|_{\mathrm{F}}$ and success requires $\|A-\widehat{B}\|_{\mathrm{F}}\le(1+\varepsilon)\operatorname{OPT}$. Zero optimal error requires exact recovery.

### Resource accounting

Retain the joint budget $(N_{\mathrm{r}},N_{\mathrm{l}})$, whose coordinates count single-vector calls to $Av$ and $A^{\mathsf T}u$, respectively. This setting explicitly uses the equal-weight scalarization $N=N_{\mathrm{r}}+N_{\mathrm{l}}$. Each column of a block is charged separately.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using only public inputs. For every admissible input fixed before its private seed is generated, the success event has probability at least $2/3$ over that private randomness.

**Budget convention.** A fixed worst-case budget respected for every input and private seed.

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$s$: Number of ones in each row and column of the public binary support pattern. **Domain:** $s\in\mathbb N,\ 1\le s\le d$.

$\sum_j S_{ij}=s,\quad\sum_i S_{ij}=s$

$\varepsilon$: Additional relative factor over the optimal Frobenius residual within the fixed support pattern **Domain:** $\varepsilon>0$.

$\|A-\widehat B\|_F\le(1+\varepsilon)\|A-S\circ A\|_F$

$b_2$: Universal hard-instance size constant in the proof of FS, Theorem 2 **Domain:** The quantity $b_2>0$ is universal and fixed.

$d_0=s\lceil b_2/\varepsilon\rceil$

$A$: The hidden matrix is arbitrary. Its entries need not follow the output support pattern. **Domain:** $\mathbb R^{d\times d}$.

$S$: Public binary support pattern **Domain:** $\{0,1\}^{d\times d}$.

$\circ$: The entrywise product of matrices of the same shape. **Domain:** A binary operation.

$(S\circ B)_{ij}=S_{ij}B_{ij}$

$\widehat B$: Output matrix conforming to the support pattern **Domain:** $\mathbb R^{d\times d}$.

$S\circ\widehat B=\widehat B$

$\operatorname{OPT}$: Best Frobenius residual within the public support pattern. **Domain:** A nonnegative real.

$\operatorname{OPT}=\min_{B:S\circ B=B}\|A-B\|_F=\|A-S\circ A\|_F$

$d_0$: Order of the source Wishart hard instance **Domain:** Auxiliary integer in the proof.

$d_0=s\lceil b_2/\varepsilon\rceil$

$c_0$: Sufficient small-accuracy constant in FS, Theorem 2 **Domain:** Fixed universal positive constant.

$0<\varepsilon<c_0$

$\|M\|_{\mathrm F}$: The Frobenius norm. **Domain:** An arbitrary real or complex matrix.

$\|M\|_{\mathrm F}=(\sum_{ij}|M_{ij}|^2)^{1/2}=(\sum_i\sigma_i(M)^2)^{1/2}$

$c,C$: Positive universal constants in the corresponding bound. Identically named constants in different theorems need not have the same value. **Domain:** Independent of the dimension, accuracy, and probability parameters tracked by this bound.

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
N^\star(d,s,\varepsilon)\qquad\text{worst case over public }S
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - Fixed-support hard construction and embedding window

**Region.** Assume $0<\varepsilon<c_0$ and define $d_0=s\lceil b_2/\varepsilon\rceil$. Require $d=d_0$ or $d\ge d_0+s$, where $c_0,b_2>0$ is the universal construction constant in the proof of the source Theorem 2.

**Quantity.** Q1

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega(s/\varepsilon)
$$

**Upper bound.** B1, B2

$$
O(s/\varepsilon)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** Use the same two-channel specification, success probability 2/3, and worst case over public masks. The dimension construction ensures d = Ω(s/ε).

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** For fixed arbitrary real $A$, exact $Av$ and $A^{\mathsf T}u$ are available, with public mask $S$. Each vector costs one call; blocks are charged by columns. The input need not be sparse.

**Guarantee mapping.** Success probability is at least 2/3 for each fixed (A,S). The lower bound may select a hard public mask, while dimension conditions of the construction are retained.

**Output mapping.** Return S ∘ B_hat = B_hat with unsquared Frobenius residual at most (1 + ε)‖A − S ∘ A‖_F. The mask constrains the output.

**Resource mapping.** Retain joint budget $(N_{\mathrm r},N_{\mathrm l})$ for single-vector $Av$ and $A^{\mathsf T}u$ calls, with the explicit equal-weight scalarization $N=N_{\mathrm r}+N_{\mathrm l}$. Charge each block column separately. The budget is a worst-case cap for every input and private seed, not an expected count. Reading public inputs and internal exact-real arithmetic, storage, and postprocessing are uncharged; query complexity is not runtime or bit complexity.

### B1 - Randomized nonadaptive least-squares sketching with a fixed support pattern

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le\max\{s+2,\lceil s(1+3/(2\varepsilon))+1\rceil\}
$$

**Sources.** [1](https://arxiv.org/pdf/2402.09379v3)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** max{s+2,ceil(s(1+3/(2eps))+1)}

**N left.** 0

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/2402.09379v3) theorem: Theorem 1; Corollary 1; section: §1.2; pdf pages: 3

Require m>=s+2 and m>=s(1+1/(2 delta epsilon))+1; set delta=1/3. The algorithm uses only right products and remains valid with the stronger two-channel interface.

### B2 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** d

**N left.** 0

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Local argument.** A1

### B3 - General randomized adaptive two-sided queries and Wishart hard families.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c s/\varepsilon
$$

**Sources.** [1](https://arxiv.org/pdf/2402.09379v3)

**Dimension conditions.** d=d0 or d>=d0+s, with d0=s ceil(b2/epsilon).

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge c s/\varepsilon
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** The source Theorem 2 allows each row and column support size within a fixed proportional interval. Fixing its proportion to $1/2$ admits the subclass with exactly s entries per row and column. The native hard dimension is $d_0=s\lceil b_2/\varepsilon\rceil$. If $d\ge d_0+s$, extend it by an s-regular block-diagonal mask and a zero input block. Each extended left or right query is simulated by one corresponding native query. The lower bound takes the worst case over public masks.

**Local argument.** A2

**Source location.** [1](https://arxiv.org/pdf/2402.09379v3) theorem: Theorem 2 and its proof; section: §3; pdf pages: 4; 14; 15

The hard-instance dimension is $d=s\lceil b_2/\epsilon\rceil$. The theorem allows between $\gamma s$ and $s$ entries per row and column; use fixed $\gamma=1/2$ and the $s$-regular subclass. Symmetry of the hard instance permits both product directions.

## 5. Local arguments

### A1 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Recover all $d$ columns by standard basis queries and return $S\circ A$. Every permitted entry is copied exactly and every prohibited entry is zero, so the output attains the best Frobenius residual for the public support pattern. The input need not follow that support pattern.

### A2 - General randomized adaptive two-sided queries and Wishart hard families.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Retain the cited primary theorem and include the padding argument here. Let d_0=s ceil(b_2/epsilon) be the native hard dimension. If d>=d_0+s, put r=d-d_0>=s. On an r by r block, choose the cyclic mask with s consecutive allowed positions in each row; it is s-regular in both rows and columns. Adjoin this mask block to the native hard mask and extend the hard input by a zero block. Every left or right query to the extended instance is simulated by one corresponding query to the native block. Restricting any admissible approximate output to the native block cannot increase its error, while the optimal masked approximation error is unchanged. The native lower bound therefore applies in the padded dimension.

**Sources.** [1](https://arxiv.org/pdf/2402.09379v3)

## References

[1] Noah Amsel; Tyler Chen; Feyza Duman Keles; Diana Halikias; Cameron Musco; Christopher Musco. Fixed-sparsity matrix approximation from matrix-vector products. 2026. Mathematical text checked in arXiv:2402.09379v3 (2024-03-26); SIMAX 47(2), 2026 publication.

https://arxiv.org/pdf/2402.09379v3
