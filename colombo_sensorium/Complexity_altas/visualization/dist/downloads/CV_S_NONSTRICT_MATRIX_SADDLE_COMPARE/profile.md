# Non-strict matrix saddlepoint search with binary comparisons

**Setting ID.** `CV_S_NONSTRICT_MATRIX_SADDLE_COMPARE`

Matrix computation

Find any pure saddlepoint of a hidden square matrix, or determine that it does not exist.

**Status.** Fully optimal

**TASK tags.** task family: Matrix computation

**MODEL tags.** spectral structure: Arbitrary real matrix

**ORACLE tags.** interface family: Exact comparison; feedback quality: Exact

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Uniform fixed-confidence identification correctness

**GUARANTEE tags.** mode: Uniform fixed-confidence identification correctness

**RESOURCE tags.** measure: Oracle calls; budget: Worst-instance expected cost

## 1. Setting specification

### Task

Find an entry attaining its row maximum and column minimum. If no such entry exists, report absence. Ties are permitted. Return any qualifying index when there are several.

### Admissible model

Fix $A\in\mathbb R^{n\times n}$. Entries may repeat. A non-strict saddlepoint may be absent or nonunique.

### Oracle interface

Choose any ordered pair of matrix cells and receive the exact bit $\mathbf{1}\{A_{ij}<A_{\ell k}\}$. Equality can be identified with a second query in the reverse direction.

The interface reveals only the comparison bits.

### Output

Return any $(i,j)\in[n]\times[n]$ satisfying both inequalities, or $\bot$ exactly when no such entry exists.

### Loss or accuracy criterion

Let $S(A)$ be the set of acceptable outputs: all saddlepoint indices, or $\{\bot\}$ if the matrix has none. The identification error is $\mathbf{1}\{\widehat s\notin S(A)\}$.

### Resource accounting

Each ordered binary comparison costs one unit. For each fixed matrix take the expectation over private randomness, then take the supremum over matrices. The cost includes all comparisons made.

### Algorithm views and success guarantees

Any adaptive comparison strategy with a private seed independent of the matrix is admissible.

For every fixed admissible matrix $A$, the algorithm returns a correct index or absence verdict with probability at least $5/6$ over its own randomness.

## 2. Notation and parameters

$n$: Number of rows and columns **Domain:** $\mathbb N_{\ge1}$.

The public side length of the square matrix.

$A$: Fixed hidden real matrix **Domain:** $\mathbb R^{n\times n}$.

The algorithm only accesses comparisons between its entries.

$N$: Number of charged binary comparisons **Domain:** $\mathbb N_{\ge0}$.

One comparison request costs one unit, regardless of the chosen pair.

$\bot$: No saddlepoint exists **Domain:** Output symbol.

The correct output if no saddlepoint exists.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(n)=\inf_{\mathcal A:\,\forall A\ \Pr(\widehat s\in S(A))\ge5/6}\ \sup_A\mathbb E[N_{\mathcal A}(A)]
$$

**Definition.** Minimum worst-instance expected comparisons at fixed confidence

**Scope.** All adaptive randomized comparison algorithms on the full square-matrix instance class.

**Optimization direction.** minimize

### R1 - At least two rows and columns

**Region.** $n\ge2$

**Quantity.** Q1

**Resource.** Worst-instance expected number of charged binary comparisons.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(n^2)
$$

**Upper bound.** B1

$$
O(n^2)
$$

**Gap or comparison.** $\Theta(n^2)$

**Comparison argument.** Matching bounds throughout the stated matrix-shape regime.

### R2 - One cell

**Region.** $n=1$

**Quantity.** Q1

**Resource.** Worst-instance expected number of charged binary comparisons.

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

**Guarantee mapping.** Success probability at least 5/6 on every fixed matrix.

**Resource mapping.** Worst-instance expected comparisons.

### B1 - Row and column scan

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Algorithmic witness: Deterministic witness

$$
O(n^2)
$$

**Conditions.** $n\ge2$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**oracle calls.**

$$
O(n^2)
$$

**Local argument.** CV_S_NONSTRICT_MATRIX_SADDLE_COMPARE__proof_lower

### B2 - Randomized entry-query lower bound

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All algorithm necessity: all_admissible_algorithms

