# Rectangular matrix multiplication: arithmetic exponent over a field

**Setting ID.** `MX_S_matmul_rect`

Matrix computation

Compute $C=AB$ exactly.

**Status.** Other quantified gap present

**TASK tags.** formulation: Explicit matrix multiplication; solution concept: Arithmetic exponent; task family: Matrix computation

**MODEL tags.** spectral structure: Explicit field matrices; spectral structure: Fixed rectangular shape

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

Assume $A\in\mathbb{F}^{\lceil n^a\rceil\times\lceil n^b\rceil}$ and $B\in\mathbb{F}^{\lceil n^b\rceil\times\lceil n^c\rceil}$. The field $\mathbb{F}$ and real shape exponents $a\ge b\ge c>0$ are fixed in advance, with $n\to\infty$.

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

$a$: Exponent of the row dimension of the first input matrix **Domain:** $a\ge b\ge c>0$, all fixed before $n$.

$A\in\mathbb F^{\lceil n^a\rceil\times\lceil n^b\rceil}$

$b$: The exponent of the shared inner dimension of the input matrices. **Domain:** $a\ge b\ge c>0$, all fixed before $n$.

The column count of $A$ and row count of $B$ are both $\lceil n^b\rceil$.

$c$: The column-dimension exponent of the second input matrix. **Domain:** $a\ge b\ge c>0$, all fixed before $n$.

$B\in\mathbb F^{\lceil n^b\rceil\times\lceil n^c\rceil}$

$A,B$: The two fully explicit input matrices. **Domain:** $A\in\mathbb F^{\lceil n^a\rceil\times\lceil n^b\rceil},\ B\in\mathbb F^{\lceil n^b\rceil\times\lceil n^c\rceil}$.

$C$: The matrix product that must be returned exactly. **Domain:** $\mathbb F^{\lceil n^a\rceil\times\lceil n^c\rceil}$.

$C=AB$

$\langle r,s,t\rangle$: Bilinear tensor describing multiplication of an r-by-s matrix by an s-by-t matrix **Domain:** $r,s,t\in\mathbb N$.

$R_{\mathbb F}(\mathcal T)$: Tensor rank over the field F. **Domain:** Nonnegative integer.

$R_{\mathbb F}(\mathcal T)=\min\{R:\mathcal T=\sum_{i=1}^{R}u_i\otimes v_i\otimes w_i\}$

$T_{\mathbb F}(n)$: Worst-input field-operation count for the shape indexed by n. **Domain:** Addition, subtraction, and multiplication each have unit cost.

$\omega_{\mathbb F}(a,b,c)$: Infimum field-arithmetic exponent for matrix multiplication of this shape **Domain:** Real number.

$\inf\{\rho:R_{\mathbb F}(\langle\lceil n^a\rceil,\lceil n^b\rceil,\lceil n^c\rceil\rangle)=O(n^\rho)\}$

$\zeta$: Arbitrary fixed positive slack allowed when translating the infimum exponent into an operation count **Domain:** $\zeta>0$.

$T_{\mathbb F}(n)=O_\zeta(n^{\omega+\zeta})$

$\rho$: Candidate real exponent over which the defining infimum is taken **Domain:** $\rho\in\mathbb R$.

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

## 3. Complexity bracket

### Compared quantities

#### Q1 - asymptotic exponent

$$
\omega_{\mathbb F}(a,b,c)=\inf\{\rho:R_{\mathbb F}(\langle\lceil n^a\rceil,\lceil n^b\rceil,\lceil n^c\rceil\rangle)=O(n^\rho)\}
$$

**Scope.** Fix the computational field first. In the rectangular case, also fix $a,b,c$ before taking $n\to\infty$. The infimum exponent yields an arithmetic-work bound for every fixed positive slack.

**Optimization direction.** minimize

### R1 - Matching-exponent regime for thin rectangular matrices

**Region.** First fix the domain $\mathbb{F}$ and shape exponent $a\ge b\ge c>0$ satisfying $c(a+b)\le ab$, then define the base scale $n\to\infty$.

**Quantity.** Q1

**Resource.** The asymptotic arithmetic exponent over the specified field.

**Status.** Optimal

**Lower bound.** B2

$$
a+b
$$

**Upper bound.** B1

$$
a+b
$$

**Gap or comparison.** $0$

**Comparison argument.** The dimension ordering is $a\ge b\ge c$. There is no general conversion between exponents and query counts.

### R2 - Exponent-gap regime for thicker rectangular matrices

**Region.** First fix the domain $\mathbb{F}$ and shape exponent $a\ge b\ge c>0$ satisfying $c(a+b)>ab$, then set the base scale $n\to\infty$.

**Quantity.** Q1

**Resource.** The asymptotic arithmetic exponent over the specified field.

**Status.** Other quantified gap

**Lower bound.** B4

$$
a+b
$$

**Upper bound.** B3

$$
(ab+bc+ca)^2/(4abc)
$$

**Gap or comparison.** $\frac{(ab+bc+ca)^2}{4abc}-(a+b)$. The comparison concerns an asymptotic arithmetic-exponent gap.

**Comparison argument.** The dimension ordering is $a\ge b\ge c$. There is no general conversion between exponents and query counts.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Dimension-compatible A and B are fully explicit and readable, with fixed field F and shape exponents a>=b>=c>0. There is no matrix–vector query cost.

