# Leading eigenvectors with a relative spectral gap: angular error.

**Setting ID.** `MX_S_eigen_gap_angle`

Matrix computation

Output a unit vector approximating the leading eigenspace of $A$.

**Status.** Bounds missing

**TASK tags.** task family: Matrix computation

**MODEL tags.** spectral structure: Explicit matrix class; spectral structure: Psd relative gap

**ORACLE tags.** feedback quality: Exact; interface family: Exact right matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Unit vector

**METRIC tags.** criterion: Principal angle error

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** measure: N right

## 1. Setting specification

### Task

Output a unit vector approximating the leading eigenspace of $A$.

### Admissible model

Assume $A=A^{\mathsf T}\succeq0$, $A\in\mathbb{R}^{d\times d}$, $0<\lambda_1(A)\le\Lambda$, $\lambda_1(A)-\lambda_2(A)\ge\gamma\lambda_1(A)$, and $0<\gamma\le1$. If $d=1$, use the convention $\lambda_2=0$. The leading eigendirection is unique.

### Oracle interface

The information $d,\gamma,\Lambda,\varepsilon,\delta$ is public. The matrix $A$ and its eigenvectors are hidden. Query $v\in\mathbb{R}^d$ returns exact $Av$; the actual largest eigenvalue is not additionally disclosed.

### Output

Return any unit vector $\widehat v\in\mathbb R^d$, without a certificate.

### Loss or accuracy criterion

Let $u_1$ be any unit basis of the true leading eigenspace. The base loss is $1-|u_1^{\mathsf T}\widehat{v}|^2$, with success threshold $\varepsilon^2$; sign changes do not affect the loss.

### Resource accounting

Count right products with single vectors only: $N=N_{\mathrm r}$. A block of width $q$ costs $q$ calls.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using public inputs only. For every admissible input fixed before generation of the private seed, success probability over private randomness is at least $1-\delta$.

**Budget convention.** fixed worst-case joint budget; no expectation substituted

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$\Lambda$: Public upper bound on the largest eigenvalue **Domain:** $\Lambda>0$.

$0<\lambda_1(A)\le\Lambda$

$\gamma$: A public lower bound on the relative leading spectral gap. **Domain:** $0<\gamma\le1$.

$\lambda_1(A)-\lambda_2(A)\ge\gamma\lambda_1(A)$

$\varepsilon$: Tolerance for the sine of the angle between the output direction and the true leading eigendirection. **Domain:** $\varepsilon>0$.

$1-|u_1^{\mathsf T}\widehat v|^2\le\varepsilon^2$

$\delta$: Allowed failure probability for each fixed admissible input **Domain:** $0<\delta<1/2$.

Success probability is at least $1-\delta$.

$A$: A hidden nonzero real symmetric PSD matrix. **Domain:** $\mathbb R^{d\times d}$.

$\lambda_i(A)$: Eigenvalues of a real symmetric or Hermitian matrix in nonincreasing order. **Domain:** $1\le i\le d$.

$\lambda_1(A)\ge\cdots\ge\lambda_d(A)$

$u_1$: A unit representative of the true leading eigendirection; either sign is admissible. **Domain:** $\mathbb R^d$.

$Au_1=\lambda_1(A)u_1,\quad\|u_1\|_2=1$

$\widehat v$: The unit direction returned by the algorithm. **Domain:** $\mathbb R^d$.

$\|\widehat v\|_2=1$

$D_0(\gamma)$: Sufficient dimension threshold for the SER18 hard construction at fixed failure probability **Domain:** Fixed polynomial threshold in $\gamma^{-1}$; source constants are not assigned numerical values.

$g_0$: Standard Gaussian initial vector used in the upper-bound proof **Domain:** $\mathbb R^d$.

$g_0\sim\mathcal N(0,I_d)$

$P_t$: A Chebyshev polynomial of degree at most t that separates the leading eigenvalue in the upper-bound proof. **Domain:** Used only to prove existence of a suitable vector in the Krylov space.

$P_t(\lambda_1)=1,\quad\max_{z\in[0,\lambda_2]}|P_t(z)|\le2e^{-ct\sqrt\gamma}$

$h,s,\lambda$: The original gap, spectral scale, and rank-one spike strength in the SER18 lower-bound conversion. **Domain:** Auxiliary proof quantity.

$h=7\gamma,\quad s=2/(1-h)=\lambda+\lambda^{-1},\quad\lambda>1$

$M,W,u_0$: The SER18 hard matrix, normalized Gaussian symmetric noise, and hidden unit direction. **Domain:** Auxiliary proof object.

$M=W+\lambda u_0u_0^{\mathsf T},\quad\|u_0\|_2=1$

$B$: Positive-definite matrix obtained by shifting the source hard matrix in the lower-bound reduction. **Domain:** $\mathbb R^{d\times d}$.

