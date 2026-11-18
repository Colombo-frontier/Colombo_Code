# Trace estimation for general symmetric matrices with Schatten-normalized error

**Setting ID.** `MX_S_trace_general`

Matrix computation

Estimate the trace $\tau=\operatorname{tr}(A)$ of a symmetric matrix.

**Status.** Fully optimal

**TASK tags.** formulation: Matrix trace; solution concept: Schatten scaled additive error; task family: Matrix computation

**MODEL tags.** spectral structure: Symmetric indefinite allowed

**ORACLE tags.** feedback quality: Exact; interface family: Exact right matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Scalar

**METRIC tags.** criterion: Schatten normalized trace error

**GUARANTEE tags.** confidence: Confidence parameter explicitly declared; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N right

## 1. Setting specification

### Task

Estimate the trace $\tau=\operatorname{tr}(A)$ of a symmetric matrix.

### Admissible model

Assume $A=A^{\mathsf T}\in\mathbb{R}^{d\times d}$, allowing indefinite or zero matrices; the norm order is $1\le p\le2$.

### Oracle interface

The information $d,p,\varepsilon,\delta$ is public and $A$ is hidden. Query $v\in\mathbb{R}^d$ returns exact $Av$. Repeated adaptive queries are allowed.

### Output

Return a scalar $\widehat\tau\in\mathbb{R}$; no additional certificate is required.

### Loss or accuracy criterion

The success event is $|\widehat\tau-\operatorname{tr}(A)|\le\varepsilon\|A\|_{S_p}$, where $\|A\|_{S_p}=(\sum_i\sigma_i(A)^p)^{1/p}$. When $A=0$, the output must be zero. A general matrix can have zero trace and nonzero norm.

### Resource accounting

Count right products with single vectors only: $N=N_{\mathrm r}$. A block of width $q$ costs $q$ calls.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using public inputs only. For every admissible input fixed before generation of the private seed, success probability over private randomness is at least $1-\delta$.

**Budget convention.** A fixed worst-case budget respected for every input and private seed.

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$p$: The Schatten-norm order used to normalize trace error. **Domain:** $1\le p\le2$.

$\|A\|_{S_p}=(\sum_{i=1}^d\sigma_i(A)^p)^{1/p}$

$\varepsilon$: Absolute trace-estimation error as a fraction of the input Schatten norm **Domain:** $\varepsilon>0$.

$|\widehat\tau-\operatorname{tr}(A)|\le\varepsilon\|A\|_{S_p}$

$\delta$: Allowed failure probability for each fixed admissible input **Domain:** $0<\delta<1/2$.

Success probability is at least $1-\delta$.

$C_0$: Sufficient-dimension constant for the Gaussian hard-instance embedding in DT Theorem 4.2. **Domain:** The quantity $C_0>0$ is universal and fixed.

$d\ge C_0(\sqrt{\log(1/\delta)}/\varepsilon)^p$

$A$: A hidden real symmetric matrix, possibly indefinite or zero. **Domain:** $\mathbb R^{d\times d}$.

$\tau,\widehat\tau$: True trace and output estimate **Domain:** $\mathbb R$.

$\tau=\operatorname{tr}(A)=\sum_{i=1}^d A_{ii}$

$\sigma_i(M)$: Singular values in nonincreasing order **Domain:** $1\le i\le\min\{\operatorname{rows}(M),\operatorname{cols}(M)\}$.

$\sigma_1(M)\ge\cdots\ge\sigma_{\min\{\operatorname{rows}(M),\operatorname{cols}(M)\}}(M)\ge0$

$\|A\|_{S_p}$: Schatten norm that sets the scale of the trace error **Domain:** A nonnegative real.

$\|A\|_{S_p}=(\sum_{i=1}^d\sigma_i(A)^p)^{1/p}$

$c$: Universal constant in the small-accuracy regime of DT, Theorem 4.2 **Domain:** Fixed positive number.

$0<\varepsilon<c[\log(1/\delta)]^{1/2-1/p}$

$C$: The universal multiplier in the upper bound. **Domain:** Fixed positive number.

$\|z\|_2$: Euclidean norm of a vector **Domain:** Finite-dimensional real or complex vector.

$\|z\|_2=(\sum_i|z_i|^2)^{1/2}$

$\log$: Natural logarithm **Domain:** Positive real argument.

$\log x=\ln x$

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
N^\star(\varepsilon,\delta;d,p)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - Regime with matching Schatten-normalized bounds

**Region.** Assume $1\le p\le2$, $0<\delta<1/4$, $0<\varepsilon<c[\log(1/\delta)]^{1/2-1/p}$, and $d\ge C_0(\sqrt{\log(1/\delta)}/\varepsilon)^p$. The quantity $c,C_0>0$ is the universal sufficient constant in the source.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega((\sqrt{\log(1/\delta)}/\varepsilon)^p)
$$

**Upper bound.** B1, B3

$$
O((\sqrt{\log(1/\delta)}/\varepsilon)^p)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** The window ensures that the log(1/δ) term does not dominate. Removing this window would invalidate a claim of full-parameter matching.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Only exact Av is available, with arbitrary randomized adaptive real-vector queries. A is one fixed general real symmetric matrix, and each vector costs one call.

**Guarantee mapping.** For each fixed A, success probability is at least 1 − δ. The lower bound retains its accuracy, confidence, and sufficient-dimension region.

**Output mapping.** Return a real scalar t_hat with error at most epsilon ||A||_{S_p}, for 1<=p<=2. Error is not normalized by the possibly zero trace.

**Resource mapping.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

### B1 - Randomized trace estimation with Schatten-norm error

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le C[(\sqrt{\log(1/\delta)}/\varepsilon)^p+\log(1/\delta)]
$$

**Sources.** [1](https://arxiv.org/pdf/2209.15219v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.**

$$
C[(\sqrt{\log(1/\delta)}/\varepsilon)^p+\log(1/\delta)]
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/2209.15219v1) theorem: Theorem B.1; section: Appendix B; pdf pages: 18

Static Schatten-$p$ Hutch++ upper bound; non-PSD inputs use an additive norm scale.

### B2 - Unrestricted randomized adaptive queries; Gaussian posterior information lower bound.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c(\sqrt{\log(1/\delta)}/\varepsilon)^p
$$

**Sources.** [1](https://arxiv.org/pdf/2209.15219v1)

**Dimension conditions.** $d\ge C_0\bigl(\sqrt{\log(1/\delta)}/\varepsilon\bigr)^p$. The quantity $C_0>0$ is the sufficient dimension constant in the source lower bound.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge c(\sqrt{\log(1/\delta)}/\varepsilon)^p
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/2209.15219v1) theorem: Theorem 4.2; section: §4.2; Appendix C.2; pdf pages: 10; 25

The Wigner posterior trace is Gaussian. Retain the source's choice of $n$ and the check $n\ge\log(1/\delta)$. Zero padding embeds the instance in larger dimensions.

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

Query all $d$ standard basis vectors, fixed before any response if nonadaptivity is required. These responses recover all columns. Summing their diagonal entries returns the exact trace. The argument applies to the stated matrix class, including zero trace, and uses $d$ right queries with deterministic success.

## References

[1] David P. Woodruff; Fred Zhang; Qiuyi (Richard) Zhang. Optimal Query Complexities for Dynamic Trace Estimation. 2022. arXiv:2209.15219v1; 2022-09-30.

https://arxiv.org/pdf/2209.15219v1
