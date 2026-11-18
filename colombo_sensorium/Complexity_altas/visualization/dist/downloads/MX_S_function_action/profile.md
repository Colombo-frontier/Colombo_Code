# Matrix-function actions: exact products and absolute vector error.

**Setting ID.** `MX_S_function_action`

Matrix computation

Approximate $y^\star=h(A)b$, with the matrix function defined through real-symmetric spectral calculus.

**Status.** Bounds missing

**TASK tags.** formulation: Matrix function action; solution concept: Vector function error; task family: Matrix computation

**MODEL tags.** smoothness: Continuous; spectral structure: Symmetric spectral interval; spectral structure: Symmetric spectrum interval

**ORACLE tags.** feedback quality: Exact; interface family: Exact right matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Vector

**METRIC tags.** criterion: Absolute function action error

**GUARANTEE tags.** randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N right

## 1. Setting specification

### Task

Approximate $y^\star=h(A)b$, with the matrix function defined through real-symmetric spectral calculus.

### Admissible model

Assume $A=A^{\mathsf T}\in\mathbb{R}^{d\times d}$ with spectrum in $[a,\beta]$, $a\le\beta$, and the specified $\beta>0$. The public function $h:[a,\beta]\to\mathbb{R}$ is continuous, with $b\in\mathbb{R}^d\setminus\{0\}$.

### Oracle interface

The information $d,a,\beta,h,b,\varepsilon$ is public and $A$ is hidden. The only hidden-data interface returns exact $Av$ for any $v\in\mathbb{R}^d$. Scalar-function evaluation and polynomial-coefficient manipulation for the public function are uncharged internal computations; they do not reveal additional $h(A)b$.

### Output

Return any $\widehat{y}\in\mathbb{R}^d$, without restriction to a Krylov subspace and without an additional certificate.

### Loss or accuracy criterion

The base loss is $\|\widehat{y}-h(A)b\|_2/\|b\|_2$, and success requires it to be at most $\varepsilon$. Continuity on the compact interval ensures that $h(A)$ is finite.

### Resource accounting

Count right products with single vectors only: $N=N_{\mathrm r}$. A block of width $q$ costs $q$ calls.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using only public inputs. For every admissible input fixed before its private seed is generated, the success event has probability at least $2/3$ over that private randomness.

**Budget convention.** A fixed worst-case budget respected for every input and private seed.

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$a$: Left endpoint of the public spectral interval **Domain:** $a\in\mathbb R,\ a\le\beta$.

$\lambda_{\min}(A)\ge a$

$\beta$: The right endpoint of the public spectral interval, with β > 0 retained. **Domain:** $\beta>0,\ \beta\ge a$.

$\lambda_{\max}(A)\le\beta$

$\varepsilon$: Function-action error tolerance scaled by the Euclidean norm of the supplied vector. **Domain:** $\varepsilon>0$.

$\|\widehat y-h(A)b\|_2\le\varepsilon\|b\|_2$

$r_h(\varepsilon)$: Minimum nonnegative polynomial degree giving uniform error epsilon on the public spectral interval **Domain:** $r_h(\varepsilon)\in\mathbb N_0$.

$r_h(\varepsilon)=\min\{r\in\mathbb N_0:\inf_{q\in\mathbb R[z],\,\deg q\le r}\max_{z\in[a,\beta]}|h(z)-q(z)|\le\varepsilon\}$

$A$: The hidden real symmetric input matrix. **Domain:** $\mathbb R^{d\times d}$.

$h$: Public continuous scalar function **Domain:** $h:[a,\beta]\to\mathbb R$.

$b$: The public nonzero action vector. **Domain:** $\mathbb R^d\setminus\{0\}$.

$h(A)b$: The target matrix-function action. **Domain:** Defined by the input's spectral decomposition.

$A=U\operatorname{diag}(\lambda_i)U^{\mathsf T}\ \Longrightarrow\ h(A)b=U\operatorname{diag}(h(\lambda_i))U^{\mathsf T}b$

$\widehat y$: Approximate matrix-function action vector returned by the algorithm **Domain:** $\mathbb R^d$.

$q,r$: Uniform approximation polynomial and the nonnegative upper bound on its degree **Domain:** $q\in\mathbb R[z],\ r\in\mathbb N_0$.

$\deg q\le r$

$t$: The maximum number of exact Lanczos calls. **Domain:** $\mathbb N$.

