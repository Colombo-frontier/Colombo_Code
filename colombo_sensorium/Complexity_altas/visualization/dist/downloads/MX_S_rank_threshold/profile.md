# Exact rank-threshold decision

**Setting ID.** `MX_S_rank_threshold`

Matrix computation

Decide $D(A)=\mathbf1\{\operatorname{rank}(A)\ge r+1\}$.

**Status.** Fully optimal

**TASK tags.** formulation: Matrix property testing; solution concept: Rank threshold decision; task family: Matrix computation

**MODEL tags.** spectral structure: Arbitrary real matrix

**ORACLE tags.** feedback quality: Exact; interface family: Exact right matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Binary decision

**METRIC tags.** criterion: Exact rank decision

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N right

## 1. Setting specification

### Task

Decide $D(A)=\mathbf1\{\operatorname{rank}(A)\ge r+1\}$.

### Admissible model

The quantity $A\in\mathbb{R}^{d\times d}$ is arbitrary; assume $d\ge1$ and integer threshold $0\le r<d$.

### Oracle interface

The quantity $d,r$ is public and $A$ hidden. Any $v\in\mathbb{R}^d$ returns exact $Av$; no transpose channel is available.

### Output

Return the one-bit decision $\widehat{D}\in\{0,1\}$; no rank value, witness vector, or certificate is required.

### Loss or accuracy criterion

The base loss is $\mathbf1\{\widehat{D}\ne D(A)\}$, and classification must be correct with probability at least $2/3$.

### Resource accounting

Count right products with single vectors only: $N=N_{\mathrm r}$. A block of width $q$ costs $q$ calls.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using only public inputs. For every admissible input fixed before its private seed is generated, the success event has probability at least $2/3$ over that private randomness.

**Budget convention.** A fixed worst-case budget respected for every input and private seed.

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$r$: The rank threshold: decide whether the actual rank is at least r + 1. **Domain:** $r\in\mathbb Z,\ 0\le r<d$.

$D(A)=\mathbf1\{\operatorname{rank}(A)\ge r+1\}$

$A$: Arbitrary hidden real square matrix **Domain:** $\mathbb R^{d\times d}$.

$D(A),\widehat D$: The true rank-threshold decision and algorithm output. **Domain:** $\{0,1\}$.

$D(A)=\mathbf1\{\operatorname{rank}(A)\ge r+1\}$

$G$: Random query block used in the Gaussian-projection upper bound **Domain:** $\mathbb R^{d\times(r+1)}$.

$G_{ij}\stackrel{\mathrm{iid}}{\sim}\mathcal N(0,1)$

$\mathbf1\{E\}$: The indicator function of event E. **Domain:** $\{0,1\}$.

The value is $\mathbf1\{E\}=1$ on event $E$ and $0$ otherwise.

$N,N_{\mathrm r}$: Single-vector query budget for exact right products Av. A block is charged by its column count. **Domain:** $\mathbb N_0$.

$N=N_{\mathrm r}$

$N^\star$: Minimum worst-case query budget attaining this profile's success guarantee **Domain:** $\mathbb N_0\cup\{+\infty\}$.

The quantity is $N^\star=\inf_{\mathcal A}\sup_{I,\omega}N_{\mathcal A}(I,\omega)$, where the infimum ranges over admissible algorithms satisfying this profile's success guarantee.

$\mathcal A,I,\omega$: The algorithm, fixed admissible input, and private algorithmic seed. **Domain:** Quantifiers for worst-case input and execution cost. Success probability is taken over ω.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(d,r)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - All admissible rank thresholds

**Region.** Assume $d\ge1$ and integer $r$ with $0\le r<d$.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Optimal

**Lower bound.** B2

$$
r+1
$$

**Upper bound.** B1

$$
r+1
$$

**Gap or comparison.** $1$

**Comparison argument.** This specification has the exact complexity N*=r+1. The constant_factor status explicitly retains ratio=1 and the exact value.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Only exact Av for arbitrary real d-vectors is available, with randomized adaptive queries allowed. Each vector costs one N_right call; if G has q columns, AG costs q calls.

**Guarantee mapping.** Correctness probability is at least 2/3 for every fixed real matrix. Gaussian tests achieve probability one per fixed input; the lower bound is still evaluated over the full randomized algorithm class allowed by the specification.

**Output mapping.** Return low_rank when rank(A) ≤ r and high_rank when rank(A) ≥ r + 1. There is no numerical-rank tolerance band.

**Resource mapping.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

### B1 - Independent Gaussian block queries determine the queried column-space rank almost surely.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le r+1
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\le r+1
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Local argument.** A1

### B2 - Exact rank-decision lower bound for arbitrary randomized adaptive algorithms

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge r+1
$$

**Sources.** [1](https://drops.dagstuhl.de/opus/volltexte/2019/10670/pdf/LIPIcs-ICALP-2019-94.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge r+1
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://drops.dagstuhl.de/opus/volltexte/2019/10670/pdf/LIPIcs-ICALP-2019-94.pdf) theorem: Theorem 8; section: §3.1; pdf pages: 11

Randomized adaptive algorithms with any constant advantage require at least $r+1$ calls. The Gaussian-projection upper bound follows from source Section 3.1 and elementary rank properties.

## 5. Local arguments

### A1 - Independent Gaussian block queries determine the queried column-space rank almost surely.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Draw a d by (r+1) matrix G with independent standard Gaussian entries and query its columns. For each fixed A, rank(AG)=min{rank(A),r+1} almost surely: after an SVD of A, the relevant Gaussian block has maximal possible rank almost surely. Thus rank(AG)<=r exactly when rank(A)<=r. The test uses r+1 queries and is almost surely correct for every fixed input.

## References

[1] Xiaoming Sun; David P. Woodruff; Guang Yang; Jialin Zhang. Querying a Matrix Through Matrix-Vector Products. 2019. ICALP 2019, Article 94, pp.94:1–94:16.

https://drops.dagstuhl.de/opus/volltexte/2019/10670/pdf/LIPIcs-ICALP-2019-94.pdf
