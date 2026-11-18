# Log determinant of a positive definite matrix: absolute error

**Setting ID.** `MX_S_logdet`

Matrix computation

Estimate $\tau=\log\det(A)=\operatorname{tr}(\log A)$, with the matrix logarithm defined by spectral decomposition.

**Status.** Bounds missing

**TASK tags.** formulation: Matrix logdet; solution concept: Additive logdet error; task family: Matrix computation

**MODEL tags.** spectral structure: Positive definite spectrum interval; spectral structure: Positive spectral interval

**ORACLE tags.** feedback quality: Exact; interface family: Exact right matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Scalar

**METRIC tags.** criterion: Absolute logdet error

**GUARANTEE tags.** confidence: Confidence parameter explicitly declared; randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Krylov steps per probe; measure: N right; measure: Probe count

## 1. Setting specification

### Task

Estimate $\tau=\log\det(A)=\operatorname{tr}(\log A)$, with the matrix logarithm defined by spectral decomposition.

### Admissible model

Assume $A=A^{\mathsf T}\succ0$ and $A\in\mathbb{R}^{d\times d}$, with $\mu I\preceq A\preceq\beta I$, $0<\mu\le\beta$, and $\beta/\mu\le\kappa$.

### Oracle interface

The information $d,\mu,\beta,\kappa,\eta,\delta$ is public and $A$ is hidden. Query $v\in\mathbb{R}^d$ returns exact $Av$. Neither $\log(A)v$ nor a shifted inverse action is available for free.

### Output

Return any real $\widehat\tau$. No explicit matrix logarithm, determinant, or verifiable certificate is required.

### Loss or accuracy criterion

The base loss is $|\widehat\tau-\log\det(A)|$, with success threshold $\eta$. Positive eigenvalues ensure that the matrix logarithm and target are finite.

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

$\mu$: Public positive lower bound on eigenvalues **Domain:** $0<\mu\le\beta$.

$\mu I_d\preceq A$

$\beta$: The public eigenvalue upper bound. **Domain:** $\beta\ge\mu>0$.

$A\preceq\beta I_d$

$\kappa$: A bound on the ratio of public spectral endpoints. **Domain:** $\kappa\ge1$.

$\beta/\mu\le\kappa$

$\eta$: The absolute log-determinant error tolerance. **Domain:** $\eta>0$.

$|\widehat\tau-\log\det A|\le\eta$

$\delta$: Allowed failure probability for each fixed admissible input **Domain:** $0<\delta<1/2$.

Success probability is at least $1-\delta$.

$A$: Hidden real symmetric positive definite matrix **Domain:** $\mathbb R^{d\times d}$.

$\log A$: Matrix logarithm defined by spectral decomposition **Domain:** Real symmetric matrix.

$A=U\operatorname{diag}(\lambda_i)U^{\mathsf T}\ \Longrightarrow\ \log A=U\operatorname{diag}(\log\lambda_i)U^{\mathsf T}$

$\tau,\widehat\tau$: True log determinant and algorithmic estimate **Domain:** $\mathbb R$.

$\tau=\log\det(A)=\sum_{i=1}^d\log\lambda_i(A)$

$s_\eta$: Number of Rademacher probes in the same stochastic Lanczos quadrature implementation **Domain:** $\mathbb N$.

$s_\eta=\max\{1,\lceil8\eta^{-2}(d\log^2\kappa+2\eta\log\kappa)\log(2/\delta)\rceil\}$

$t_\eta$: Sufficient upper bound on Lanczos steps per probe. **Domain:** $\mathbb N$.

$t_\eta=\max\{1,\lceil\tfrac{\sqrt{\kappa+1}}4\log[4\eta^{-1}d(\sqrt{\kappa+1}+1)\log(2\kappa)]\rceil\}$

$\mathcal R$: Rademacher probe distribution **Domain:** Each coordinate independently equals +1 or −1 with probability 1/2.