$B=M+2sI_d$

$|M|$: Absolute value of the symmetric matrix M **Domain:** A real symmetric PSD matrix.

$|M|=(M^2)^{1/2}$

$I_d$: d-dimensional identity matrix **Domain:** $\mathbb R^{d\times d}$.

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

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon,\delta;d,\gamma,\Lambda)
$$

**Scope.** Choose one algorithm, then require the relevant error guarantee for every fixed input in the complete specification. Cost is a worst-case hard budget.

**Optimization direction.** minimize

### R1 - General upper-bound regime in the spectral gap and angle

**Region.** $d\ge2$, $0<\gamma\le1$, $0<\varepsilon<1$, $0<\delta<1/2$, $\Lambda>0$.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O\!\left(\min\{d,1+\gamma^{-1/2}\log(Cd/(\delta\varepsilon\gamma))\}\right)
$$

**Comparison argument.** An upper bound is verified on the general (epsilon,delta,gamma,d) domain. The lower bound applies only in the specific window listed next.

### R2 - The matching strip relating angular accuracy to the spectral gap.

**Region.** Assume $0<\gamma\le1/14$, $\delta=1/10$, $\gamma^2\le\varepsilon^2\le\gamma/12$, and $d\ge\max\{D_0(\gamma),\gamma^{-2}\}$. The quantity $D_0$ is the sufficient polynomial dimension threshold in SER18.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(\gamma^{-1/2}\log d)
$$

**Upper bound.** B1

$$
O(\gamma^{-1/2}\log d)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** In this window, error is tied to the eigengap and dimension exceeds the original theorem threshold. This row does not establish optimality at arbitrary accuracy.

## 4. Bounds and supporting evidence

### B1 - Random-start Lanczos with Chebyshev-filter analysis, or deterministic reconstruction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le C\min\left\{d,\,1+\gamma^{-1/2}\log\frac{Cd}{\delta\varepsilon\gamma}\right\}
$$

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

**Derivation.** Draw the initial vector $g_0\sim\mathcal N(0,I_d)$. With probability at least $1-\delta$, both $|u_1^{\mathsf T}g_0|\ge c\delta$ and $\|g_0\|_2\le C\sqrt{d/\delta}$ hold. Choose a scaled Chebyshev polynomial $P_t$ of degree at most $t$ such that $P_t(\lambda_1)=1$ and $\max_{x\in[0,\lambda_2]}|P_t(x)|\le2\exp(-ct\sqrt\gamma)$; if $\lambda_2=0$, one matrix application suffices. The vector $P_t(A)g_0$ lies in the Krylov subspace, and the sine of its angle to $u_1$ is at most $C\sqrt d\,\delta^{-3/2}\exp(-ct\sqrt\gamma)$. The unit vector maximizing the Rayleigh quotient in that subspace has no greater Rayleigh loss. By $\lambda_1-\lambda_2\ge\gamma\lambda_1$, dividing the normalized Rayleigh loss by $\gamma$ bounds the squared sine error. Thus $t=O\!\bigl(\gamma^{-1/2}\log(Cd/(\delta\varepsilon\gamma))\bigr)$ suffices. The unknown values $\lambda_1,\lambda_2$ are used only to prove the existence of the polynomial; the algorithm need not know them. The projected matrix is formed from the queried Krylov vectors. Alternatively, $d$ standard-basis queries reconstruct the matrix exactly.

**Local argument.** A1

### B2 - Randomly rotated spiked-Wigner hard instances, affinely transformed to positive semidefinite matrices.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c\gamma^{-1/2}\log d
$$

**Sources.** [1](https://arxiv.org/abs/1804.01221)

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

**Derivation.** Use the rank-one hard instance from Theorem 2.2 of Simchowitz, El Alaoui, and Recht (2018). Set its asymptotic relative gap to $h=7\gamma\le1/2$ and choose $\lambda>1$ so that $s=\lambda+\lambda^{-1}=2/(1-h)$. The source matrix is $M=W+\lambda u_0u_0^{\mathsf T}$, where $W$ is its normalized Gaussian symmetric noise matrix and $u_0$ is the hidden unit vector. On the source event $E_{\mathrm{good}}(1/2)$, we have $\lambda_1(M)\le3s/2$ and $\lambda_1(M)-\|W\|_{\mathrm{op}}\ge(s-2)/2=hs/2$, hence $\|W\|_{\mathrm{op}}\le s+1$. Setting $B=M+2sI_d$ gives $B\succ0$, $\lambda_1(B)\le7s/2$, and relative leading-eigenvalue gap at least $h/7=\gamma$. Then $A=(2\Lambda/(7s))B$ ensures $\lambda_1(A)\le\Lambda$. The matrices $A$ and $M$ have the same leading eigenvector; each $A$ product is simulated by exactly one $M$ query and public linear operations. If the squared sine error is at most $\varepsilon^2\le h/12$, the output has Rayleigh quotient for $|M|=(M^2)^{1/2}$ at least $(1-h/12)\|M\|_{\mathrm{op}}$, meeting the source theorem's target. The theorem therefore excludes unrestricted randomized adaptive algorithms using fewer than $ch^{-1/2}\log d$ queries. The sufficient dimension threshold $D_0(\gamma)$ retains the polynomial conditions in Proposition 2.1 and Theorem 6.1 and the condition making the failure bound a constant; unspecified constants remain unspecified. In the region $\delta=1/10$, $\gamma^2\le\varepsilon^2\le\gamma/12$, and $d\ge\max\{D_0(\gamma),\gamma^{-2}\}$, all additional upper-bound logarithms are controlled by $\log d$, giving $\Theta(\gamma^{-1/2}\log d)$.

**Source location.** [1](https://arxiv.org/abs/1804.01221) theorem: Theorem 2.2; Proposition 2.1; Theorem 6.1

Use the rank-one hard instance from Theorem 2.2 of Simchowitz, El Alaoui, and Recht (2018). Set its asymptotic relative gap to $h=7\gamma\le1/2$ and choose $\lambda>1$ so that $s=\lambda+\lambda^{-1}=2/(1-h)$. The source matrix is $M=W+\lambda uu^{\mathsf T}$, where $W$ is its normalized Gaussian symmetric noise matrix and $u$ is the hidden unit vector. On the source event $E_{\mathrm{good}}(1/2)$, we have $\lambda_1(M)\le3s/2$ and $\lambda_1(M)-\|W\|_{\mathrm{op}}\ge(s-2)/2=hs/2$, hence $\|W\|_{\mathrm{op}}\le s+1$. Setting $B=M+2sI_d$ gives $B\succ0$, $\lambda_1(B)\le7s/2$, and relative leading-eigenvalue gap at least $h/7=\gamma$. Then $A=(2\Lambda/(7s))B$ ensures $\lambda_1(A)\le\Lambda$. The matrices $A$ and $M$ have the same leading eigenvector; each $A$ product is simulated by exactly one $M$ query and public linear operations. If the squared sine error is at most $\varepsilon^2\le h/12$, the output has Rayleigh quotient for $|M|=(M^2)^{1/2}$ at least $(1-h/12)\|M\|_{\mathrm{op}}$, meeting the source theorem's target. The theorem therefore excludes unrestricted randomized adaptive algorithms using fewer than $ch^{-1/2}\log d$ queries. The sufficient dimension threshold $D_0(\gamma)$ retains the polynomial conditions in Proposition 2.1 and Theorem 6.1 and the condition making the failure bound a constant; unspecified constants remain unspecified. In the region $\delta=1/10$, $\gamma^2\le\varepsilon^2\le\gamma/12$, and $d\ge\max\{D_0(\gamma),\gamma^{-2}\}$, all additional upper-bound logarithms are controlled by $\log d$, giving $\Theta(\gamma^{-1/2}\log d)$.

## 5. Local arguments

### A1 - Random-start Lanczos with Chebyshev-filter analysis, or deterministic reconstruction

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Draw the initial vector $g_0\sim\mathcal N(0,I_d)$. With probability at least $1-\delta$, both $|u_1^{\mathsf T}g_0|\ge c\delta$ and $\|g_0\|_2\le C\sqrt{d/\delta}$ hold. Choose a scaled Chebyshev polynomial $P_t$ of degree at most $t$ such that $P_t(\lambda_1)=1$ and $\max_{x\in[0,\lambda_2]}|P_t(x)|\le2\exp(-ct\sqrt\gamma)$; if $\lambda_2=0$, one matrix application suffices. The vector $P_t(A)g_0$ lies in the Krylov subspace, and the sine of its angle to $u_1$ is at most $C\sqrt d\,\delta^{-3/2}\exp(-ct\sqrt\gamma)$. The unit vector maximizing the Rayleigh quotient in that subspace has no greater Rayleigh loss. By $\lambda_1-\lambda_2\ge\gamma\lambda_1$, dividing the normalized Rayleigh loss by $\gamma$ bounds the squared sine error. Thus $t=O\!\bigl(\gamma^{-1/2}\log(Cd/(\delta\varepsilon\gamma))\bigr)$ suffices. The unknown values $\lambda_1,\lambda_2$ are used only to prove the existence of the polynomial; the algorithm need not know them. The projected matrix is formed from the queried Krylov vectors. Alternatively, $d$ standard-basis queries reconstruct the matrix exactly.

## References

[1] Max Simchowitz; Ahmed El Alaoui; Benjamin Recht. Tight Query Complexity Lower Bounds for PCA via Finite Sample Deformed Wigner Law. 2018. arXiv PDF retrieved 2026-11-02.

https://arxiv.org/abs/1804.01221