$t=1+r_h(\varepsilon/2)$

$\lambda_i(A)$: Eigenvalues of a real symmetric or Hermitian matrix in nonincreasing order. **Domain:** $1\le i\le d$.

$\lambda_1(A)\ge\cdots\ge\lambda_d(A)$

$\|z\|_2$: Euclidean norm of a vector **Domain:** Finite-dimensional real or complex vector.

$\|z\|_2=(\sum_i|z_i|^2)^{1/2}$

$\|M\|_{\mathrm{op}}$: The matrix operator norm induced by the Euclidean norm. **Domain:** Any compatible matrix.

$\|M\|_{\mathrm{op}}=\max_{\|z\|_2=1}\|Mz\|_2=\sigma_1(M)$

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

$N,N_{\mathrm r}$: Single-vector query budget for exact right products Av. A block is charged by its column count. **Domain:** $\mathbb N_0$.

$N=N_{\mathrm r}$

$N^\star$: Minimum worst-case query budget attaining this profile's success guarantee **Domain:** $\mathbb N_0\cup\{+\infty\}$.

The quantity is $N^\star=\inf_{\mathcal A}\sup_{I,\omega}N_{\mathcal A}(I,\omega)$, where the infimum ranges over admissible algorithms satisfying this profile's success guarantee.

$\mathcal A,I,\omega$: The algorithm, fixed admissible input, and private algorithmic seed. **Domain:** Quantifiers for worst-case input and execution cost. Success probability is taken over ω.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon;d,h,[a,\beta])
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - Polynomial-approximation regime for a continuous function

**Region.** Assume $d\ge1$, $a<\beta$, and $\varepsilon>0$. The function $h$ is continuous on the public spectral interval; polynomial coefficients are handled by the exact internal computation permitted by the specification.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1, B2, B3

$$
\min\{d,r_h(\varepsilon),1+r_h(\varepsilon/2)\}
$$

**Comparison argument.** This is an envelope of feasible algorithms depending on the public function. A minimax lower bound over arbitrary algorithms remains unverified.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Only exact Av products are available; h and b are public. Scalar h evaluations and functions of known compressed matrices do not count as matrix–vector products. Neither h(A)v nor a shifted inverse is an oracle primitive.

**Guarantee mapping.** The three verified upper bounds are deterministic exact-arithmetic algorithms and satisfy the required success probability of at least 2/3. No randomized lower bound follows from this.

**Output mapping.** Return y_hat ∈ R^d satisfying ‖y_hat − h(A)b‖₂ ≤ ε‖b‖₂. The known function h and spectral interval remain part of the specification.

**Resource mapping.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

### B1 - Deterministic evaluation of the best uniform polynomial approximation.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le r_h(\varepsilon)
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\le r_h(\varepsilon)
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Local argument.** A1

### B2 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\le d
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Local argument.** A2

### B3 - Deterministic exact Lanczos approximation of matrix functions

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le1+r_h(\varepsilon/2)
$$

**Sources.** [1](https://arxiv.org/pdf/1708.07788v2)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\le1+r_h(\varepsilon/2)
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/1708.07788v2) theorem: Theorem 6; Lemma 7; section: §4.1; pdf pages: 9; equations: (9)

Original PDF page 9, printed page 8: exact Lanczos error is at most twice the best uniform approximation error among polynomials of degree below $t$.

## 5. Local arguments

### A1 - Deterministic evaluation of the best uniform polynomial approximation.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

By the definition of r_h(epsilon), choose a public polynomial p of degree r_h(epsilon) with max_{lambda in [a,b]}|p(lambda)-h(lambda)|<=epsilon. The spectral theorem gives ||p(A)b-h(A)b||_2<=epsilon||b||_2. Horner evaluation of p(A)b uses at most r_h(epsilon) exact matrix-vector products. All coefficients and scalar computations depend only on public h and the public spectral interval.

### A2 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Recover $A$ using $d$ standard basis queries. Exact internal spectral decomposition and the public scalar function $h$ determine $h(A)b$. The vector error is zero. This uses only the admitted exact-real internal computation and adds no matrix-function oracle.

## References

[1] Cameron Musco; Christopher Musco; Aaron Sidford. Stability of the Lanczos Method for Matrix Function Approximation. 2018. arXiv:1708.07788v2, revised 2024-11-18; SODA 2018.

https://arxiv.org/pdf/1708.07788v2
