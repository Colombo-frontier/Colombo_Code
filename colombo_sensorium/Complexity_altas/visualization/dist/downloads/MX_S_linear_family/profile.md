# Public linear matrix family with mixed relative and additive error

**Setting ID.** `MX_S_linear_family`

Matrix computation

Approximate the unknown matrix $A$ within the public linear subspace $\mathcal{L}=\operatorname{span}\{B_1,\ldots,B_q\}$.

**Status.** Bounds missing

**TASK tags.** task family: Matrix computation

**MODEL tags.** spectral structure: Explicit matrix class; spectral structure: Public linear matrix family

**ORACLE tags.** feedback quality: Exact; interface family: Exact two sided matvec; operation: Matrix right matvec; operation: Matrix transpose matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Matrix in linear space

**METRIC tags.** criterion: Mixed relative additive error

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** measure: N left; measure: N right

## 1. Setting specification

### Task

Approximate the unknown matrix $A$ within the public linear subspace $\mathcal{L}=\operatorname{span}\{B_1,\ldots,B_q\}$.

### Admissible model

The matrix $A\in\mathbb{R}^{d\times d}$ is arbitrary. The public $B_1,\ldots,B_q$ are linearly independent, with $1\le q\le d^2$. Approximation factor is $\gamma\ge1$ and additive coefficient $\alpha\ge0$.

### Oracle interface

The information $d,q,B_1,\ldots,B_q,\gamma,\alpha,\delta$ is public and $A$ is hidden. Exact $Av$ and $A^{\mathsf T}u$ may be queried at arbitrary vectors. Computation and search over the public basis are uncharged.

### Output

Return $\widehat{B}\in\mathcal{L}$, possibly in basis-coefficient form. No certificate is required.

### Loss or accuracy criterion

Define $\operatorname{OPT}=\min_{B\in\mathcal{L}}\|A-B\|_{\mathrm{F}}$; success requires $\|A-\widehat{B}\|_{\mathrm{F}}\le\gamma\operatorname{OPT}+\alpha\|A\|_{\mathrm{F}}$. The finite-dimensional linear space is closed, so a minimizer exists. If $A=0$, output zero.

### Resource accounting

Retain the joint budget $(N_{\mathrm{r}},N_{\mathrm{l}})$, whose coordinates count single-vector calls to $Av$ and $A^{\mathsf T}u$, respectively. This setting explicitly uses the equal-weight scalarization $N=N_{\mathrm{r}}+N_{\mathrm{l}}$. Each column of a block is charged separately.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using public inputs only. For every admissible input fixed before generation of the private seed, success probability over private randomness is at least $1-\delta$.

**Budget convention.** fixed worst-case joint budget; no expectation substituted

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$q$: Dimension of the public matrix linear space **Domain:** $q\in\mathbb N,\ 1\le q\le d^2$.

$q=\dim\mathcal L$

$\gamma$: Relative coefficient multiplying the optimal residual in the mixed target **Domain:** $\gamma\ge1$.

$\|A-\widehat B\|_F\le\gamma\operatorname{OPT}+\alpha\|A\|_F$

$\alpha$: Additive coefficient multiplying the input Frobenius norm in the mixed objective. **Domain:** $\alpha\ge0$.

$\|A-\widehat B\|_F\le\gamma\operatorname{OPT}+\alpha\|A\|_F$

$\delta$: Allowed failure probability for each fixed input and fixed public linear space **Domain:** $0<\delta<1$.

Success probability is at least $1-\delta$.

$A$: The hidden arbitrary input matrix. **Domain:** $\mathbb R^{d\times d}$.

$B_1,\ldots,B_q$: A public linearly independent matrix basis. **Domain:** $B_i\in\mathbb R^{d\times d}$.

$\mathcal L$: The public q-dimensional linear space of candidate matrices. **Domain:** $\mathcal L\subseteq\mathbb R^{d\times d}$.

$\mathcal L=\operatorname{span}\{B_1,\ldots,B_q\}$

$\widehat B$: Candidate matrix returned by the algorithm **Domain:** $\widehat B\in\mathcal L$.

$\operatorname{OPT}$: The best Frobenius residual in the linear space. **Domain:** A nonnegative real.

$\operatorname{OPT}=\min_{B\in\mathcal L}\|A-B\|_F$

$\eta$: The additional relative factor in the QSL finite-net approximation method. **Domain:** $0<\eta<1$.

$\eta=\gamma-3$

$\widetilde O$: Suppresses the accuracy, confidence, and covering-net logarithms explicitly stated in this upper bound **Domain:** Use only in the upper-bound window $\alpha>0$ and $3<\gamma<4$.

$\|M\|_{\mathrm F}$: The Frobenius norm. **Domain:** An arbitrary real or complex matrix.

