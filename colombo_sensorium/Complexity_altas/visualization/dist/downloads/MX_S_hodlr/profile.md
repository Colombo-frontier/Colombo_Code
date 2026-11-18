# Hierarchical low-rank matrix approximation: HODLR relative error.

**Setting ID.** `MX_S_hodlr`

Matrix computation

Find $\widehat{H}\in\mathcal{H}_k$, where $\mathcal{H}_k$ is the HODLR class for the specified block tree.

**Status.** Other quantified gap present

**TASK tags.** formulation: Hierarchical matrix approximation; solution concept: Relative hodlr error; task family: Matrix computation

**MODEL tags.** spectral structure: Balanced hierarchical partition; spectral structure: Public hodlr tree

**ORACLE tags.** feedback quality: Exact; interface family: Exact two sided matvec; operation: Matrix left matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Structured matrix

**METRIC tags.** criterion: Relative hierarchical residual

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N left; measure: N right

## 1. Setting specification

### Task

Find $\widehat{H}\in\mathcal{H}_k$, where $\mathcal{H}_k$ is the HODLR class for the specified block tree.

### Admissible model

The matrix $A\in\mathbb{R}^{d\times d}$ is arbitrary. A balanced binary partition tree is public. At each level only diagonal blocks are partitioned recursively, until leaf sizes are at most $k$; every off-diagonal sibling block has rank at most $k$. Assume $1\le k<d$ and tree depth $L=\lceil\log_2(d/k)\rceil$, together with the integer compatibility conditions required for equal partitions. The full matrix need not have low rank.

### Oracle interface

The quantity $d,k$, block tree, and $\varepsilon$ are public; $A$ is hidden. Exact $Av$ and $A^{\mathsf T}u$ are available for arbitrary real vectors.

### Output

Return $\widehat{H}\in\mathcal{H}_k$ satisfying every block-rank constraint of the tree. A hierarchical factor representation is allowed, and no certificate is required.

### Loss or accuracy criterion

Define $\operatorname{OPT}_{\mathcal{H}}=\min_{H\in\mathcal{H}_k}\|A-H\|_{\mathrm{F}}$. Success requires $\|A-\widehat{H}\|_{\mathrm{F}}\le(1+\varepsilon)\operatorname{OPT}_{\mathcal{H}}$. Zero optimal error requires exact structured recovery.

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

$k$: Rank cap on every sibling off-diagonal block in the public partition tree **Domain:** $k\in\mathbb N,\ 1\le k<d$.

For every pair of sibling blocks $I,J$ in the public partition tree, $\operatorname{rank}(H_{I,J})\le k$.

$L$: Number of recursive diagonal-block bisections needed to reach leaf side length at most $k$. **Domain:** $L\in\mathbb N,\ d/2^L\in\mathbb N$.

$L=\lceil\log_2(d/k)\rceil$

$\varepsilon$: Additional relative factor over the best HODLR Frobenius residual. **Domain:** $\varepsilon>0$.

$\|A-\widehat H\|_F\le(1+\varepsilon)\operatorname{OPT}_{\mathcal H}$

$C_0$: The sufficient-dimension constant required by the hard constructions in HD Theorems 1.2 and 6.2. **Domain:** The quantity $C_0>0$ is universal and fixed.

$d\ge C_0k/\varepsilon$

$A$: The hidden arbitrary input matrix. **Domain:** $\mathbb R^{d\times d}$.

$\mathcal T$: Public balanced binary block tree **Domain:** Recursively bisect only diagonal blocks until leaf side lengths are at most $k$.

$\mathcal H_k$: Matrices whose sibling off-diagonal blocks on the specified tree each have rank at most k **Domain:** $\mathcal H_k\subseteq\mathbb R^{d\times d}$. Diagonal leaf blocks are arbitrary.

$\widehat H$: Returned hierarchical low-rank matrix **Domain:** $\widehat H\in\mathcal H_k$.

$\operatorname{OPT}_{\mathcal H}$: The optimal HODLR Frobenius residual for the specified tree. **Domain:** A nonnegative real.

$\operatorname{OPT}_{\mathcal H}=\min_{H\in\mathcal H_k}\|A-H\|_F$

$\beta_{\mathrm{alg}}$: Additional relative factor at each level in the HD upper bound **Domain:** An internal algorithm parameter.

$\beta_{\mathrm{alg}}=(1+\varepsilon)^{1/L}-1$

$\Gamma$: Overall approximation factor in the source HODLR theorem. **Domain:** Internal change of variables.

$\Gamma=(1+\beta_{\mathrm{alg}})^L=1+\varepsilon$

$\log_2$: Base-$2$ logarithm **Domain:** Positive real argument.

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
N^\star(d,k,\varepsilon)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - The hierarchical-approximation lower-bound window.

**Region.** Require $0<\varepsilon<1$ and $d\ge C_0k/\varepsilon$. The condition $d,k$ must be compatible with the specified balanced binary partition tree. The quantity $C_0>0$ is the sufficient dimension constant from the source.

