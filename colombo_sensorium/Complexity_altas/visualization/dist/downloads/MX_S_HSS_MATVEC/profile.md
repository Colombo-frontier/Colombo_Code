# Hierarchically semi-separable matrix approximation from two-sided matrix-vector products

**Setting ID.** `MX_S_HSS_MATVEC`

Matrix computation

Approximate an arbitrary real square matrix by a matrix with nested HSS bases, measured against the best HSS squared Frobenius residual.

**Status.** Logarithmic gap present

**TASK tags.** task family: Matrix computation; formulation: Hierarchical matrix approximation

**MODEL tags.** spectral structure: Balanced hierarchical partition

**ORACLE tags.** operation: Matrix left matvec; feedback quality: Exact; operation: Matrix right matvec

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** object: Structured matrix

**METRIC tags.** criterion: Relative hierarchical residual

**GUARANTEE tags.** mode: Expectation

**RESOURCE tags.** measure: Oracle calls

## 1. Setting specification

### Task

Return a quasi-optimal HSS approximation relative to the best HSS matrix on the same tree.

$$
\min_{B\in\operatorname{HSS}(L,k)} \|A-B\|_F^2
$$

### Admissible model

The hidden input $A$ is arbitrary. The comparison class uses a perfect binary tree with $2^L$ leaves of size $2k$.

An HSS matrix has a telescoping factorization $B^{(L+1)}=B$, $B^{(1)}=D^{(0)}$, and $B^{(\ell+1)}=U^{(\ell)}B^{(\ell)}(V^{(\ell)})^{\mathsf T}+D^{(\ell)}$ for $\ell=1,\dots,L$.

At level $\ell$, $U^{(\ell)}$ and $V^{(\ell)}$ have $2^\ell$ diagonal blocks of shape $2k\times k$ with orthonormal columns. $D^{(\ell)}$ has $2^\ell$ arbitrary diagonal blocks of shape $2k\times2k$. The base $D^{(0)}$ is arbitrary $2k\times2k$.

### Oracle interface

With $A$ hidden, query any $v,u\in\mathbb R^N$ to receive exact $Av$ or exact $A^{\mathsf T}u$ in separate calls. No independent entry or submatrix access is supplied.

### Output

Return $\widehat B\in\operatorname{HSS}(L,k)$, for instance by returning its valid telescoping factors.

### Loss or accuracy criterion

Use $\|A-\widehat B\|_F^2$ against the minimum squared residual for HSS on the same tree.

### Resource accounting

Count $N_{\rm right}+N_{\rm left}$. Block queries are charged by column.

### Algorithm views and success guarantees

The algorithm may use private randomness and the full transcript. The native response is a full vector. Internal computation is uncharged.

The expected squared error is required separately for every admissible input.

$$
\mathbb{E}_{\omega}\|A-\widehat B\|_F^2\le\gamma\min_{B\in\operatorname{HSS}(L,k)}\|A-B\|_F^2
$$

If the minimum is zero, the returned matrix must equal the input almost surely.

## 2. Notation and parameters

$L$: Number of HSS compression levels. **Domain:** $L\in\mathbb N_{\ge1}$.

$L\in\mathbb N_{\ge1}$

$k$: Basis width in each block. **Domain:** $k\in\mathbb N_{\ge1}$.

$k\in\mathbb N_{\ge1}$

$N$: Dimension of the square matrix. **Domain:** $N=2^{L+1}k$.

$N=2^{L+1}k$

$\gamma$: Target factor on the expected squared residual. **Domain:** $\gamma\ge1$.

$\gamma\ge1$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
Q^\star(N,L,k,\gamma)
$$

**Scope.** The minimum fixed total query cap of a randomized adaptive algorithm satisfying the guarantee on every input.

**Optimization direction.** minimize

### R1 - Perfect binary tree and quasi-optimal factor

**Region.** Public integers $L,k\ge1$, $N=2^{L+1}k$, and target factor $\gamma\ge c_{\mathrm{HSS}}L$ for a sufficiently large universal constant. The fixed binary partition has $2k$ indices per leaf.

**Quantity.** Q1

**Resource.** Sum of charged right and transpose matvecs.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(k)
$$

**Upper bound.** B1

$$
O(kL)
$$

**Gap or comparison.** $O(L)=O(\log(N/k))$

**Comparison argument.** At most a logarithmic query gap in this window. A failure example for the greedy algorithm is not a lower bound against all algorithms.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Public integers $L,k\ge1$, $N=2^{L+1}k$, and target factor $\gamma\ge c_{\mathrm{HSS}}L$ for a sufficiently large universal constant. The fixed binary partition has $2k$ indices per leaf.

**Oracle mapping.** With $A$ hidden, query any $v,u\in\mathbb R^N$ to receive exact $Av$ or exact $A^{\mathsf T}u$ in separate calls. No independent entry or submatrix access is supplied.

**Guarantee mapping.**

$$
\mathbb{E}_{\omega}\|A-\widehat B\|_F^2\le\gamma\min_{B\in\operatorname{HSS}(L,k)}\|A-B\|_F^2
$$

**Output mapping.** Return $\widehat B\in\operatorname{HSS}(L,k)$.

**Resource mapping.** Sum of left and right single-vector responses.

### B1 - Algorithm 4.1 with sketch size s=5k

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(kL)
$$

**Sources.** [1](https://arxiv.org/abs/2505.16937v2)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**sum matvecs.** O(kL)

**Constants.** Universal.

**Source location.** [1](https://arxiv.org/abs/2505.16937v2) theorem: Theorem 4.1 (arXiv PDF pp. 13–14)

### B2 - Exact recovery of an arbitrary Gaussian diagonal leaf

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** all_admissible_algorithms

$$
\Omega(k)
$$

**Sources.** [1](https://arxiv.org/abs/2505.16937v2)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**sum matvecs.**

$$
\Omega(k)
$$

**Constants.** Universal.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/abs/2505.16937v2) theorem: Definition 2.3 (arXiv v2), telescoping HSS factorization

## 5. Local arguments

### A1 - Adaptive Gaussian leaf-block exact recovery

**Scope.** This local proof uses the paper's HSS definition and covers every adaptive randomized exact two-sided query algorithm.

Choose $A$ with only one nonzero diagonal leaf block of size $2k\times2k$, with independent standard Gaussian entries. Such a matrix lies in $\operatorname{HSS}(L,k)$ by using that block in $D^{(L)}$ and setting the other $D$ blocks to zero. The relative guarantee therefore requires exact recovery almost surely for every fixed $A$. Condition on the private seed. At each adaptive query, remove the known components in the spans of previous left and right queries. Conditional on the transcript, the unseen part of the leaf block on the two orthogonal complements is again a standard Gaussian matrix in transcript-measurable orthonormal coordinates. This follows inductively from orthogonal Gaussian conditioning: a fresh right or left query reveals one column or row of the current residual, and the remaining entries are independent. With fewer than $2k$ total queries both complements are nonzero, so the conditional law retains a continuous component and no transcript-measurable output can recover it exactly. Integrating over the seed and the Gaussian instance contradicts per-instance exact recovery.

## References

[1] Noah Amsel; Tyler Chen; Feyza Duman Keles; Diana Halikias; Cameron Musco; Christopher Musco; David Persson. Quasi-optimal hierarchically semi-separable matrix approximation. 2025.

https://arxiv.org/abs/2505.16937v2