**Guarantee mapping.** For each fixed field and shape, the result is exact on all inputs. The asymptotic exponent as n → ∞ allows any fixed slack ζ > 0. The original thin and thick regions are retained.

**Output mapping.** Return the exact ceil(n^a) × ceil(n^c) product AB. Dimensions and shape parameters belong to the explicit input, not to a freely chosen query block.

**Resource mapping.** Count field additions, subtractions, and multiplications, not bit operations. Preprocessing and internal algebra use the same cost unit. Field-element encoding length and communication scalarization are unspecified.

### B1 - An exponent upper bound for deterministic rectangular field arithmetic.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\omega_{\mathbb{F}}(a,b,c)\le a+b
$$

**Sources.** [1](https://arxiv.org/pdf/2610.30054v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**arithmetic ops.** for every ζ>0: O_ζ(n^(a+b+ζ))

**input entries.** ceil(n^a)ceil(n^b)+ceil(n^b)ceil(n^c)

**output entries.** ceil(n^a)ceil(n^c)

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/2610.30054v1) theorem: Theorem 1.2; Corollary 4.17; section: §1; §4; pdf pages: 2

Fix shape exponents $a\ge b\ge c>0$. If $c(a+b)\le ab$, the rectangular multiplication exponent is exactly $\omega_{\mathbb F}(a,b,c)=a+b$. If $c(a+b)>ab$, the recorded bracket is $a+b\le\omega_{\mathbb F}(a,b,c)\le(ab+bc+ca)^2/(4abc)$. These statements compare asymptotic arithmetic exponents; an infimum exponent does not by itself give an endpoint operation bound $O(n^\omega)$.

### B2 - A flattening lower bound for the matrix-multiplication tensor.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\omega_{\mathbb{F}}(a,b,c)\ge a+b
$$

**Sources.** [1](https://arxiv.org/pdf/2610.30054v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**tensor rank.**

$$
\Omega (n^{a+b})
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/pdf/2610.30054v1) theorem: Theorem 1.2; Corollary 4.17; section: §1; §4; pdf pages: 2

Fix shape exponents $a\ge b\ge c>0$. If $c(a+b)\le ab$, the rectangular multiplication exponent is exactly $\omega_{\mathbb F}(a,b,c)=a+b$. If $c(a+b)>ab$, the recorded bracket is $a+b\le\omega_{\mathbb F}(a,b,c)\le(ab+bc+ca)^2/(4abc)$. These statements compare asymptotic arithmetic exponents; an infimum exponent does not by itself give an endpoint operation bound $O(n^\omega)$.

### B3 - An exponent upper bound for deterministic rectangular field arithmetic.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\omega_{\mathbb{F}}(a,b,c)\le\frac{(ab+bc+ca)^2}{4abc}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.30054v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**arithmetic ops.** for every ζ>0: O_ζ(n^((ab+bc+ca)^2/(4abc)+ζ))

**input entries.** ceil(n^a)ceil(n^b)+ceil(n^b)ceil(n^c)

**output entries.** ceil(n^a)ceil(n^c)

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/2610.30054v1) theorem: Theorem 1.2; Corollary 4.17; section: §1; §4; pdf pages: 2

Fix shape exponents $a\ge b\ge c>0$. If $c(a+b)\le ab$, the rectangular multiplication exponent is exactly $\omega_{\mathbb F}(a,b,c)=a+b$. If $c(a+b)>ab$, the recorded bracket is $a+b\le\omega_{\mathbb F}(a,b,c)\le(ab+bc+ca)^2/(4abc)$. These statements compare asymptotic arithmetic exponents; an infimum exponent does not by itself give an endpoint operation bound $O(n^\omega)$.

### B4 - A flattening lower bound for the matrix-multiplication tensor.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\omega_{\mathbb{F}}(a,b,c)\ge a+b
$$

**Sources.** [1](https://arxiv.org/pdf/2610.30054v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**tensor rank.**

$$
\Omega (n^{a+b})
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/pdf/2610.30054v1) theorem: Theorem 1.2; Corollary 4.17; section: §1; §4; pdf pages: 2

Fix shape exponents $a\ge b\ge c>0$. If $c(a+b)\le ab$, the rectangular multiplication exponent is exactly $\omega_{\mathbb F}(a,b,c)=a+b$. If $c(a+b)>ab$, the recorded bracket is $a+b\le\omega_{\mathbb F}(a,b,c)\le(ab+bc+ca)^2/(4abc)$. These statements compare asymptotic arithmetic exponents; an infimum exponent does not by itself give an endpoint operation bound $O(n^\omega)$.

## 5. Local arguments

### A1 - A flattening lower bound for the matrix-multiplication tensor.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

For multiplying an n^a by n^b matrix by an n^b by n^c matrix, the three flattening ranks of the matrix-multiplication tensor have exponents a+b, b+c, and a+c. Tensor rank is at least their maximum. Under a>=b>=c>0 this maximum is a+b. Bilinearization changes arithmetic complexity by only a constant factor, so omega_F(a,b,c)>=a+b.

**Sources.** [1](https://arxiv.org/pdf/2610.30054v1)

## References

[1] Alimzhan Amanov; Maxim van den Berg; Jeroen Zuiddam. Multiplying matrices via polynomials: exposition and barriers. 2026. arXiv:2610.30054v1; submitted 2026-10-21; PDF dated 2026-10-22.

https://arxiv.org/pdf/2610.30054v1
