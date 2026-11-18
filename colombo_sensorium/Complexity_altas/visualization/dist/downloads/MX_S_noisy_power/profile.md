# Perturbed block multiplication: the fixed Noisy Power Method

**Setting ID.** `MX_S_noisy_power`

Matrix computation

The fixed Noisy Power Method returns a subspace of width $b_{\mathrm{blk}}$ that approximately contains the true leading $k$-dimensional singular subspace.

**Status.** Bounds missing

**TASK tags.** task family: Matrix computation

**MODEL tags.** spectral structure: Explicit matrix class; spectral structure: Symmetric singular gap

**ORACLE tags.** feedback quality: Bounded adversarial; interface family: Causal bounded block noise; operation: Noisy block matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol

**OUTPUT tags.** certificate: No additional output certificate required; object: Orthonormal block

**METRIC tags.** criterion: Subspace containment error

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** accounting: Joint coordinates retained; measure: N block; measure: N vec

## 1. Setting specification

### Task

The fixed Noisy Power Method returns a subspace of width $b_{\mathrm{blk}}$ that approximately contains the true leading $k$-dimensional singular subspace.

### Admissible model

Assume $A=A^{\mathsf T}\in\mathbb{R}^{d\times d}$, $\sigma_1(A)\le\Lambda$, and $\sigma_k(A)-\sigma_{k+1}(A)\ge g>0$. Let $U\in\mathbb{R}^{d\times k}$ be an orthonormal basis for the leading singular subspace, with $1\le k\le b_{\mathrm{blk}}\le d$; append zero singular values at the end when needed.

### Oracle interface

Inputs $d,k,b_{\mathrm{blk}},\Lambda,g,\nu_{\mathrm{tot}},\nu_{\parallel},\varepsilon,\delta$ are public and $A,U$ is hidden. For a block $X\in\mathbb{R}^{d\times b_{\mathrm{blk}}}$ with orthonormal columns, the response is $AX+G$. The oracle may choose $G$ from the history, but $\|G\|_{\mathrm{op}}\le\nu_{\mathrm{tot}}$ and $\|U^{\mathsf T}G\|_{\mathrm{op}}\le\nu_{\parallel}$ must hold on every realization at every step.

### Output

Return the fixed algorithm’s final orthogonal block $X_L$ with $b_{\mathrm{blk}}$ columns. Compression to rank k is not required.

### Loss or accuracy criterion

The base error is $\|(I-X_LX_L^{\mathsf T})U\|_{\mathrm{op}}$, with success threshold $\varepsilon$. It measures how well the output subspace contains the true target subspace.

### Resource accounting

Retain joint resources $(N_{\mathrm{block}},N_{\mathrm{vec}})$. A block call of width $b_{\mathrm{blk}}$ increments the first coordinate by one and the second by $b_{\mathrm{blk}}$, giving $N_{\mathrm{block}}=L$ and $N_{\mathrm{vec}}=b_{\mathrm{blk}}L$.

The second term converts block products to per-column cost. The actual interface remains an orthogonal block product with a joint perturbation constraint. Public parameters determine the iteration count in advance; orthogonalization, storage, and internal arithmetic are free.

### Algorithm views and success guarantees

Use the fixed Noisy Power Method with random orthonormal initialization and update $X_{\ell}=\operatorname{orth}(AX_{\ell-1}+G_{\ell})$. Orthogonalization is exact internal computation. The upper bound evaluates this algorithm, not an infimum over all algorithms.

For every admissible matrix and every causal perturbation rule satisfying the per-step norm bounds, probability is over random initialization alone. The error criterion holds with probability at least $1-\delta$. Public parameters determine the iteration count in advance.

**Budget convention.** fixed worst-case joint budget; no expectation substituted

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$k$: Dimension of the leading singular subspace to be contained **Domain:** $k\in\mathbb N,\ 1\le k\le b_{\mathrm{blk}}$.

$U\in\mathbb R^{d\times k},\ U^{\mathsf T}U=I_k$

$b_{\mathrm{blk}}$: The orthogonal-block width in every query and the final output. **Domain:** $b_{\mathrm{blk}}\in\mathbb N,\ k\le b_{\mathrm{blk}}\le d$.

$X_\ell\in\mathbb R^{d\times b_{\mathrm{blk}}}$

$\Lambda$: The public spectral-norm bound. **Domain:** $\Lambda>0$.

$\sigma_1(A)\le\Lambda$

$g$: A lower bound on the absolute singular-value gap at the target boundary. **Domain:** $0<g\le\Lambda$.

$\sigma_k(A)-\sigma_{k+1}(A)\ge g$

$\nu_{\mathrm{tot}}$: Spectral-norm bound on the complete perturbation block at each step **Domain:** $\nu_{\mathrm{tot}}\ge0$.

$\|G_\ell\|_{\rm op}\le\nu_{\mathrm{tot}}$

$\nu_\parallel$: A spectral-norm bound on each perturbation’s projection onto the true target subspace. **Domain:** $\nu_\parallel\ge0$.

$\|U^{\mathsf T}G_\ell\|_{\rm op}\le\nu_\parallel$

$\varepsilon$: Operator-norm tolerance for the portion of the target subspace outside the output space. **Domain:** $\varepsilon>0$.

$\|(I_d-X_LX_L^{\mathsf T})U\|_{\rm op}\le\varepsilon$

$\delta$: Allowed failure probability for each fixed admissible input **Domain:** $0<\delta<1/2$.

Success probability is at least $1-\delta$.

