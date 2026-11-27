# Strict matrix saddlepoint search with binary comparisons

**Setting ID.** `CV_S_STRICT_MATRIX_SADDLE_COMPARE`

Matrix computation

Find the unique strict pure saddlepoint of a hidden matrix, or determine that it does not exist.

**Status.** Fully optimal

**TASK tags.** task family: Matrix computation

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

**Local argument.** CV_S_STRICT_MATRIX_SADDLE_COMPARE__proof_lower

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

**Local argument.** CV_S_STRICT_MATRIX_SADDLE_COMPARE__proof_trivial

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

**Local argument.** CV_S_STRICT_MATRIX_SADDLE_COMPARE__proof_trivial

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: c46a1b2b3f198b8a2a2a5a765652d59b60ebf9ef53828d2b1c75fe8856d711b1

### Native proof: CV_S_STRICT_MATRIX_SADDLE_COMPARE__proof_lower

Native pointer: /proofs/0; canonical SHA-256: 7c9602524374a69719d593102396328d7f90b4e685d1a9bb6ff9b06815667a04

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 335b8097e25deec08815853715a20fd654b53629139965675431c4e5a4cbe1de

Unqueried cell adversary

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 9e59c6af1c9dac85eb648655dc49413034a57a6ad942be077cdef69ea29fe409

#### Native item 1

Native pointer: /proofs/0/body/0; canonical SHA-256: a758f7640209464dee33f60048650faf9252dbbb902e73301342a08a597fd4d9

Fix a matrix with strict saddlepoint (1,1). A comparison transcript that never uses one of the other entries in row 1 or column 1 is identical after changing that entry to equal A[1,1]. The alteration invalidates the output (1,1). Every one of the m+n-2 other row and column cells must therefore occur in the transcript. A comparison touches at most two of them.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: a053becd94cef93c341e71a960e4d4c083510126f16ad34701731a9d095d7a86

At least two cells

#### Native field: algorithm_scope

Native pointer: /proofs/0/algorithm_scope; canonical SHA-256: 7eb20316807a3d4ca053e5a372c3090909fc6fefcee306256d66ad01d39f78e1

All deterministic adaptive comparison algorithms

### Native proof: CV_S_STRICT_MATRIX_SADDLE_COMPARE__proof_trivial

Native pointer: /proofs/1; canonical SHA-256: f70c64549bed558a21093fc06b372e329e3f0e242a73a2eb5ea7be9d2e81241c

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 4ff6d589d6c03c013858562f2186fd7040d3112b2bb7b030c84c53b29f095419

One-cell regime

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: f44394792b2d4a172eefc35596ab7c47569a373d08478d65b72ba2dba0ccd629

#### Native item 1

Native pointer: /proofs/1/body/0; canonical SHA-256: b9c1406c048e26d2d42813e4aa808699a41376d274266462ee43a1f3f260b635

In a one-entry matrix both strict inequality systems are vacuous. Output (1,1) immediately.

## References

[1] Justin Dallant. An optimal deterministic algorithm for finding a strict saddlepoint. 2026. arXiv:2607.22312v1 (24 July 2026).

https://arxiv.org/abs/2607.22312v1

[2] Justin Dallant; Frederik Haagensen; Riko Jacob; László Kozma; Sebastian Wild. An Optimal Randomized Algorithm for Finding the Saddlepoint. 2024.

https://doi.org/10.4230/LIPIcs.ESA.2024.44
