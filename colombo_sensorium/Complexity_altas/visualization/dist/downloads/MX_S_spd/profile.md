# Symmetric positive-definite linear systems with normalized energy error.

**Setting ID.** `MX_S_spd`

Matrix computation

Solve $Ax=b$, whose unique solution is $x^\star=A^{-1}b$.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Linear system; solution concept: Solution energy error; task family: Matrix computation

**MODEL tags.** spectral structure: Positive definite; spectral structure: Real spd

**ORACLE tags.** feedback quality: Exact; interface family: Exact right matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Vector

**METRIC tags.** criterion: Linear system energy error

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N right

## 1. Setting specification

### Task

Solve $Ax=b$, whose unique solution is $x^\star=A^{-1}b$.

### Admissible model

The matrix $A\in\mathbb{R}^{d\times d}$ is symmetric positive definite, $d\ge1$, and its spectral condition number is $\lambda_{\max}(A)/\lambda_{\min}(A)\le\kappa$, where $\kappa\ge1$. No absolute spectral scale, sparsity, or preconditioner is promised.

### Oracle interface

Inputs $d,\kappa,\varepsilon,b,x_0$ are public, with $b,x_0\in\mathbb{R}^d$; $A$ is hidden. Any $v\in\mathbb{R}^d$ may be queried for exact $Av$. All responses use one fixed matrix; repetitions are not independent samples.

Entries, inverse actions, shifted solves, and the complete matrix are not free interfaces.

### Output

Return any $\widehat x\in\mathbb R^d$, including an unqueried point or any postprocessing of the transcript. No additional error certificate is required.

### Loss or accuracy criterion

The energy norm is $\|z\|_A^2=z^{\mathsf T}Az$. If $x_0\ne x^\star$, the base loss is $\ell(\widehat{x})=\|\widehat{x}-x^\star\|_A^2/(\|A\|_{\mathrm{op}}\|x_0-x^\star\|_2^2)$ and must satisfy $\ell\le\varepsilon$.

If $x_0=x^\star$, success requires $\widehat x=x^\star$. The criterion is neither relative initial energy error nor relative residual.

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

$\kappa$: Public upper bound on the spectral condition number of the positive definite input matrix **Domain:** $\kappa\ge1$.

$\lambda_{\max}(A)/\lambda_{\min}(A)\le\kappa$

$\varepsilon$: Energy-error tolerance normalized by the spectral norm times the squared initial Euclidean error. **Domain:** $\varepsilon>0$.

$\|\widehat x-x^\star\|_A^2\le\varepsilon\|A\|_{\rm op}\|x_0-x^\star\|_2^2$

$C_0$: The sufficient-dimension constant in the lower-bound window of FL Theorem 26. **Domain:** The quantity $C_0>0$ is universal and fixed.

$d\ge C_0\sqrt{\kappa}+1$

$A$: Hidden symmetric positive definite input matrix **Domain:** $\mathbb R^{d\times d}$.

$b$: Public right-hand side, possibly zero **Domain:** $\mathbb R^d$.

$x_0$: Public initial point **Domain:** $\mathbb R^d$.

$x^\star$: The unique exact solution. **Domain:** $\mathbb R^d$.

$x^\star=A^{-1}b$

$\widehat x$: The solution vector returned by the algorithm. **Domain:** $\mathbb R^d$.

$\|z\|_A$: Energy norm induced by the input A **Domain:** $z\in\mathbb R^d$.

$\|z\|_A=(z^{\mathsf T}Az)^{1/2}$

$\lambda_{\min}(A),\lambda_{\max}(A)$: Smallest and largest eigenvalues **Domain:** Positive real number.

$\lambda_{\min}(A)=\lambda_d(A),\ \lambda_{\max}(A)=\lambda_1(A)$

$\ell(\widehat x)$: Squared normalized energy error. **Domain:** Nonnegative real number; a zero denominator invokes the exact-solution convention.

$\ell(\widehat x)=\|\widehat x-x^\star\|_A^2/(\|A\|_{\rm op}\|x_0-x^\star\|_2^2)$

$t$: Number of conjugate-gradient iterations **Domain:** $\mathbb N_0$.

$\mu_A,\beta_A$: The actual smallest and largest eigenvalues in the error-conversion proof. **Domain:** Auxiliary proof quantity.

$\mu_A=\lambda_{\min}(A),\quad\beta_A=\|A\|_{\rm op}$

$e_x$: The solution-error vector in the error-conversion proof. **Domain:** $\mathbb R^d$.

$e_x=\widehat x-x^\star$