$$
\Omega(n^2)
$$

**Sources.** [1](https://doi.org/10.4230/LIPIcs.ESA.2024.44)

**Conditions.** $n\ge2$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**oracle calls.**

$$
\Omega(n^2)
$$

**Derivation.** Given a comparison algorithm for the coordinate-or-absence output, simulate each comparison by reading at most two values. On a coordinate output, use at most one additional read to recover the alleged saddlepoint value. A correct output gives the correct decision and value. Therefore the randomized entry-read lower bound in Theorem 15 at success probability 5/6 also bounds worst-instance expected comparison cost up to a constant factor and one read.

**Source location.** [1](https://doi.org/10.4230/LIPIcs.ESA.2024.44) theorem: Theorems 2 and 15; pdf pages: 2; 10; 11

Given a comparison algorithm for the coordinate-or-absence output, simulate each comparison by reading at most two values. On a coordinate output, use at most one additional read to recover the alleged saddlepoint value. A correct output gives the correct decision and value. Therefore the randomized entry-read lower bound in Theorem 15 at success probability 5/6 also bounds worst-instance expected comparison cost up to a constant factor and one read.

### B3 - One-cell regime

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Algorithmic witness: Deterministic witness

$$
0
$$

**Conditions.** $n=1$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**oracle calls.** 0

**Local argument.** CV_S_NONSTRICT_MATRIX_SADDLE_COMPARE__proof_trivial

### B4 - One-cell regime

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All algorithm necessity: all_admissible_algorithms

$$
0
$$

**Conditions.** $n=1$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**oracle calls.** 0

**Local argument.** CV_S_NONSTRICT_MATRIX_SADDLE_COMPARE__proof_trivial

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 68b55b77b1381b0ad7463cd01eb24320e2d56f426b657a3ed0d3ca67e5cfaeaf

### Native proof: CV_S_NONSTRICT_MATRIX_SADDLE_COMPARE__proof_lower

Native pointer: /proofs/0; canonical SHA-256: 26a00dd85e5ce3a6ee296925c82ce07b9b4f3bde0e3f1bac6c4a2eaa0ae2211b

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 71460a316a859b67e7f3401eb031b6684123771b599a1a1a6c8064abf942fb56

Row and column scan

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: b3ba1584f9570198058a582b320263c860a09e63528aa2ed9bc02412c301f049

#### Native item 1

Native pointer: /proofs/0/body/0; canonical SHA-256: b4d7f0e815c9cedbae5246d41ced4ae924feb43352e0f4c23e9fe88ca1e6534a

Find one maximum index in each row and one minimum index in each column using linear scans. For every cell, use comparisons in both directions to test equality with its row maximum and column minimum. Return the first cell satisfying both tests, or report absence if no cell does.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 7f83c3fcaa9c1f8e6432511eefdec9f8ddf6ce22c6e673a6678043dd6f386ed1

Every square matrix, including ties

#### Native field: algorithm_scope

Native pointer: /proofs/0/algorithm_scope; canonical SHA-256: 808c15dc7cffa4531c874c27b9a4e0e45083b19352286b52766061bf5b740519

Deterministic witness

### Native proof: CV_S_NONSTRICT_MATRIX_SADDLE_COMPARE__proof_trivial

Native pointer: /proofs/1; canonical SHA-256: 7c944168e4da2bdbe3c14714e3baa6637d9f2be7454a1b1027a4456bd9bb1b60

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 4ff6d589d6c03c013858562f2186fd7040d3112b2bb7b030c84c53b29f095419

One-cell regime

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 4f415f659510758932c2a32660b8d020ee9179d9088444d171e655f98a537add

#### Native item 1

Native pointer: /proofs/1/body/0; canonical SHA-256: 6aa0ce5cba2f1c538cd3bf107126862ba491d5478953de8288a0612ecc3aaa28

The only entry is both a row maximum and a column minimum. Output (1,1) immediately.

## References

[1] Justin Dallant; Frederik Haagensen; Riko Jacob; László Kozma; Sebastian Wild. An Optimal Randomized Algorithm for Finding the Saddlepoint. 2024.

https://doi.org/10.4230/LIPIcs.ESA.2024.44
