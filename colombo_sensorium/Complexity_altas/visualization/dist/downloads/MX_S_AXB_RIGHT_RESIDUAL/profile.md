# General nonsingular linear systems from right-only products: relative residual

**Setting ID.** `MX_S_AXB_RIGHT_RESIDUAL`

Matrix computation

A hidden general nonsingular square matrix is accessible only through right products. Even a perfectly conditioned orthogonal system can require a linear number of queries.

**Status.** Fully optimal

**TASK tags.** task family: Matrix computation; formulation: Linear system

**ORACLE tags.** feedback quality: Exact; operation: Matrix right matvec

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** object: Vector

**GUARANTEE tags.** confidence: Fixed numerical success / failure probability

**RESOURCE tags.** measure: Oracle calls

## 1. Setting specification

### Task

Return a vector $\widehat x$ satisfying the stated relative residual for the general nonsingular system $Ax=b$.

### Admissible model

$A\in\mathbb R^{n\times n}$ is nonsingular and $\sigma_{\max}(A)/\sigma_{\min}(A)\le\kappa$. No symmetry, positive definiteness, or absolute spectral scale is assumed.

$b\in\mathbb R^n$ is public and nonzero.

### Oracle interface

The only native access to $A$ is an exact right product $Av$ for any $v\in\mathbb R^n$. The oracle gives neither transpose products nor direct entry access.

### Output

Return one vector $\widehat x$, without a separate certificate.

### Loss or accuracy criterion

The success event is $\|A\widehat x-b\|_2\le\varepsilon\|b\|_2$.

### Resource accounting

Charge each individual right product. Exact arithmetic, including solving a fully recovered system, is free.

### Algorithm views and success guarantees

No Krylov, span, or zero-respecting restriction applies.

For every fixed admissible matrix and nonzero right hand side, require $\Pr_\omega[\|A\widehat x-b\|_2\le\varepsilon\|b\|_2]\ge 2/3$.

## 2. Notation and parameters

$n$: Positive integer **Domain:** Positive integer.

$\kappa$: Condition-number upper bound at least one **Domain:** Condition-number upper bound at least one.

$\varepsilon$: Positive relative residual tolerance **Domain:** Positive relative residual tolerance.

$A$: Hidden nonsingular matrix

$b$: Public nonzero right hand side

$n_0$: Sufficient dimension constant in Theorem 1.2

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
Q^\star(n,\kappa,\varepsilon)
$$

**Scope.** Worst case over matrices and right hand sides at the public dimension.

**Optimization direction.** minimize

### R1 - Half-relative-residual window

**Region.** $n\ge n_0$, $\kappa\ge1$, $0<\varepsilon\le 1/2$.

**Quantity.** Q1

**Resource.** Number of exact right products.

**Status.** Optimal

**Lower bound.** B2

$$
\left\lceil n/2\right\rceil
$$

**Upper bound.** B1

$$
n
$$

**Gap or comparison.** $\le2$

**Comparison argument.** The upper and lower budgets are within factor two.

### R2 - Higher-accuracy exact query-count window

**Region.** $n\ge n_0$, $\kappa\ge1$, $0<\varepsilon\le 0.2/\sqrt n$.

**Quantity.** Q1

**Resource.** Number of exact right products.

**Status.** Optimal

**Lower bound.** B4

$$
n
$$

**Upper bound.** B3

$$
n
$$

**Gap or comparison.** $1$

**Comparison argument.** The two envelopes agree exactly.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** The only native access to $A$ is an exact right product $Av$ for any $v\in\mathbb R^n$. The oracle gives neither transpose products nor direct entry access.

**Guarantee mapping.**

$$
\Pr_\omega[\|A\widehat x-b\|_2\le\varepsilon\|b\|_2]\ge 2/3
$$

### B1 - Query every basis vector and solve exactly

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
n
$$

**Conditions.** $n\ge n_0$, $\kappa\ge1$, $0<\varepsilon\le 1/2$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** n

**Constants.** No hidden query-count factor.

### B2 - Theorem 1.2, hidden Haar orthogonal matrix

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** all_admissible_algorithms

$$
\left\lceil n/2\right\rceil
$$

**Sources.** [1](https://arxiv.org/abs/2602.04842)

**Conditions.** $n\ge n_0$, $\kappa\ge1$, $0<\varepsilon\le 1/2$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.**

$$
\left\lceil n/2\right\rceil
$$

**Constants.** No hidden query-count factor.

**Source location.** [1](https://arxiv.org/abs/2602.04842) theorem: Theorem 1.2 and Section 3

### B3 - Query every basis vector and solve exactly

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
n
$$

**Conditions.** $n\ge n_0$, $\kappa\ge1$, $0<\varepsilon\le 0.2/\sqrt n$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** n

**Constants.** No hidden query-count factor.

### B4 - Theorem 1.2, hidden Haar orthogonal matrix

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** all_admissible_algorithms

$$
n
$$

**Sources.** [1](https://arxiv.org/abs/2602.04842)

**Conditions.** $n\ge n_0$, $\kappa\ge1$, $0<\varepsilon\le 0.2/\sqrt n$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** n

**Constants.** No hidden query-count factor.

**Source location.** [1](https://arxiv.org/abs/2602.04842) theorem: Theorem 1.2 and Section 3

## References

[1] Michał Dereziński; Ethan N. Epperly; Raphael A. Meyer. The matrix-vector complexity of Ax=b. 2026.

https://arxiv.org/abs/2602.04842