$\delta_0,\eta_0$: Two auxiliary parameters fixed when instantiating the DEM26 lower bound. **Domain:** A fixed constant.

$\delta_0=\eta_0=1/2$

$\lambda_i(A)$: Eigenvalues of a real symmetric or Hermitian matrix in nonincreasing order. **Domain:** $1\le i\le d$.

$\lambda_1(A)\ge\cdots\ge\lambda_d(A)$

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

$q_{\rm quad}$: Associated quadratic objective equivalent to the current SPD solve. **Domain:** Auxiliary function in the associated reduction.

$q_{\rm quad}(x)=\tfrac12x^{\mathsf T}Ax-b^{\mathsf T}x$

$e_0$: Initial solution-error vector **Domain:** $\mathbb R^d$.

$e_0=x_0-x^\star$

$B_{\rm normal},c_{\rm normal}$: Normal-equation matrix and right-hand side in the least-squares-to-SPD reduction **Domain:** An auxiliary object in the associated reduction.

$B_{\rm normal}=A^{\mathsf T}A,\quad c_{\rm normal}=A^{\mathsf T}b$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon;d,\kappa)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - The established randomized lower-bound window.

**Region.** Assume $\kappa\ge2$, $d\ge C_0\sqrt\kappa+1$, and $0<\varepsilon\le1/(e\kappa)$. The sufficient dimension constant $C_0>0$ is from Theorem 26 of the source; retain this restriction of the hard construction.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(\sqrt\kappa/[\log^2(2+\kappa)\log\log(e^e+\kappa)])
$$

**Upper bound.** B1, B3

$$
O(\min\{d,\sqrt\kappa\log(4/\varepsilon)\})
$$

**Gap or comparison.** $O(\log(4/\varepsilon)\log^2(2+\kappa)\log\log(e^e+\kappa))$

**Comparison argument.** CG and reconstruction upper bounds apply on a wider domain. The cited randomized lower bound requires $d\ge C_0\sqrt\kappa+1$ and $\epsilon\le1/(e\kappa)$ and leaves the displayed logarithmic gap. The 2026 high-accuracy strip is recorded separately.

### R2 - High-accuracy matching window from the 2026 result

**Region.** Assume $\kappa\ge2$, $d\ge C\kappa^{13}$, and $d^{-4}\le\varepsilon\le\kappa^{-2}d^{-2}$. The universal constant $C$ is inherited from the theorem and is not assigned an arbitrary numerical value.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Optimal

**Lower bound.** B4

$$
\Omega(\sqrt\kappa\log d)
$$

**Upper bound.** B1, B3

$$
O(\sqrt\kappa\log d)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** The source accuracy is tied to dimension; a constant-factor match is asserted only in the stated high-accuracy band.

## 4. Bounds and supporting evidence

### B1 - Deterministic conjugate gradient, charged by actual $Av$ calls

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le\lceil C\sqrt{\kappa}\log(4/\varepsilon)\rceil
$$

