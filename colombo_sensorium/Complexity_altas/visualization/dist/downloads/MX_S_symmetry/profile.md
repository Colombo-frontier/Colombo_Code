# Exact symmetry testing for a real matrix

**Setting ID.** `MX_S_symmetry`

Matrix computation

Decide $D(A)=\mathbf1\{A=A^{\mathsf T}\}$.

**Status.** Fully optimal

**TASK tags.** formulation: Matrix property testing; solution concept: Symmetry decision; task family: Matrix computation

**MODEL tags.** spectral structure: Arbitrary real matrix

**ORACLE tags.** feedback quality: Exact; interface family: Exact right matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Binary decision

**METRIC tags.** criterion: Exact symmetry decision

**GUARANTEE tags.** randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N right

## 1. Setting specification

### Task

Decide $D(A)=\mathbf1\{A=A^{\mathsf T}\}$.

### Admissible model

The matrix $A\in\mathbb R^{d\times d}$ is arbitrary, with $d\ge2$. No known distance from symmetry is required.

### Oracle interface

The data $d$ are public and $A$ is hidden. Exact $Av$ queries are allowed for arbitrary real vectors. No $A^{\mathsf T}u$ channel is provided.

### Output

Return $\widehat D\in\{0,1\}$, without an additional certificate.

### Loss or accuracy criterion

The misclassification loss is $\mathbf1\{\widehat{D}\ne D(A)\}$ and must vanish almost surely. There is no approximate-symmetry or finite-precision threshold.

### Resource accounting

Count right products with single vectors only: $N=N_{\mathrm r}$. A block of width $q$ costs $q$ calls.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

For each fixed matrix, correctness has probability one over private randomness. A single seed need not be correct simultaneously for all real matrices.

**Budget convention.** A fixed worst-case budget respected for every input and private seed.

## 2. Notation and parameters

$d$: The order of the real square matrix tested for symmetry. **Domain:** $d\in\mathbb N,\ d\ge2$.

$A\in\mathbb R^{d\times d}$

$A$: Arbitrary hidden real square matrix **Domain:** $\mathbb R^{d\times d}$.

$D(A),\widehat D$: True symmetry decision and the algorithm's output **Domain:** $\{0,1\}$.

$D(A)=\mathbf1\{A=A^{\mathsf T}\}$

$u,v$: The independent standard Gaussian probes used in the two right-product queries. **Domain:** $\mathbb R^d$.

$u,v\stackrel{\mathrm{ind}}{\sim}\mathcal N(0,I_d)$

$I_d$: d-dimensional identity matrix **Domain:** $\mathbb R^{d\times d}$.

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
N^\star(d)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - Nontrivial dimension

**Region.** Integer dimension $d\ge2$

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Optimal

**Lower bound.** B2

$$
1
$$

**Upper bound.** B1

$$
2
$$

**Gap or comparison.** $2$

**Comparison argument.** A constant-factor bracket is certified; the exact optimum is not asserted to be two.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Only exact right products Av are supplied, without A^T u. Two right products evaluate the cross bilinear expression; each vector product costs one call.

**Guarantee mapping.** The specification requires probability-one success for each fixed A. Gaussian testing is one upper-bound algorithm, not a restriction on every admissible algorithm's randomness.

**Output mapping.** Return symmetric or nonsymmetric, distinguishing $A=A^{\mathsf T}$ exactly from $A\ne A^{\mathsf T}$. No distance-tolerant property is used.

**Resource mapping.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

### B1 - Bilinear symmetry test using two independent continuous probes

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le 2
$$

**Sources.** [1](https://drops.dagstuhl.de/opus/volltexte/2019/10670/pdf/LIPIcs-ICALP-2019-94.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\le 2
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Local argument.** A1

**Source location.** [1](https://drops.dagstuhl.de/opus/volltexte/2019/10670/pdf/LIPIcs-ICALP-2019-94.pdf) theorem: Theorem 10 and its proof; section: §3.3; pdf pages: 11

The source gives a common O(log(1/δ)) statement over finite fields and the reals. Over the reals, a nonzero quadratic polynomial vanishes on a Gaussian-null set. Consequently, two fixed queries suffice with success probability one.

### B2 - Zero queries cannot distinguish symmetric from nonsymmetric inputs.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge 1
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge 1
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Local argument.** A2

## 5. Local arguments

### A1 - Bilinear symmetry test using two independent continuous probes

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Draw independent standard Gaussian vectors u,v and query Au and Av. Test whether u^T Av=v^T Au. A symmetric matrix always passes. If B=A-A^T is nonzero, the polynomial u^T Bv is not identically zero; its zero set has Lebesgue measure zero. Consequently every fixed nonsymmetric matrix is rejected with probability one. Exactly two right-multiplication queries are used.

**Sources.** [1](https://drops.dagstuhl.de/opus/volltexte/2019/10670/pdf/LIPIcs-ICALP-2019-94.pdf)

### A2 - Zero-query indistinguishability of symmetric and nonsymmetric inputs

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

For d>=2, the allowed class contains both a symmetric matrix and a nonsymmetric matrix. With no queries, the output distribution is the same on these two inputs. It cannot return the two different correct labels almost surely, so at least one query is necessary.

## References

[1] Xiaoming Sun; David P. Woodruff; Guang Yang; Jialin Zhang. Querying a Matrix Through Matrix-Vector Products. 2019. ICALP 2019, Article 94, pp.94:1–94:16.

https://drops.dagstuhl.de/opus/volltexte/2019/10670/pdf/LIPIcs-ICALP-2019-94.pdf