$I_d$: d-dimensional identity matrix **Domain:** $\mathbb R^{d\times d}$.

$\lambda_i(A)$: Eigenvalues of a real symmetric or Hermitian matrix in nonincreasing order. **Domain:** $1\le i\le d$.

$\lambda_1(A)\ge\cdots\ge\lambda_d(A)$

$\|z\|_2$: Euclidean norm of a vector **Domain:** Finite-dimensional real or complex vector.

$\|z\|_2=(\sum_i|z_i|^2)^{1/2}$

$\|M\|_{\mathrm{op}}$: The matrix operator norm induced by the Euclidean norm. **Domain:** Any compatible matrix.

$\|M\|_{\mathrm{op}}=\max_{\|z\|_2=1}\|Mz\|_2=\sigma_1(M)$

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
N^\star(\eta,\delta;d,\mu,\beta,\kappa)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - A positive spectral interval and nontrivial absolute accuracy.

**Region.** Assume $d\ge1$, $\kappa\ge2$, $\mu>0$, $\beta/\mu\le\kappa$, $0<\eta\le d\log\kappa$, and $0<\delta<1/2$, together with model condition $\mu\le\beta$.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1, B2

$$
\min\{d,s_\eta\min(d,t_\eta)\}
$$

**Comparison argument.** Choose one of the two complete upper-bound algorithms. Probe count and Lanczos length cannot be minimized coordinatewise across algorithms.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Only exact Av is available. Products log(A)v, linear solves, and preconditioners are not free interfaces. Each Lanczos iteration consumes one native right-product query.

**Guarantee mapping.** Success probability is at least 1 − δ for each fixed SPD input. Sampling and truncation parameters must use the same verified error allocation.

**Output mapping.** Return a real estimate of logdet(A) with absolute error at most η. Retain the public positive spectral interval [μ,β]; relative log-determinant error is a different target.

**Resource mapping.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

### B1 - Random Rademacher probes with stochastic Lanczos quadrature (SLQ)

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le s_\eta\min\{d,t_\eta\}
$$

**Sources.** [1](https://arxiv.org/pdf/2005.10009v2)

**Conditions.**

$$
s_\eta=\max\{1,\lceil8\eta^{-2}(d\log^2\kappa+2\eta\log\kappa)\log(2/\delta)\rceil\}; t_\eta=\max\{1,\lceil\sqrt{\kappa+1}\log[4\eta^{-1}d(\sqrt{\kappa+1}+1)\log(2\kappa)]/4\rceil\}
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.**

$$
s_eta \min{d,t_eta}
$$

**probe count.**

$$
s_eta
$$

**krylov steps per probe.**

$$
\min{d,t_eta}
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** Each Lanczos step costs one Av product. If the Krylov subspace becomes invariant early, the quadratic form is computed exactly. Replacing the actual condition number kappa(A) by the public upper bound kappa only enlarges the two monotone sufficient budgets. Probe count and step count must arise from the same parameter choice.

**Source location.** [1](https://arxiv.org/pdf/2005.10009v2) theorem: Theorem 20; Lemma 21; section: §4.2; pdf pages: 16; 17

The Rademacher construction avoids the additional Gaussian sample-count restriction in Theorem 19. The sampling bound in Lemma 21 does not depend on the sign of the log determinant.

### B2 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** d

**probe count.** 0

**krylov steps per probe.** 0

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Local argument.** A1

## 5. Local arguments

### A1 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Recover the $d$ columns of $A$ by standard basis queries. Its positive spectrum permits exact internal evaluation of the sum of eigenvalue logarithms. The log-determinant error is zero, regardless of whether the log determinant itself is positive, zero, or negative.

## References

[1] Alice Cortinovis; Daniel Kressner. On randomized trace estimates for indefinite matrices with an application to determinants. 2021. arXiv:2005.10009v2; 2021-05-25; journal DOI 10.1007/s10208-021-09525-9.

https://arxiv.org/pdf/2005.10009v2