$\|M\|_{\mathrm F}=(\sum_{ij}|M_{ij}|^2)^{1/2}=(\sum_i\sigma_i(M)^2)^{1/2}$

$c,C$: Positive universal constants in the corresponding bound. Identically named constants in different theorems need not have the same value. **Domain:** Independent of the dimension, accuracy, and probability parameters tracked by this bound.

$\log$: Natural logarithm **Domain:** Positive real argument.

$\log x=\ln x$

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

$N_{\mathrm r},N_{\mathrm l}$: Single-vector counts for right products Av and transpose products Aᵀu. **Domain:** $\mathbb N_0^2$.

$N$: The worst-case call budget with equal costs for both product channels. **Domain:** $\mathbb N_0$.

$N=N_{\mathrm r}+N_{\mathrm l}$

$N^\star$: Minimum worst-case query budget attaining this profile's success guarantee **Domain:** $\mathbb N_0\cup\{+\infty\}$.

The quantity is $N^\star=\inf_{\mathcal A}\sup_{I,\omega}N_{\mathcal A}(I,\omega)$, where the infimum ranges over admissible algorithms satisfying this profile's success guarantee.

$\mathcal A,I,\omega$: The algorithm, fixed admissible input, and private algorithmic seed. **Domain:** Quantifiers for worst-case input and execution cost. Success probability is taken over ω.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(d,q,\gamma,\alpha,\delta)
$$

**Scope.** The algorithm may use the complete public basis. For fixed d, q, gamma, alpha, and delta, take the worst case over all such public q-dimensional linear spaces and hidden inputs.

**Optimization direction.** minimize

### R1 - Linear-family upper bound with positive additive tolerance

**Region.** Assume $1\le q\le d^2$, $3<\gamma<4$, $0<\alpha<1$, and $0<\delta<1/2$. The pure-relative-error endpoint $\alpha=0$ is outside this upper bound.

**Quantity.** Q1

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1, B2

$$
\min\!\left\{d,\widetilde{O}\!\left(\frac{\sqrt{q\log(1/\alpha)}}{(\gamma-3)^2}\right)\right\}
$$

**Comparison argument.** Use the same two-sided query resources and minimize over complete algorithms. No matching lower bound is verified.

### R2 - Baseline from complete parameter reconstruction of the linear family

**Region.** $1\le q\le d^2$, $\gamma\ge1$, $\alpha\ge0$, $0<\delta<1$.

**Quantity.** Q1

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B2

$$
O(d)
$$

**Comparison argument.** The upper bound covers the full domain, including α = 0. A hard finite-family lower bound is not transferred to an arbitrary q-dimensional linear space.

## 4. Bounds and supporting evidence

### B1 - A covering net for the linear space followed by a finite-family query algorithm, Amsel et al., Corollary 3.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le\widetilde{O}\!\left(\frac{\sqrt{q\log(1/\alpha)}}{(\gamma-3)^2}\right)
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v336/main/assets/amsel26a/amsel26a.pdf)

**Oracle correspondence.** Exact two-sided queries; the public matrix basis and internal calculations using it are free.

**Resource conversion.** Two-sided vector calls; public basis/cover manipulation arithmetic excluded.

**Constants.** Fixed declared regularity and initialization budgets; no unlisted joint-parameter optimality is asserted.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v336/main/assets/amsel26a/amsel26a.pdf) pdf pages: 2; 3; 4; 10; 11; 12; 13; theorem or section: Definition 7; Corollary 3; Theorem 6 and its application to linear families; theorem: Definition 7; Corollary 3; Theorem 6 and its application to linear families

Definition 7 of QSL defines the q-dimensional linear matrix family. Corollary 3 and the covering argument in Theorem 6 give $(3+\eta)\operatorname{OPT}+\alpha\|A\|_F$, with $\eta=\gamma-3$. Both multiplication directions are allowed; public-basis and covering-net computations are uncharged.

### B2 - Deterministic basis reconstruction followed by projection onto the public linear matrix space.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

**Derivation.** After recovering A, use a free Frobenius orthogonal projection to obtain the exact optimal candidate.

**Local argument.** A1

## 5. Local arguments

### A1 - Deterministic basis reconstruction followed by projection onto the public linear matrix space.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Recover all $d$ columns by standard basis queries. Frobenius orthogonal projection onto the public linear span is a finite-dimensional least-squares problem in known coefficients and is uncharged. Its output attains the exact optimum residual, including zero optimum.

## References

[1] Noah Amsel; Pratyush Avi; Tyler Chen; Feyza Duman Keles; Chinmay Hegde; Christopher Musco; Cameron Musco; David Persson. Query Efficient Structured Matrix Learning. 2026. COLT 2026 PMLR 336, pp.158–194.

https://raw.githubusercontent.com/mlresearch/v336/main/assets/amsel26a/amsel26a.pdf
