# Leading-eigenvalue approximation without a spectral gap: relative Rayleigh error.

**Setting ID.** `MX_S_rayleigh`

Matrix computation

Find a unit vector $\widehat{v}$ such that $\widehat{v}^{\mathsf T}A\widehat{v}$ approximates $\lambda_1(A)$.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Dominant eigenpair; solution concept: Relative rayleigh gap; task family: Matrix computation

**MODEL tags.** spectral structure: Positive semidefinite; spectral structure: Psd gap free

**ORACLE tags.** feedback quality: Exact; interface family: Exact right matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Vector

**METRIC tags.** criterion: Relative rayleigh error

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N right

## 1. Setting specification

### Task

Find a unit vector $\widehat{v}$ such that $\widehat{v}^{\mathsf T}A\widehat{v}$ approximates $\lambda_1(A)$.

### Admissible model

Assume $A=A^{\mathsf T}\succeq0$, $A\in\mathbb{R}^{d\times d}$, and $\lambda_1(A)>0$; the largest eigenvalue may have multiplicity greater than one.

### Oracle interface

The data $d,\varepsilon$ are public and $A$ is hidden. Any query $v\in\mathbb{R}^d$ returns exact $Av$. Queries have no norm restriction and may be adaptive or repeated.

### Output

Return a unit vector $\widehat v\in\mathbb R^d$. It need not have been queried. No separate largest-eigenvalue estimate or certificate is required.

### Loss or accuracy criterion

The base loss is $\ell(\widehat{v})=(\lambda_1(A)-\widehat{v}^{\mathsf T}A\widehat{v})/\lambda_1(A)$ and success requires $\ell\le\varepsilon$. Its denominator is positive under the nonzero positive-semidefinite promise.

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

$\varepsilon$: Rayleigh-quotient loss tolerance relative to the largest eigenvalue. **Domain:** $\varepsilon>0$.

$\lambda_1(A)-\widehat v^{\mathsf T}A\widehat v\le\varepsilon\lambda_1(A)$

$d_0$: Sufficient dimension threshold for the gap-free leading-eigenvalue lower bound of BH **Domain:** The quantity $d_0\in\mathbb N$ is a fixed universal constant.

$d\ge d_0$

$A$: A hidden nonzero real symmetric PSD matrix. **Domain:** $\mathbb R^{d\times d}$.

$\lambda_i(A)$: Eigenvalues of a real symmetric or Hermitian matrix in nonincreasing order. **Domain:** $1\le i\le d$.

$\lambda_1(A)\ge\cdots\ge\lambda_d(A)$

$\widehat v$: Unit vector returned by the algorithm **Domain:** $\mathbb R^d$.

$\|\widehat v\|_2=1$

$\ell(\widehat v)$: Rayleigh loss relative to the largest eigenvalue. **Domain:** A nonnegative real.

$\ell(\widehat v)=(\lambda_1(A)-\widehat v^{\mathsf T}A\widehat v)/\lambda_1(A)$

$\|z\|_2$: Euclidean norm of a vector **Domain:** Finite-dimensional real or complex vector.

$\|z\|_2=(\sum_i|z_i|^2)^{1/2}$

$\|M\|_{\mathrm{op}}$: The matrix operator norm induced by the Euclidean norm. **Domain:** Any compatible matrix.

$\|M\|_{\mathrm{op}}=\max_{\|z\|_2=1}\|Mz\|_2=\sigma_1(M)$

$c,C$: Positive universal constants in the corresponding bound. Identically named constants in different theorems need not have the same value. **Domain:** Independent of the dimension, accuracy, and probability parameters tracked by this bound.

$\log$: Natural logarithm **Domain:** Positive real argument.

$\log x=\ln x$

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

$N,N_{\mathrm r}$: Single-vector query budget for exact right products Av. A block is charged by its column count. **Domain:** $\mathbb N_0$.

$N=N_{\mathrm r}$

