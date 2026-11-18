# Square matrix multiplication: arithmetic exponent over a field

**Setting ID.** `MX_S_matmul_square`

Matrix computation

Compute $C=AB$ exactly.

**Status.** Other quantified gap present

**TASK tags.** formulation: Explicit matrix multiplication; solution concept: Arithmetic exponent; task family: Matrix computation

**MODEL tags.** spectral structure: Explicit field matrices; spectral structure: Square matrices

**ORACLE tags.** feedback quality: Exact; interface family: Explicit exact entries; operation: Explicit matrix input; public information: Public inputs explicitly declared

**ALGORITHMS tags.** computation: Exact field arithmetic; randomization: Deterministic

**OUTPUT tags.** certificate: No additional output certificate required; object: Matrix

**METRIC tags.** criterion: Arithmetic exponent

**GUARANTEE tags.** mode: Exact per instance

**RESOURCE tags.** measure: Arithmetic ops; measure: Input entries; measure: Input pairs; measure: Output entries

## 1. Setting specification

### Task

Compute $C=AB$ exactly.

### Admissible model

The quantity $A,B\in\mathbb{F}^{n\times n}$ is arbitrary. The field $\mathbb{F}$ is fixed in advance, and the matrix order is $n\to\infty$.

### Oracle interface

All input entries are supplied as exact field elements, with no hidden-matrix query interface. Addition, subtraction, and multiplication over the public field have unit arithmetic cost; associated preprocessing cannot be hidden for free.

### Output

Return every entry of the product $C$ exactly for all inputs.

### Loss or accuracy criterion

The base loss is $\mathbf1\{\widehat C\ne AB\}$ and must always be zero. Native complexity is the infimum exponent of exact arithmetic work.

### Resource accounting

Count field additions, subtractions, and multiplications, not bit operations. Preprocessing and internal algebra use the same cost unit. Field-element encoding length and communication scalarization are unspecified.

### Algorithm views and success guarantees

Algorithms are deterministic and use exact field arithmetic. General algorithm design, recursion, and preprocessing are allowed, but every field operation is charged. Communication and memory have no separate budgets. This arithmetic model is not replaced by an exact-real oracle model.

The output is exact for every input. The exponent describes worst-case work as n tends to infinity over a fixed field, with shape exponents also fixed in the rectangular case. No probabilistic success quantifier is involved.

**Budget convention.** Worst-case arithmetic count at each $n$, followed by the infimum asymptotic exponent as $n\to\infty$.

## 2. Notation and parameters

$\mathbb F$: The field fixed throughout the asymptotic matrix-multiplication problem. **Domain:** Any field, including a finite field.

$n$: The base asymptotic scale for matrix dimensions. **Domain:** $n\in\mathbb N,\ n\to\infty$.

$A,B$: The two fully explicit input matrices. **Domain:** $A,B\in\mathbb F^{n\times n}$.

$C$: The matrix product that must be returned exactly. **Domain:** $\mathbb F^{n\times n}$.

$C=AB$

$\langle r,s,t\rangle$: Bilinear tensor describing multiplication of an r-by-s matrix by an s-by-t matrix **Domain:** $r,s,t\in\mathbb N$.

$R_{\mathbb F}(\mathcal T)$: Tensor rank over the field F. **Domain:** Nonnegative integer.

$R_{\mathbb F}(\mathcal T)=\min\{R:\mathcal T=\sum_{i=1}^{R}u_i\otimes v_i\otimes w_i\}$

$T_{\mathbb F}(n)$: Worst-input field-operation count for the shape indexed by n. **Domain:** Addition, subtraction, and multiplication each have unit cost.

$\omega_{\mathbb F}$: Infimum field-arithmetic exponent for matrix multiplication of this shape **Domain:** Real number.

$\inf\{\rho:R_{\mathbb F}(\langle n,n,n\rangle)=O(n^\rho)\}$

$\zeta$: Arbitrary fixed positive slack allowed when translating the infimum exponent into an operation count **Domain:** $\zeta>0$.

$T_{\mathbb F}(n)=O_\zeta(n^{\omega+\zeta})$

$\rho$: Candidate real exponent over which the defining infimum is taken **Domain:** $\rho\in\mathbb R$.

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

## 3. Complexity bracket

### Compared quantities

#### Q1 - asymptotic exponent

$$
\omega_{\mathbb F}=\inf\{\rho:R_{\mathbb F}(\langle n,n,n\rangle)=O(n^\rho)\}
$$

**Scope.** Fix the computational field first. In the rectangular case, also fix $a,b,c$ before taking $n\to\infty$. The infimum exponent yields an arithmetic-work bound for every fixed positive slack.

**Optimization direction.** minimize

### R1 - Square-multiplication asymptotic exponent over a fixed field

**Region.** Fix an arbitrary field $\mathbb F$ before taking matrix order $n\to\infty$.

**Quantity.** Q1

**Resource.** The asymptotic arithmetic exponent over the specified field.

**Status.** Other quantified gap

**Lower bound.** B2

$$
2
$$

**Upper bound.** B1

$$
9/4
$$

**Gap or comparison.** $\frac94-2=\frac14$

**Comparison argument.** The bound $\omega_F\le9/4$ does not establish an endpoint running time $O(n^{9/4})$. It implies $O_\zeta(n^{9/4+\zeta})$ for every $\zeta>0$. An exponent gap is not an unqualified complexity ratio $n^{1/4}$.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Every entry of A and B is explicit, and the field F is fixed in advance. There is no hidden matrix–vector or block-query interface. Count all field operations needed to produce AB.

**Guarantee mapping.** The computation is deterministic and exact for all inputs. Fix the field before $n\to\infty$. Exponent upper bounds allow every fixed slack $\zeta>0$; there is no success-probability parameter.

**Output mapping.** Return the full $n\times n$ matrix $AB$ exactly. This is not approximate multiplication, randomized error, or an oracle-accuracy task.

**Resource mapping.** Count field additions, subtractions, and multiplications, not bit operations. Preprocessing and internal algebra use the same cost unit. Field-element encoding length and communication scalarization are unspecified.

### B1 - Deterministic field-arithmetic algorithm and upper bound on the square matrix-multiplication exponent

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\omega_{\mathbb{F}}\le\frac{9}{4}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.30054v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**arithmetic ops.** for every ζ>0: O_ζ(n^(9/4+ζ))

**input entries.**

$$
2n^2
$$

**output entries.**

$$
n^2
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/2610.30054v1) theorem: Theorem 1.1; definitions of exponent; section: §1; §2; pdf pages: 2; 3

The source states the result for every field F, with omega_F at most 9/4. The definition uses tensor rank and is equivalent to the arithmetic-circuit exponent. The preprint itself was obtained; the claim is not inferred from its abstract.

### B2 - Lower bound from matrix-multiplication tensor flattening and input-output dimensions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\omega_{\mathbb{F}}\ge2
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**tensor rank.** at least n²

**output entries.**

$$
n^2
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Local argument.** A1

## 5. Local arguments

### A1 - Matrix-multiplication tensor flattening and dimension lower bounds

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

The matrix-multiplication tensor has flattening rank n^2 in each input/output mode. The rank of a flattening is a lower bound on tensor rank. Standard bilinearization of an exact arithmetic circuit incurs only a constant factor in operation count, so the arithmetic exponent is at least 2.

## References

[1] Alimzhan Amanov; Maxim van den Berg; Jeroen Zuiddam. Multiplying matrices via polynomials: exposition and barriers. 2026. arXiv:2610.30054v1; submitted 2026-10-21; PDF dated 2026-10-22.

https://arxiv.org/pdf/2610.30054v1
