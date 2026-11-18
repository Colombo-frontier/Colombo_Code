# Strict matrix saddlepoint search with binary comparisons

**Setting ID.** `CV_S_STRICT_MATRIX_SADDLE_COMPARE`

Saddle-point problems

Find the unique strict pure saddlepoint of a hidden matrix, or determine that it does not exist.

**Status.** Fully optimal

**TASK tags.** task family: Saddle point

**MODEL tags.** spectral structure: Arbitrary real matrix

**ORACLE tags.** interface family: Exact comparison; feedback quality: Exact

**ALGORITHMS tags.** randomization: Deterministic algorithms

**OUTPUT tags.** certificate: No additional output certificate required

**GUARANTEE tags.** mode: Exact per instance

**RESOURCE tags.** measure: Oracle calls

## 1. Setting specification

### Task

Identify the unique matrix entry that is strictly largest in its row and strictly smallest in its column. If no such entry exists, report absence.

### Admissible model

Fix $A\in\mathbb R^{m\times n}$. Entries may repeat. A strict saddlepoint, when it exists, is unique.

### Oracle interface

Choose any ordered pair of matrix cells and receive the exact bit $\mathbf{1}\{A_{ij}<A_{\ell k}\}$. Equality can be identified with a second query in the reverse direction.

The interface reveals only the comparison bits.

### Output

Return $(i,j)\in[m]\times[n]$ satisfying both strict inequalities, or $\bot$ if no such entry exists.

### Loss or accuracy criterion

Let $s(A)$ be the unique strict saddlepoint index, or $\bot$ when absent. The exact identification error is $\mathbf{1}\{\widehat{s}\ne s(A)\}$.

### Resource accounting

Each ordered binary comparison costs one unit. The bracket measures comparison calls. The source upper bound additionally holds for total unit-cost running time.

### Algorithm views and success guarantees

The next comparison and final output may depend on all preceding replies. Any deterministic comparison strategy is admissible.

The algorithm must return the exact index or correct absence verdict on every input matrix.

## 2. Notation and parameters

$m$: Number of rows **Domain:** $\mathbb N_{\ge1}$.

$n$: Number of columns **Domain:** $\mathbb N_{\ge1}$.

$A$: Fixed hidden real matrix **Domain:** $\mathbb R^{m\times n}$.

The algorithm only accesses comparisons between its entries.

$N$: Number of charged binary comparisons **Domain:** $\mathbb N_{\ge0}$.

One comparison request costs one unit, regardless of the chosen pair.

$\bot$: No strict saddlepoint exists **Domain:** Output symbol.

Return this symbol exactly when no strict saddlepoint exists.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(m,n)=\inf_{\mathcal A\text{ exact}}\ \sup_{A\in\mathbb R^{m\times n}}N_{\mathcal A}(A)
$$

**Definition.** Minimum worst-case comparison count for exact identification

**Scope.** All deterministic comparison algorithms solving the entire fixed-shape instance class.

**Optimization direction.** minimize

### R1 - At least two cells

**Region.** $m,n\ge1$ and $m+n\ge3$

**Quantity.** Q1

**Resource.** Number of charged binary comparisons.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(m+n)
$$

**Upper bound.** B1

$$
O(m+n)
$$

**Gap or comparison.** $\Theta(m+n)$

**Comparison argument.** Matching bounds throughout the stated matrix-shape regime.

### R2 - One cell

**Region.** $m=n=1$

**Quantity.** Q1

**Resource.** Number of charged binary comparisons.

**Status.** Optimal

**Lower bound.** B4

$$
0
$$

**Upper bound.** B3

$$
0
$$

**Gap or comparison.** $0$

**Comparison argument.** Matching bounds throughout the stated matrix-shape regime.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact ordered binary comparisons.

**Guarantee mapping.** Exact identification on all inputs of the fixed shape.

**Resource mapping.** Count binary comparisons, including verification.

### B1 - Linear-time comparison search of Dallant

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Algorithmic witness: Deterministic witness

$$
O(m+n)
$$

**Sources.** [1](https://arxiv.org/abs/2607.22312v1)

**Conditions.** $m,n\ge1$ and $m+n\ge3$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**oracle calls.** O(m+n)

**Source location.** [1](https://arxiv.org/abs/2607.22312v1) theorem: Theorem 1.1 and Sections 4–5; pdf pages: 2; 6; 7

Dallant 2026 gives a deterministic linear-time comparison algorithm. It removes a constant fraction of the longer dimension at each stage using selection across monotone prefix-maximum lists. An index tie-break handles repeated keys, followed by strict verification using the original keys. Section 5 extends the bound to rectangular matrices.

### B2 - Unqueried cell adversary

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All algorithm necessity: all_admissible_algorithms

$$
\Omega(m+n)
$$

**Sources.** [1](https://arxiv.org/abs/2607.22312v1)

**Conditions.** $m,n\ge1$ and $m+n\ge3$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**oracle calls.**

$$
\Omega(m+n)
$$

**Local argument.** A1

**Source location.** [1](https://arxiv.org/abs/2607.22312v1) theorem: Discussion following Theorem 1.1; pdf pages: 2

The proof record gives an indistinguishability argument covering arbitrary comparisons and rectangular matrices.

### B3 - One-cell regime

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Algorithmic witness: Deterministic witness

$$
0
$$

**Conditions.** $m=n=1$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**oracle calls.** 0

**Local argument.** A2

### B4 - One-cell regime

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All algorithm necessity: all_admissible_algorithms

$$
0
$$

**Conditions.** $m=n=1$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**oracle calls.** 0

**Local argument.** A2

## 5. Local arguments

### A1 - Unqueried cell adversary

**Scope.** At least two cells

**Algorithm scope.** All deterministic adaptive comparison algorithms

Fix a matrix with strict saddlepoint (1,1). A comparison transcript that never uses one of the other entries in row 1 or column 1 is identical after changing that entry to equal A[1,1]. The alteration invalidates the output (1,1). Every one of the m+n-2 other row and column cells must therefore occur in the transcript. A comparison touches at most two of them.

### A2 - One-cell regime

In a one-entry matrix both strict inequality systems are vacuous. Output (1,1) immediately.

## References

[1] Justin Dallant. An optimal deterministic algorithm for finding a strict saddlepoint. 2026. arXiv:2607.22312v1 (24 July 2026).

https://arxiv.org/abs/2607.22312v1

[2] Justin Dallant; Frederik Haagensen; Riko Jacob; László Kozma; Sebastian Wild. An Optimal Randomized Algorithm for Finding the Saddlepoint. 2024.

https://doi.org/10.4230/LIPIcs.ESA.2024.44