**Sources.** [4](https://arxiv.org/pdf/1708.07788v2)

**Oracle correspondence.** Only exact Av is available for v ∈ R^d. Each vector costs one N_right call, and a q-column block costs q calls. The vectors b and x0 are public; inversion and preconditioning are not additional interfaces.

**Guarantee conversion.** Success probability is at least 2/3 for each fixed (A,b,x0). The deterministic upper bound satisfies a stronger guarantee. The lower bound constrains general randomized adaptive algorithms only within its stated region.

**Output rule.** Return $\widehat x\in\mathbb R^d$ with $\|\widehat x-x^\star\|_A^2\le\epsilon\|A\|_{\mathrm{op}}\|x_0-x^\star\|_2^2$. Retain this initial point and normalization.

**Resource conversion.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.**

$$
\lceil C\sqrt\kappa\log(4/\varepsilon)\rceil
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** The iteration budget uses only kappa and epsilon; the unknown norm ||A|| need not be accessible to the algorithm. The first query identifies zero initial residual.

**Local argument.** A1

**Source location.** [4](https://arxiv.org/pdf/1708.07788v2) theorem: Theorem 24 proof; section: Appendix B.1; equations: 86; pdf pages: 45; 46

### B2 - Lower bounds for arbitrary randomized adaptive algorithms using Wishart hard families and reductions.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c\sqrt{\kappa}/[\log^2(2+\kappa)\log\log(e^e+\kappa)]
$$

**Sources.** [3](https://jmlr.org/papers/volume26/24-1906/24-1906.pdf) [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf)

**Conditions.** $\varepsilon\le1/(e\kappa)$; set $\ell=1$.

**Dimension conditions.** d≥C0 sqrtκ+1

**Oracle correspondence.** Only exact Av is available for v ∈ R^d. Each vector costs one N_right call, and a q-column block costs q calls. The vectors b and x0 are public; inversion and preconditioning are not additional interfaces.

**Guarantee conversion.** Success probability is at least 2/3 for each fixed (A,b,x0). The deterministic upper bound satisfies a stronger guarantee. The lower bound constrains general randomized adaptive algorithms only within its stated region.

**Output rule.** Return $\widehat x\in\mathbb R^d$ with $\|\widehat x-x^\star\|_A^2\le\epsilon\|A\|_{\mathrm{op}}\|x_0-x^\star\|_2^2$. Retain this initial point and normalization.

**Resource conversion.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
N\ge c\sqrt\kappa/[\log^2(2+\kappa)\log\log(e^e+\kappa)]
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [3](https://jmlr.org/papers/volume26/24-1906/24-1906.pdf) theorem: Theorem 26; Lemma 28; proof of Theorem 26; section: §9; pdf pages: 36; 37

Set the spectral-tail parameter $\ell=1$ to recover the ordinary condition number. Retain construction dimension at least $C\sqrt\kappa$ and the source loss $\|e\|_A^2/(\|A\|\|e_0\|^2)$.

**Source location.** [1](https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf) theorem: Theorem 6; Appendix B; as restated in FL Lemma 28; pdf pages: 7

BH gives an unrestricted randomized linear-system query lower bound with explicit loss $\log^2s\,\log\log s$. FL Lemma 28 and Theorem 26 use this result to obtain the lower bound for the energy-error criterion here.

### B3 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le d
$$

**Oracle correspondence.** Only exact Av is available for v ∈ R^d. Each vector costs one N_right call, and a q-column block costs q calls. The vectors b and x0 are public; inversion and preconditioning are not additional interfaces.

**Guarantee conversion.** Success probability is at least 2/3 for each fixed (A,b,x0). The deterministic upper bound satisfies a stronger guarantee. The lower bound constrains general randomized adaptive algorithms only within its stated region.

**Output rule.** Return $\widehat x\in\mathbb R^d$ with $\|\widehat x-x^\star\|_A^2\le\epsilon\|A\|_{\mathrm{op}}\|x_0-x^\star\|_2^2$. Retain this initial point and normalization.

**Resource conversion.** Count only right multiplication by a single vector, $N=N_{\mathrm r}$. A block product of width $q$ costs $q$ calls. The worst-case cap holds for every input and random seed; it is not an expected call count. Reading public inputs and exact internal arithmetic, storage, and postprocessing are uncharged. This budget does not certify running time or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** d

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** Standard-basis queries reveal every matrix column.

**Local argument.** A2

### B4 - General randomized adaptive queries; randomly rotated spectral families and polynomial-approximation lower bounds

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c\sqrt\kappa\log d
$$

**Sources.** [2](https://proceedings.mlr.press/v336/derezinski26a.html)

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

**Derivation.** Fix the auxiliary parameters in the source Theorem E.2 at $\delta_0=\eta_0=1/2$. Its sufficient dimension condition is $d\ge C\kappa^{13}$, its residual threshold is $1/d$, and its required success probability is $5/6$. Choose the hard-instance initial point $x_0=0$. Let $e_x=\widehat x-x^\star$, $\beta_A=\|A\|_{\mathrm{op}}$, and $\mu_A=\lambda_{\min}(A)$. Then
$$\|Ae_x\|_2^2\le\beta_A\|e_x\|_A^2\le\varepsilon\beta_A^2\|x^\star\|_2^2,\qquad \|b\|_2\ge\mu_A\|x^\star\|_2,$$
so the relative residual on success is at most $\kappa\sqrt\varepsilon$. The condition $\varepsilon\le\kappa^{-2}d^{-2}$ ensures the source residual threshold. Run a $2/3$-success algorithm independently three times, spend one additional $A\widehat x$ query per output, and select the smallest residual. At least one run succeeds with probability $1-(1/3)^3=26/27>5/6$. If the original budget is $N$, the source theorem excludes $3(N+1)<c\sqrt\kappa\log d$, giving $N\ge c'\sqrt\kappa\log d-O(1)$. On the strip $d^{-4}\le\varepsilon\le\kappa^{-2}d^{-2}$, we have $\log(1/\varepsilon)=\Theta(\log d)$, while $d\ge C\kappa^{13}$ ensures that the reconstruction branch does not change the order. Thus deterministic CG and the unrestricted randomized lower bound match up to constants in this strip; this does not establish optimality for every $(d,\kappa,\varepsilon)$.

**Source location.** [2](https://proceedings.mlr.press/v336/derezinski26a.html) theorem: Theorem E.2, PDF p.30

Fix the auxiliary parameters in the source Theorem E.2 at $\delta_0=\eta_0=1/2$. Its sufficient dimension condition is $d\ge C\kappa^{13}$, its residual threshold is $1/d$, and its required success probability is $5/6$. Choose the hard-instance initial point $x_0=0$. Let $e=\widehat x-x^\star$, $\beta=\|A\|_{\mathrm{op}}$, and $\mu=\lambda_{\min}(A)$. Then
$$\|Ae\|_2^2\le\beta\|e\|_A^2\le\varepsilon\beta^2\|x^\star\|_2^2,\qquad \|b\|_2\ge\mu\|x^\star\|_2,$$
so the relative residual on success is at most $\kappa\sqrt\varepsilon$. The condition $\varepsilon\le\kappa^{-2}d^{-2}$ ensures the source residual threshold. Run a $2/3$-success algorithm independently three times, spend one additional $A\widehat x$ query per output, and select the smallest residual. At least one run succeeds with probability $1-(1/3)^3=26/27>5/6$. If the original budget is $N$, the source theorem excludes $3(N+1)<c\sqrt\kappa\log d$, giving $N\ge c'\sqrt\kappa\log d-O(1)$. On the strip $d^{-4}\le\varepsilon\le\kappa^{-2}d^{-2}$, we have $\log(1/\varepsilon)=\Theta(\log d)$, while $d\ge C\kappa^{13}$ ensures that the reconstruction branch does not change the order. Thus deterministic CG and the unrestricted randomized lower bound match up to constants in this strip; this does not establish optimality for every $(d,\kappa,\varepsilon)$.

## 5. Local arguments

### A1 - Deterministic conjugate gradients with actual Av calls charged

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Let $x^\star=A^{-1}b$, $e_0=x_0-x^\star$, and $r_0=b-Ax_0$. One charged product forms $r_0$; if it is zero, return the exact solution $x_0$. Exact conjugate gradients minimizes the $A$-norm error over $x_0+\mathcal K_t(A,r_0)$. For every degree-$t$ polynomial $p$ with $p(0)=1$, this gives
$$\|x_t-x^\star\|_A\le\max_{\lambda\in\operatorname{spec}(A)}|p(\lambda)|\,\|e_0\|_A.$$
A scaled Chebyshev polynomial yields
$$\|x_t-x^\star\|_A^2\le4\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^{2t}\|e_0\|_A^2\le4\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^{2t}\|A\|_{\rm op}\|e_0\|_2^2.$$
Thus $t=O(\sqrt\kappa\log(4/\varepsilon))$ suffices in the nontrivial accuracy region. The initial residual call and the one product per CG iteration are included by increasing the universal constant in the registered ceiling. Actual spectral endpoints are used only to prove the polynomial bound; the algorithm uses the public condition-number bound and tolerance. This argument covers arbitrary public $x_0$, not only $x_0=0$. The Krylov minimum-error property is the cited primary ingredient; the normalization and resource accounting are explicit here.

**Sources.** [4](https://arxiv.org/pdf/1708.07788v2)

### A2 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Query all $d$ standard basis vectors to recover every column of $A$. Exact internal linear algebra returns $A^{-1}b$, giving zero energy error, including the zero-denominator case. The algorithm is deterministic and uses exactly $d$ right products.

## References

[1] Mark Braverman; Elad Hazan; Max Simchowitz; Blake Woodworth. The Gradient Complexity of Linear Regression. 2020. COLT 2020 PMLR 125 PDF, 21 pages.

https://proceedings.mlr.press/v125/braverman20a/braverman20a.pdf

[2] Michał Dereziński; Ethan N. Epperly; Raphael A. Meyer. The matrix-vector complexity of Ax = b. 2026. PMLR proceedings PDF, 34 pages.

https://proceedings.mlr.press/v336/derezinski26a.html

[3] Michal Dereziński; Daniel LeJeune; Deanna Needell; Elizaveta Rebrova. Fine-grained Analysis and Faster Algorithms for Iteratively Solving Linear Systems. 2025. JMLR 26 (2025), published June 2025, 49-page PDF.

https://jmlr.org/papers/volume26/24-1906/24-1906.pdf

[4] Cameron Musco; Christopher Musco; Aaron Sidford. Stability of the Lanczos Method for Matrix Function Approximation. 2018. arXiv:1708.07788v2, revised 2024-11-18; SODA 2018.

https://arxiv.org/pdf/1708.07788v2