$A$: The hidden real symmetric input matrix. **Domain:** $\mathbb R^{d\times d}$.

$\sigma_i(A)$: Input singular values in nonincreasing order, padded with zeros at the end. **Domain:** $1\le i\le d+1$.

$\sigma_1(A)\ge\cdots\ge\sigma_d(A)\ge\sigma_{d+1}(A)=0$

$U$: An orthonormal basis for the true leading k-dimensional singular subspace. **Domain:** $\mathbb R^{d\times k}$.

$U^{\mathsf T}U=I_k$

$X_\ell$: Orthonormal column block retained at step $\ell$ **Domain:** $\mathbb R^{d\times b_{\rm blk}}$.

$X_\ell^{\mathsf T}X_\ell=I_{b_{\rm blk}}$

$G_\ell$: Additive error block at step $\ell$, generated by the causal disturbance rule **Domain:** $\mathbb R^{d\times b_{\rm blk}}$.

$\operatorname{orth}$: Specified exact orthogonalization of a given column space. **Domain:** Used by the fixed Noisy Power Method.

$L$: Number of iterations determined by public parameters **Domain:** $\mathbb N_0$.

$\tau$: A tunable parameter in the random orthogonal-initialization tail bound. **Domain:** $\tau>1$.

$c_0,c_1$: Two universal positive constants in the random-initialization tail bound **Domain:** A fixed constant.

$\tau^{-c_0(b_{\rm blk}+1-k)}+e^{-c_1d}$

$N_{\mathrm{block}}$: The total native block-interface calls in the algorithm. **Domain:** $\mathbb N_0$.

$N_{\rm block}=L$

$N_{\mathrm{vec}}$: Cost coordinate that charges each block query by its number of columns **Domain:** This cost coordinate does not grant a separate single-column query interface.

$N_{\rm vec}=b_{\rm blk}N_{\rm block}$

$I_j$: Identity matrix of order $j$ **Domain:** $\mathbb R^{j\times j}$.

$\|z\|_2$: Euclidean norm of a vector **Domain:** Finite-dimensional real or complex vector.

$\|z\|_2=(\sum_i|z_i|^2)^{1/2}$

$\|M\|_{\mathrm{op}}$: The matrix operator norm induced by the Euclidean norm. **Domain:** Any compatible matrix.

$\|M\|_{\mathrm{op}}=\max_{\|z\|_2=1}\|Mz\|_2=\sigma_1(M)$

$c,C$: Positive universal constants in the corresponding bound. Identically named constants in different theorems need not have the same value. **Domain:** Independent of the dimension, accuracy, and probability parameters tracked by this bound.

$\log$: Natural logarithm **Domain:** Positive real argument.

$\log x=\ln x$

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.**

$$
\Pr(\|(I_d-X_LX_L^{\mathsf T})U\|_{\rm op}\le\varepsilon)\ge1-\delta
$$

**Resource contract.** vector: N_block; N_vec; projection: N_vec=b_blk*N_block. N_vec charges each column in a block call, while information access is still defined by the orthogonal-block oracle.

Subspace-containment error and joint-call guarantee for the fixed noisy power method. There is no minimization over all algorithms and no additional weighting of the resource vector.

### R1 - The perturbation threshold and initialization-confidence window.

**Region.** Choose $\tau>1$ so that $\tau^{-c_0(b_{\mathrm{blk}}+1-k)}+e^{-c_1d}\le\delta$. Require $0<\varepsilon<1/2$, $5\nu_{\mathrm{tot}}\le\varepsilon g$, and $5\nu_{\parallel}\le g(\sqrt{b_{\mathrm{blk}}}-\sqrt{k-1})/(\tau\sqrt d)$, where $c_0,c_1>0$ is the source universal constant.

**Quantity.** Q1

**Resource.** $N_{\mathrm{vec}}=b_{\mathrm{blk}}N_{\mathrm{block}}$

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
N_{\mathrm{block}}\le C\frac{\Lambda}{g}\log\frac{d\tau}{\varepsilon},\qquad N_{\mathrm{vec}}=b_{\mathrm{blk}}N_{\mathrm{block}}
$$

**Comparison argument.** An attainable call upper bound for a fixed algorithm. Minimum algorithmic complexity is not defined, so a missing lower bound is not a general minimax gap.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** The total-perturbation and U-projected-perturbation bounds hold jointly at every step. Neither independence nor zero means are used.

**Resource mapping.** L block calls of width b_blk cost b_blk L column queries.

### B1 - Fixed Noisy Power Method with randomized initialization and causal bounded perturbations.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N_{\mathrm{block}}\le C\frac{\Lambda}{g}\log\frac{d\tau}{\varepsilon},\qquad N_{\mathrm{vec}}=b_{\mathrm{blk}}N_{\mathrm{block}}
$$

**Sources.** [1](https://www.cs.utexas.edu/~ecprice/papers/npm.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N block.**

$$
O((\Lambda/g)\log(d\tau/\varepsilon))
$$

**N vec.** b_blk*N_block

**Constants.** The iteration constant C and initialization-tail constants c_0 and c_1 are universal constants from the source theorem.

**Source location.** [1](https://www.cs.utexas.edu/~ecprice/papers/npm.pdf) pdf pages: 1; 2; 3; theorem or section: Noisy Power Method; Corollary 1.1; theorem: Noisy Power Method; Corollary 1.1

## References

[1] Moritz Hardt; Eric Price. The Noisy Power Method: A Meta Algorithm with Applications. 2014. author manuscript dated November11,2014.

https://www.cs.utexas.edu/~ecprice/papers/npm.pdf