$N^\star$: Minimum worst-case query budget attaining this profile's success guarantee **Domain:** $\mathbb N_0\cup\{+\infty\}$.

The quantity is $N^\star=\inf_{\mathcal A}\sup_{I,\omega}N_{\mathcal A}(I,\omega)$, where the infimum ranges over admissible algorithms satisfying this profile's success guarantee.

$\mathcal A,I,\omega$: The algorithm, fixed admissible input, and private algorithmic seed. **Domain:** Quantifiers for worst-case input and execution cost. Success probability is taken over ω.

$\varepsilon_0$: Sufficient small-error threshold in the BH gap-free leading-eigenvalue lower bound. **Domain:** Fixed universal positive constant.

$s$: Order of the hard BH subblock **Domain:** Auxiliary integer in the proof.

$s\asymp\min\{d,c/\sqrt\varepsilon\}$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon;d)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - Sufficiently small error and finite-dimensional regime

**Region.** Require $d\ge d_0$ and $0<\varepsilon\le\varepsilon_0$. The quantities $d_0$ and $\varepsilon_0$ are the universal dimension and accuracy constants sufficient for the source result.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(\min\{d,\varepsilon^{-1/2}\})
$$

**Upper bound.** B1, B3

$$
O(\min\{d,\varepsilon^{-1/2}\log(2d/\varepsilon)\})
$$

**Gap or comparison.** $O(\log(2d/\varepsilon))$

**Comparison argument.** Only this envelope is certified. Simchowitz and Bakshi–Narayanan provide finer log-dimension dependence in specific rank-one spectral windows; it is not transferred universally.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Only exact Av is available, for arbitrary real d-dimensional vectors. Each vector costs one N_right call. Every response comes from the same fixed nonzero PSD matrix.

**Guarantee mapping.** Every fixed nonzero PSD input has success probability at least $2/3$, over the private seed only. The reconstruction baseline is deterministic.

**Output mapping.** Return a unit vector v_hat satisfying (λ_max − v_hatᵀ A v_hat)/λ_max ≤ ε. The target is not replaced by angular error or a prescribed-gap objective.

**Resource mapping.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

### B1 - Upper bound for Lanczos with random initialization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le C\varepsilon^{-1/2}\log(2d/\varepsilon)
$$

**Sources.** [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.**

$$
C\varepsilon^{-1/2}\log(2d/\varepsilon)
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf) theorem: Table 1 and Introduction; section: §1; pdf pages: 1; 2

The registered Lanczos upper bound is O(epsilon^(−1/2) log d). The source cites Kuczynski–Wozniakowski and Musco–Musco.

### B2 - General randomized adaptive-query lower bound from a Wishart-eigenvalue hard family

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c\min\{d,\varepsilon^{-1/2}\}
$$

**Sources.** [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge c\min\{d,\varepsilon^{-1/2}\}
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** Choose $s\approx\min\{d,c/\sqrt{\varepsilon}\}$. A constant number of repetitions and one Rayleigh evaluation per output normalize the success probability.

**Source location.** [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf) theorem: Theorem 2; Corollary 4; section: §2.1; pdf pages: 5; 6

The lower bound covers arbitrary randomized adaptive matrix–vector queries on hard matrices of size s ≤ d at accuracy 1/(20s²). Fixed success probabilities can be converted at constant cost by independent repetition, followed by Rayleigh-value queries and selection of the best candidate.

### B3 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** d

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** Standard-basis queries reveal every matrix column.

**Local argument.** A1

## 5. Local arguments

### A1 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Recover the $d$ columns of $A$ using standard basis queries. Exact internal eigendecomposition returns a unit vector for its largest eigenvalue, giving zero relative Rayleigh loss. No positive spectral gap is needed.

## References

[1] Mark Braverman; Elad Hazan; Max Simchowitz; Blake Woodworth. The Gradient Complexity of Linear Regression. 2020. COLT 2020 PMLR 125 PDF, 21 pages.

https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf
