# Non-strict matrix saddlepoint search with binary comparisons

**Setting ID.** `CV_S_NONSTRICT_MATRIX_SADDLE_COMPARE`

Saddle-point problems

Find any pure saddlepoint of a hidden square matrix, or determine that it does not exist.

**Status.** Fully optimal

**TASK tags.** task family: Saddle point

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

**Local argument.** A1

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

**Local argument.** A2

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

**Local argument.** A2

## 5. Local arguments

### A1 - Row and column scan

**Scope.** Every square matrix, including ties

**Algorithm scope.** Deterministic witness

Find one maximum index in each row and one minimum index in each column using linear scans. For every cell, use comparisons in both directions to test equality with its row maximum and column minimum. Return the first cell satisfying both tests, or report absence if no cell does.

### A2 - One-cell regime

The only entry is both a row maximum and a column minimum. Output (1,1) immediately.

## References

[1] Justin Dallant; Frederik Haagensen; Riko Jacob; László Kozma; Sebastian Wild. An Optimal Randomized Algorithm for Finding the Saddlepoint. 2024.

https://doi.org/10.4230/LIPIcs.ESA.2024.44