**Quantity.** Q1

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Other quantified gap

**Lower bound.** B3

$$
\Omega(k\log(d/k)+k/\varepsilon)
$$

**Upper bound.** B1, B2

$$
O(\min\{d,kL^4/\varepsilon^3\})
$$

**Gap or comparison.** $O\!\left(\frac{\min\{d,kL^4/\varepsilon^3\}}{k\log(d/k)+k/\varepsilon}\right)$. Parameters vary jointly; the rate is not reduced to one accuracy exponent throughout the domain.

**Comparison argument.** Only the difference between verified envelopes is reported. On the nonsaturated slice with epsilon<=1/L, the ratio is O(L^4/epsilon²); the full multiparameter domain is not assigned a single fixed power.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact Av and A^T u channels, with a public balanced block tree. Each vector product costs one call, and batched sketches are charged per column. A need not itself be HODLR.

**Output mapping.** Return a matrix in the specified tree's HODLR($k$) class: off-diagonal sibling blocks have rank at most $k$, and leaf blocks are unrestricted. The criterion is a $(1+\epsilon)$ relative residual in unsquared Frobenius norm.

**Resource mapping.** Retain joint budget $(N_{\mathrm r},N_{\mathrm l})$ for single-vector $Av$ and $A^{\mathsf T}u$ calls, with the explicit equal-weight scalarization $N=N_{\mathrm r}+N_{\mathrm l}$. Charge each block column separately. The budget is a worst-case cap for every input and private seed, not an expected count. Reading public inputs and internal exact-real arithmetic, storage, and postprocessing are uncharged; query complexity is not runtime or bit complexity.

### B1 - Randomized nonadaptive hierarchical peeling or sketching upper bound.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le C kL^4/\varepsilon^3
$$

**Sources.** [1](https://arxiv.org/pdf/2407.04686v2)

**Guarantee conversion.** The source's nonadaptive upper bound succeeds with probability $99/100$, exceeding the required $2/3$. Its parameter conversion from $(1+\beta)^L$ to $1+\epsilon$ retains the recorded derivation and validity region.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right+N left.**

$$
C k L^4 / eps^3
$$

**additional arithmetic.** d poly(log d,k,1/eps)

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** Choose $\beta_{\mathrm{alg}}=(1+\varepsilon)^{1/L}-1$, giving source error factor $\Gamma=(1+\beta_{\mathrm{alg}})^L=1+\varepsilon$. On $0<\varepsilon<1$, we have $\beta_{\mathrm{alg}}=\Theta(\varepsilon/L)$. Substitution into the same algorithm's total bidirectional call count $O(kL/\beta_{\mathrm{alg}}^3)$ yields $O(kL^4/\varepsilon^3)$.

**Source location.** [1](https://arxiv.org/pdf/2407.04686v2) theorem: Theorem 1.1; Definition 1.1; Problem 1.1; section: §1; pdf pages: 2; 3

The method is nonadaptive with success probability 99/100. Its native parameters are Γ = (1 + β)^L and q = O(kL/β³).

### B2 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Sources.** [1](https://arxiv.org/pdf/2407.04686v2)

**Guarantee conversion.** Success probability is at least 2/3 for each fixed A and public tree. Nonadaptive peeling gives a valid upper bound; the general lower bound may still cover randomized adaptive algorithms.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** d

**N left.** 0

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/2407.04686v2) theorem: Theorem 1.1; Definition 1.1; Problem 1.1; section: §1; pdf pages: 2; 3

The method is nonadaptive with success probability 99/100. Its native parameters are Γ = (1 + β)^L and q = O(kL/β³).

### B3 - General randomized adaptive two-sided queries; exact recovery and reduction from fixed-pattern sparse approximation

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c[k\log(d/k)+k/\varepsilon]
$$

**Sources.** [1](https://arxiv.org/pdf/2407.04686v2)

**Dimension conditions.** Require d ≥ C0 k/ε and a compatible tree.

**Guarantee conversion.** The source hard threshold is below the required 2/3 success probability, so the lower bound applies. Retain sufficient-dimension and tree-compatibility conditions; it does not extend to arbitrary d.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge c[k\log(d/k)+k/\varepsilon]
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/2407.04686v2) theorem: Theorem 1.2; Theorems 6.1 and 6.2; section: §1; §6; pdf pages: 3; 22; 23; 24

The dimension condition d>=c k/epsilon is retained in Theorem 1.2, footnote 6, and Theorem 6.2, footnote 14. The required 2/3 success probability exceeds the source lower-bound threshold 1/25.

## References

[1] Tyler Chen; Feyza Duman Keles; Diana Halikias; Cameron Musco; Christopher Musco; David Persson. Near-optimal hierarchical matrix approximation from matrix-vector products. 2025. arXiv:2407.04686v2 (2024-10-24); SODA 2025.

https://arxiv.org/pdf/2407.04686v2
