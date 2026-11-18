# Low-rank approximation: Schatten residual and right projection.

**Setting ID.** `MX_S_lowrank`

Matrix computation

Construct a rank-$k$ orthogonal right projection $P$ approximating the optimal rank-$k$ residual.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Matrix lowrank approximation; solution concept: Relative schatten residual; task family: Matrix computation

**MODEL tags.** spectral structure: Arbitrary real matrix

**ORACLE tags.** feedback quality: Exact; interface family: Exact two sided matvec; operation: Matrix left matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Orthogonal projector

**METRIC tags.** criterion: Relative schatten residual

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N left; measure: N right

## 1. Setting specification

### Task

Construct a rank-$k$ orthogonal right projection $P$ approximating the optimal rank-$k$ residual.

### Admissible model

The matrix $A\in\mathbb{R}^{m\times n}$ is arbitrary real, with $d_{\mathrm{min}}=\min\{m,n\}$, $1\le k<d_{\mathrm{min}}$, and $1\le p\le\infty$. No rank, singular-gap, or spectral-decay promise is imposed.

### Oracle interface

The information $m,n,k,p,\varepsilon$ is public and $A$ is hidden. Exact $Av$ is available for every $v\in\mathbb{R}^n$, and exact $A^{\mathsf T}u$ for every $u\in\mathbb{R}^m$. The two directions are charged separately.

### Output

Return $P\in\mathbb{R}^{n\times n}$ satisfying $P=P^{\mathsf T}=P^2$ and $\operatorname{rank}(P)=k$, or an orthonormal basis for that projector. Neither $AP$ nor an error certificate is required.

### Loss or accuracy criterion

For finite $p$, use $\|M\|_{S_p}=(\sum_i\sigma_i(M)^p)^{1/p}$; $p=\infty$ gives the spectral norm. Define $\operatorname{OPT}_{p,k}=\min_{\operatorname{rank}(B)\le k}\|A-B\|_{S_p}$.

Success means $\|A(I_n-P)\|_{S_p}\le(1+\varepsilon)\operatorname{OPT}_{p,k}$. Zero optimal residual requires exact recovery of the relevant row space. The unsquared criterion is retained.

### Resource accounting

Retain the joint budget $(N_{\mathrm{r}},N_{\mathrm{l}})$, whose coordinates count single-vector calls to $Av$ and $A^{\mathsf T}u$, respectively. This setting explicitly uses the equal-weight scalarization $N=N_{\mathrm{r}}+N_{\mathrm{l}}$. Each column of a block is charged separately.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using only public inputs. For every admissible input fixed before its private seed is generated, the success event has probability at least $2/3$ over that private randomness.

**Budget convention.** A fixed worst-case budget respected for every input and private seed.

## 2. Notation and parameters

$m$: Number of rows of the input matrix **Domain:** $m\in\mathbb N,\ m\ge1$.

$A\in\mathbb R^{m\times n}$

$n$: Number of columns of the input matrix **Domain:** $n\in\mathbb N,\ n\ge1$.

$A\in\mathbb R^{m\times n}$

$d_{\mathrm{min}}$: Smaller dimension of the input matrix **Domain:** $d_{\min}=\min\{m,n\}\ge2$.

$d_{\mathrm{min}}=\min\{m,n\}$

$k$: The exact rank of the output orthogonal right projection. **Domain:** $k\in\mathbb N,\ 1\le k<d_{\mathrm{min}}$.

$\operatorname{rank}(P)=k$

$p$: The Schatten-norm order used in the residual. It may vary with other parameters in the uniform region. **Domain:** $1\le p\le\infty$.

$\|M\|_{S_p}=(\sum_i\sigma_i(M)^p)^{1/p}\quad(p<\infty)$

$\varepsilon$: The additional relative factor above the optimal Schatten residual. **Domain:** $\varepsilon>0$.

$\|A(I_n-P)\|_{S_p}\le(1+\varepsilon)\operatorname{OPT}_{p,k}$

$\varepsilon_0$: Fixed accuracy threshold permitted by the uniform lower bound in LR26, Theorem 3.1 **Domain:** $0<\varepsilon_0\le1$, a universal constant.

$0<\varepsilon\le\varepsilon_0$

$\varepsilon_p$: The accuracy threshold permitted by LR26 after fixing p ∈ [1,2). **Domain:** The threshold satisfies $0<\varepsilon_p\le1$ and depends only on fixed $p$.

$0<\varepsilon\le\varepsilon_p$

$C_{\mathrm{bridge}}$: Universal bridge constant chosen when transferring a larger-p Schatten target to an operator-norm target **Domain:** The quantity $C_{\mathrm{bridge}}>0$ is fixed in advance.

$C_{\mathrm{bridge}}\log2\ge1,\quad e^{\varepsilon/C_{\mathrm{bridge}}}\le1+\varepsilon/4\quad(0<\varepsilon\le1)$

$A$: The hidden arbitrary input matrix. **Domain:** $\mathbb R^{m\times n}$.

$P$: Returned right orthogonal projection **Domain:** $\mathbb R^{n\times n}$.

$P=P^{\mathsf T}=P^2,\quad\operatorname{rank}(P)=k$

$I_n$: The order-n identity matrix. **Domain:** $\mathbb R^{n\times n}$.

$\sigma_i(M)$: Singular values in nonincreasing order **Domain:** $1\le i\le\min\{\operatorname{rows}(M),\operatorname{cols}(M)\}$.

$\sigma_1(M)\ge\cdots\ge\sigma_{\min\{\operatorname{rows}(M),\operatorname{cols}(M)\}}(M)\ge0$

$\|M\|_{S_p}$: Schatten norm; for finite order, apply the $\ell_p$ norm to singular values **Domain:** Arbitrary rectangular matrix.

$\|M\|_{S_p}=(\sum_i\sigma_i(M)^p)^{1/p}\ (p<\infty),\quad\|M\|_{S_\infty}=\sigma_1(M)$

$A_k$: Any best approximation of rank at most $k$ obtained by truncating to the leading $k$ singular directions **Domain:** $\mathbb R^{m\times n}$.

$\operatorname{OPT}_{p,k}$: The best Schatten residual at rank at most k. **Domain:** A nonnegative real.

$\operatorname{OPT}_{p,k}=\min_{\operatorname{rank}(B)\le k}\|A-B\|_{S_p}=\|A-A_k\|_{S_p}$

$\Phi_{\mathrm{lr}}(p,\varepsilon)$: Polynomial core of the uniform low-rank complexity bound **Domain:** $2\le p<\infty$.

$\Phi_{\mathrm{lr}}(p,\varepsilon)=\min\{p^{1/6}\varepsilon^{-1/3},\varepsilon^{-1/2}\}$

$c_B$: A fixed universal witness constant within the range permitted by BCW Theorem 5.1. **Domain:** $c_B>0$.

$p\le c_B\log(d_{\mathrm{min}})/\delta_B$

$\alpha_B,\delta_B$: Fixed scaling and internal accuracy for invoking BCW in the uniform-p regime **Domain:** An internal algorithm parameter.

$\alpha_B=\min\{1/2,c_B/(2C_{\mathrm{bridge}})\},\quad\delta_B=\alpha_B\varepsilon$

$\beta_B,\delta_{\mathrm{low}}$: The scaling and internal precision used to apply BCW in the fixed $p<2$ region. **Domain:** An internal algorithm parameter.

$$
\begin{aligned}
\beta_B&=\min\{1/2,c_B\log2/4\},\\
\delta_{\mathrm{low}}&=\beta_B\varepsilon.
\end{aligned}
$$

$\eta$: Internal accuracy used when invoking the spectral-norm block Krylov upper bound **Domain:** An internal algorithm parameter.

$\eta=\varepsilon/4$

$Q_p^\star$: Minimum worst-case total two-sided calls attaining the right-projection error guarantee for the specified p **Domain:** $\mathbb N_0\cup\{+\infty\}$.

$c_p,C_p$: Positive constants may depend on $p$ only in comparisons that fix $p\in[1,2)$ in advance. **Domain:** Uniform in m, n, k, and ε.

$\widetilde O,\widetilde\Omega,\widetilde\Theta$: Suppress only the logarithmic factors explicitly registered for this bound. **Domain:** Polynomial dependence on $p$ is explicit in a regime uniform over $p$.

$\|z\|_2$: Euclidean norm of a vector **Domain:** Finite-dimensional real or complex vector.

$\|z\|_2=(\sum_i|z_i|^2)^{1/2}$

$\|M\|_{\mathrm{op}}$: The matrix operator norm induced by the Euclidean norm. **Domain:** Any compatible matrix.

$\|M\|_{\mathrm{op}}=\max_{\|z\|_2=1}\|Mz\|_2=\sigma_1(M)$

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
Q_p^\star(m,n,k,\varepsilon)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

#### Q2 - target accuracy cost

$$
Q_p^\star(m,n,k,\varepsilon),\qquad p\ \mathrm{fixed}
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - A uniform comparison across finite norm orders.

**Region.** Assume $2\le p<\infty$, $0<\varepsilon\le\varepsilon_0$, and $1\le k<d_{\mathrm{min}}$. Hidden constants are uniform in $p$ as it varies within this regime.

**Quantity.** Q1

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Logarithmic gap

**Lower bound.** B1

$$
\Omega(\min\{d_{\mathrm{min}},k\min\{p^{1/6}\varepsilon^{-1/3},\varepsilon^{-1/2}\}\})
$$

**Upper bound.** B4, B5, B8

$$
\widetilde{O}(\min\{d_{\mathrm{min}},k\min\{p^{1/6}\varepsilon^{-1/3},\varepsilon^{-1/2}\}\})
$$

**Gap or comparison.** The ratio is at most $O\!\left(\log\!\frac{2d_{\mathrm{min}}}{\varepsilon}\sqrt{\log(2d_{\mathrm{min}})}\right)$, hence also $O\!\left(\log^{3/2}\!\frac{2d_{\mathrm{min}}}{\varepsilon}\right)$. Universal constants are independent of every $p\ge2$ varying in this region.

**Comparison argument.** Compare the bound of each complete algorithm with reconstruction in $d_{\mathrm{min}}$ queries, where $d_{\mathrm{min}}=\min\{m,n\}$ corresponds to the source dimension notation $N$. Three cases cover the full declared region. If $p\varepsilon\le1$, then $\sqrt p\le p^{1/6}\varepsilon^{-1/3}$. If $1\le p\varepsilon\le C_{\mathrm{bridge}}\log d_{\mathrm{min}}$, both BCW terms are bounded by $\varepsilon^{-1/2}\operatorname{polylog}(d_{\mathrm{min}})$. If $p\ge C_{\mathrm{bridge}}\log(d_{\mathrm{min}})/\varepsilon$, the spectral-norm conversion applies. Constants depending on fixed $p$ remain explicit; the $\sqrt p$ term growing with $p$ is retained. After rescaling BCW's internal tolerance, the first case incurs $\log(2d_{\mathrm{min}}/\varepsilon)$, the second adds at most $\sqrt{C_{\mathrm{bridge}}\log d_{\mathrm{min}}}$, and the third uses the single-logarithm spectral bound. With $\Phi_{\mathrm{lr}}(p,\varepsilon)=\min\{p^{1/6}\varepsilon^{-1/3},\varepsilon^{-1/2}\}$, this gives $Q_{\mathrm{upper}}\le\min\{d_{\mathrm{min}},Ck\Phi_{\mathrm{lr}}(p,\varepsilon)\log(2d_{\mathrm{min}}/\varepsilon)\sqrt{\log(2d_{\mathrm{min}})}\}$. The minimum includes only applicable branches. BCW's parameter window is enforced using $\delta_B=\alpha_B\varepsilon$ with the stated rescaling constant; it cannot be dropped by silently changing hidden constants.

### R2 - The spectral-norm endpoint.

**Region.** $p=\infty$, $0<\varepsilon\le\varepsilon_0$, $1\le k<d_{\mathrm{min}}$.

**Quantity.** Q1

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(\min\{d_{\mathrm{min}},k\varepsilon^{-1/2}\})
$$

**Upper bound.** B6, B9

$$
\widetilde{O}(\min\{d_{\mathrm{min}},k\varepsilon^{-1/2}\})
$$

**Gap or comparison.** The bound is $O\!\left(\log\!\frac{2d_{\mathrm{min}}}{\varepsilon}\right)$ with universal constants.

**Comparison argument.** The spectral block-Krylov method and full reconstruction in $d_{\mathrm{min}}$ calls are separate complete algorithms. Comparing their minimum cost with $\Omega(\min\{d_{\mathrm{min}},k\varepsilon^{-1/2}\})$ bounds the upper-to-lower ratio by $C\log(2d_{\mathrm{min}}/\varepsilon)$.

### R3 - Small norm order fixed in advance

**Region.** Fix $p\in[1,2)$ first, then let $0<\varepsilon\le\varepsilon_p$ and $1\le k<d_{\mathrm{min}}$. The threshold $\varepsilon_p$ and hidden constants may depend on this fixed $p$.

**Quantity.** Q2

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Logarithmic gap

**Lower bound.** B3

$$
\Omega(\min\{d_{\mathrm{min}},k\varepsilon^{-1/3}\})
$$

**Upper bound.** B7, B10

$$
\widetilde{O}(\min\{d_{\mathrm{min}},k\varepsilon^{-1/3}\})
$$

**Gap or comparison.** $O_p\!\left(\log\!\frac{2d_{\mathrm{min}}}{\varepsilon}\right)$. Fix exponent $p$ in $[1,2)$ beforehand; constants may depend on this fixed $p$.

**Comparison argument.** Fix $1\le p<2$ and run BCW at $\delta_{\mathrm{low}}=\beta_B\varepsilon$. Compare its $C_p k\varepsilon^{-1/3}\log(2d_{\mathrm{min}}/\varepsilon)$ calls with reconstruction in $d_{\mathrm{min}}$ queries, then compare their minimum with the lower bound on the same region. The ratio is $O_p(\log(2d_{\mathrm{min}}/\varepsilon))$.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact $Av$ and $A^{\mathsf T}u$ are available for $v\in\mathbb R^n$ and $u\in\mathbb R^m$. Each column is charged separately. Block width and Krylov rounds do not replace total calls.

**Guarantee mapping.** Success probability is at least 2/3 for each fixed A. Retain the bound’s constant and accuracy windows for fixed and variable p.

**Output mapping.** Output a right orthogonal projector $\widehat P$ of rank $k$ satisfying $\|A(I_n-\widehat P)\|_{S_p}\le(1+\varepsilon)\|A-A_k\|_{S_p}$. The input $A$ need not have low rank. If the optimal tail is zero, success requires exactly zero residual.

**Resource mapping.** Retain joint budget $(N_{\mathrm r},N_{\mathrm l})$ for single-vector $Av$ and $A^{\mathsf T}u$ calls, with the explicit equal-weight scalarization $N=N_{\mathrm r}+N_{\mathrm l}$. Charge each block column separately. The budget is a worst-case cap for every input and private seed, not an expected count. Reading public inputs and internal exact-real arithmetic, storage, and postprocessing are uncharged; query complexity is not runtime or bit complexity.

### B1 - Lower bound for arbitrary randomized adaptive two-sided queries (Zhang et al., 2026)

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\min\{d_{\mathrm{min}},k\min\{p^{1/6}\varepsilon^{-1/3},\varepsilon^{-1/2}\}\})
$$

**Sources.** [2](https://arxiv.org/pdf/2609.35840v2)

**Conditions.**

$$
2\le p<\infty , 0<\varepsilon \le \varepsilon 0, 1\le k<d_{\mathrm{min}}
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**Q.**

$$
\Omega(\min\{d_{\mathrm{min}},k\min\{p^{1/6}\varepsilon^{-1/3},\varepsilon^{-1/2}\}\})
$$

**Constants.** The constant c and sufficient-accuracy threshold ε_0 are universal, uniformly in p and the other tracked parameters.

**Source location.** [2](https://arxiv.org/pdf/2609.35840v2) theorem: Theorem 3.1; Proposition 3.2; section: §3; §9; pdf pages: 4; 5; 24; equations: (4); (6); (7); (65)

The complete model, fixed worst-case budget, and 2/3 success probability have been verified. The key zero-padding, left-to-right projection, posterior-factorization, and overlap arguments have been read; the high-order spectral-profile lemma has not been independently reproved.

### B2 - Lower bound for arbitrary randomized adaptive two-sided queries (Zhang et al., 2026)

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\min\{d_{\mathrm{min}},k\varepsilon^{-1/2}\})
$$

**Sources.** [2](https://arxiv.org/pdf/2609.35840v2)

**Conditions.**

$$
p=\infty , 0<\varepsilon \le \varepsilon 0, 1\le k<d_{\mathrm{min}}
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**Q.**

$$
\Omega(\min\{d_{\mathrm{min}},k\varepsilon^{-1/2}\})
$$

**Constants.** The constant c and sufficient-accuracy threshold ε_0 are universal, uniformly in p and the other tracked parameters.

**Source location.** [2](https://arxiv.org/pdf/2609.35840v2) theorem: Theorem 3.1; Proposition 3.2; section: §3; §9; pdf pages: 4; 5; 24; equations: (4); (6); (7); (65)

The complete model, fixed worst-case budget, and 2/3 success probability have been verified. The key zero-padding, left-to-right projection, posterior-factorization, and overlap arguments have been read; the high-order spectral-profile lemma has not been independently reproved.

### B3 - Lower bound for arbitrary randomized adaptive two-sided queries (Zhang et al., 2026)

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\min\{d_{\mathrm{min}},k\varepsilon^{-1/3}\})
$$

**Sources.** [2](https://arxiv.org/pdf/2609.35840v2)

**Conditions.** Fix p in [1,2) in advance; 0<epsilon<=epsilon_p and 1<=k<d_min.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**Q.**

$$
\Omega(\min\{d_{\mathrm{min}},k\varepsilon^{-1/3}\})
$$

**Constants.** The constants $c_p$ and sufficient-accuracy threshold $\epsilon_p$ may depend on fixed $p\in[1,2)$ and are uniform in the remaining parameters.

**Source location.** [2](https://arxiv.org/pdf/2609.35840v2) theorem: Theorem 3.1; Proposition 3.2; section: §3; §9; pdf pages: 4; 5; 24; equations: (4); (6); (7); (65)

The complete model, fixed worst-case budget, and 2/3 success probability have been verified. The key zero-padding, left-to-right projection, posterior-factorization, and overlap arguments have been read; the high-order spectral-profile lemma has not been independently reproved.

### B4 - Randomized block Krylov with spectral-norm conversion. The full algorithm class is unrestricted.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le Ck\log(2d_{\mathrm{min}}/\varepsilon)\left[p^{1/6}\varepsilon^{-1/3}+\sqrt{p}\right]
$$

**Sources.** [2](https://arxiv.org/pdf/2609.35840v2) [1](https://arxiv.org/pdf/2202.05120v4)

**Conditions.** $2\le p\le C_{\mathrm{bridge}}\log(d_{\mathrm{min}})/\varepsilon$; $0<\varepsilon\le\varepsilon_0\le1$. The internal precision satisfies the BCW condition $p\le c_B\log(d_{\mathrm{min}})/\delta_B$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**Q.** $Ck\log\!\frac{2d_{\mathrm{min}}}{\varepsilon}\left(p^{1/6}\varepsilon^{-1/3}+\sqrt p\right)$

**Constants.** The constant $C$ is uniform in $m,n,k,p,\epsilon$. The quantities $c_B,C_{\mathrm{bridge}},\alpha_B$ are fixed universal proof constants.

**Derivation.** Let $\alpha_B=\min\{1/2,c_B/(2C_{\mathrm{bridge}})\}$ and run BCW with internal tolerance $\delta_B=\alpha_B\varepsilon$. If $p\varepsilon\le C_{\mathrm{bridge}}\log d_{\mathrm{min}}$, then $p\le c_B\log(d_{\mathrm{min}})/\delta_B$, while $\delta_B\le\varepsilon/2<1$. The source residual guarantee $(1+\delta_B)$ therefore implies the target $(1+\varepsilon)$ guarantee. Substituting $\delta_B$ into the query bound gives $N\le Ck\log(2d_{\mathrm{min}}/\varepsilon)[p^{1/6}\varepsilon^{-1/3}+\sqrt p]$. Since $\alpha_B$ is fixed in advance, the constants are uniform in varying p. When $m<n$, run the algorithm on $A^{\mathsf T}$ and include at most k additional $A^{\mathsf T}U$ calls to form the right projector. The resulting right subspace may be enlarged to rank k, which can only decrease the residual.

**Source location.** [2](https://arxiv.org/pdf/2609.35840v2) theorem: Theorem 3.1; Proposition 3.2; section: §3; §9; pdf pages: 4; 5; 24; equations: (4); (6); (7); (65)

The complete model, fixed worst-case budget, and 2/3 success probability have been verified. The key zero-padding, left-to-right projection, posterior-factorization, and overlap arguments have been read; the high-order spectral-profile lemma has not been independently reproved.

**Source location.** [1](https://arxiv.org/pdf/2202.05120v4) theorem: Theorem 5.1; section: §5; pdf pages: 16

Retain both the $p^{1/6}$ and $\sqrt p$ terms of the inherited upper bound. The $\sqrt p$ term cannot be dropped when $p$ grows.

### B5 - Randomized block Krylov with spectral-norm conversion. The full algorithm class is unrestricted.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le Ck\varepsilon^{-1/2}\log(2d_{\mathrm{min}}/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/2609.35840v2) [3](https://arxiv.org/pdf/1504.05477v4)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**Q.** $Ck\varepsilon^{-1/2}\log\!\frac{2d_{\mathrm{min}}}{\varepsilon}$

**Constants.** Spectral-norm algorithm constants are universal. The transfer to larger p uses only the fixed C_bridge.

**Logarithmic factors.** The only logarithmic factor is the explicit $\log(2d_{\mathrm{min}}/\varepsilon)$. No unspecified additional logarithmic powers are hidden.

**Derivation.** Run the Musco-Musco block Krylov algorithm at internal spectral tolerance $\eta=\varepsilon/4$. The iteration count is $$
O\bigl(\varepsilon^{-1/2}\log(2d_{\mathrm{min}}/\varepsilon)\bigr).
$$ Charging each column separately and including the output conversion gives $$
N\le Ck\varepsilon^{-1/2}\log(2d_{\mathrm{min}}/\varepsilon).
$$ This branch requires $p\ge C_{\mathrm{bridge}}\log(d_{\mathrm{min}})/\varepsilon$, hence $d_{\mathrm{min}}^{1/p}\le1+\varepsilon/4$. Using $\operatorname{rank}(A(I_n-P))\le d_{\mathrm{min}}$ yields $$
\begin{aligned}
\|A(I_n-P)\|_{S_p}
&\le(1+\varepsilon/4)^2\operatorname{OPT}_{\infty,k}\\
&\le(1+\varepsilon)\operatorname{OPT}_{p,k}.
\end{aligned}
$$

**Source location.** [2](https://arxiv.org/pdf/2609.35840v2) theorem: Theorem 3.1; Proposition 3.2; section: §3; §9; pdf pages: 4; 5; 24; equations: (4); (6); (7); (65)

The complete model, fixed worst-case budget, and 2/3 success probability have been verified. The key zero-padding, left-to-right projection, posterior-factorization, and overlap arguments have been read; the high-order spectral-profile lemma has not been independently reproved.

**Source location.** [3](https://arxiv.org/pdf/1504.05477v4) theorem: Algorithm 2; Theorem 1; Theorem 10; section: 2.1, 2.3, 6; pdf pages: 3; 4; 14; printed pages: 3; 4; 14; equations: (2)

Original arXiv v4 PDF read from author MIT mirror. Query-count derivation counts every block column; arithmetic costs remain uncharged. The new Schatten lower theorem was not independently reproved.

For rectangular matrices choose an orientation with the smaller dimension on the right; the LR26 section9 projector conversion adds at most k products.

### B6 - Randomized block Krylov with spectral-norm conversion. The full algorithm class is unrestricted.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le Ck\varepsilon^{-1/2}\log(2d_{\mathrm{min}}/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/2609.35840v2) [3](https://arxiv.org/pdf/1504.05477v4)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**Q.** $Ck\varepsilon^{-1/2}\log\!\frac{2d_{\mathrm{min}}}{\varepsilon}$

**Constants.** Spectral-norm algorithm constants are universal. The transfer to larger p uses only the fixed C_bridge.

**Logarithmic factors.** The only logarithmic factor is the explicit $\log(2d_{\mathrm{min}}/\varepsilon)$. No unspecified additional logarithmic powers are hidden.

**Derivation.** Run the Musco-Musco block Krylov algorithm at internal spectral tolerance $\eta=\varepsilon/4$. Its iteration count is $$
O\bigl(\varepsilon^{-1/2}\log(2d_{\mathrm{min}}/\varepsilon)\bigr).
$$. Charging each column and including output conversion gives total calls $$
N\le Ck\varepsilon^{-1/2}\log(2d_{\mathrm{min}}/\varepsilon).
$$.

**Source location.** [2](https://arxiv.org/pdf/2609.35840v2) theorem: Theorem 3.1; Proposition 3.2; section: §3; §9; pdf pages: 4; 5; 24; equations: (4); (6); (7); (65)

The complete model, fixed worst-case budget, and 2/3 success probability have been verified. The key zero-padding, left-to-right projection, posterior-factorization, and overlap arguments have been read; the high-order spectral-profile lemma has not been independently reproved.

**Source location.** [3](https://arxiv.org/pdf/1504.05477v4) theorem: Algorithm 2; Theorem 1; Theorem 10; section: 2.1, 2.3, 6; pdf pages: 3; 4; 14; printed pages: 3; 4; 14; equations: (2)

Original arXiv v4 PDF read from author MIT mirror. Query-count derivation counts every block column; arithmetic costs remain uncharged. The new Schatten lower theorem was not independently reproved.

For rectangular matrices choose an orientation with the smaller dimension on the right; the LR26 section9 projector conversion adds at most k products.

### B7 - Randomized block Krylov with spectral-norm conversion. The full algorithm class is unrestricted.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le C_p k\varepsilon^{-1/3}\log(2d_{\mathrm{min}}/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/2609.35840v2) [1](https://arxiv.org/pdf/2202.05120v4)

**Conditions.** First fix $p\in[1,2)$ and $0<\varepsilon\le\varepsilon_p\le1$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**Q.** $C_p k\varepsilon^{-1/3}\log\!\frac{2d_{\mathrm{min}}}{\varepsilon}$

**Constants.** Only in this explicitly fixed p in [1,2) regime may C_p, c_p, and epsilon_p depend on p; they are uniform in m, n, k, and epsilon.

**Logarithmic factors.** The only logarithmic factor is the explicit $\log(2d_{\mathrm{min}}/\varepsilon)$. No unspecified additional logarithmic powers are hidden.

**Derivation.** Fix $1\le p<2$, set $\delta_{\mathrm{low}}=\beta_B\varepsilon$ and $\beta_B=\min\{1/2,c_B\log2/4\}$. Since $d_{\mathrm{min}}\ge2$ and $\varepsilon\le\varepsilon_p\le1$, BCW's applicability condition $p\le c_B\log(d_{\mathrm{min}})/\delta_{\mathrm{low}}$ holds. The factors $p^{1/6}$ and $\sqrt p$ in its total query bound can be absorbed into constants depending on fixed p, giving $N\le C_p k\varepsilon^{-1/3}\log(2d_{\mathrm{min}}/\varepsilon)$.

**Source location.** [2](https://arxiv.org/pdf/2609.35840v2) theorem: Theorem 3.1; Proposition 3.2; section: §3; §9; pdf pages: 4; 5; 24; equations: (4); (6); (7); (65)

The complete model, fixed worst-case budget, and 2/3 success probability have been verified. The key zero-padding, left-to-right projection, posterior-factorization, and overlap arguments have been read; the high-order spectral-profile lemma has not been independently reproved.

**Source location.** [1](https://arxiv.org/pdf/2202.05120v4) theorem: Theorem 5.1; section: §5; pdf pages: 16

Retain both the $p^{1/6}$ and $\sqrt p$ terms of the inherited upper bound. The $\sqrt p$ term cannot be dropped when $p$ grows.

### B8 - Deterministic basis reconstruction, choosing the smaller row or column direction.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le\min\{m,n\}
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**joint alternatives.** [{"N_left": 0, "N_right": "n"}, {"N_left": "m", "N_right": 0}]

**Constants.** Exactly min{m,n} standard basis queries suffice, with no hidden logarithmic or p dependence.

**Derivation.** Public dimensions select a complete reconstruction algorithm; an internal SVD returns the right rank-k projection.

**Local argument.** A1

### B9 - Deterministic basis reconstruction, choosing the smaller row or column direction.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le\min\{m,n\}
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**joint alternatives.** [{"N_left": 0, "N_right": "n"}, {"N_left": "m", "N_right": 0}]

**Constants.** Exactly min{m,n} standard basis queries suffice, with no hidden logarithmic or p dependence.

**Derivation.** Public dimensions select a complete reconstruction algorithm; an internal SVD returns the right rank-k projection.

**Local argument.** A1

### B10 - Deterministic basis reconstruction, choosing the smaller row or column direction.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le\min\{m,n\}
$$

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**joint alternatives.** [{"N_left": 0, "N_right": "n"}, {"N_left": "m", "N_right": 0}]

**Constants.** Exactly min{m,n} standard basis queries suffice, with no hidden logarithmic or p dependence.

**Derivation.** Public dimensions select a complete reconstruction algorithm; an internal SVD returns the right rank-k projection.

**Local argument.** A1

## 5. Local arguments

### A1 - Deterministic basis reconstruction, choosing the smaller row or column direction.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Recover all columns in $n$ right queries or all rows in $m$ transpose queries, choosing the cheaper channel. Exact internal singular-value decomposition returns the orthogonal right projection onto the leading $k$ right singular vectors. The singular-value characterization of the best rank-$k$ Schatten approximation shows that the residual is optimal for the declared norm order, including zero optimal residual. The query count is $\min\{m,n\}$; the two alternatives are complete algorithms, not a coordinatewise combination of budgets.

## References

[1] Ainesh Bakshi; Kenneth L. Clarkson; David P. Woodruff. Low-Rank Approximation with 1/epsilon^(1/3) Matrix-Vector Products. 2022. arXiv:2202.05120v4; 2022-06-16.

https://arxiv.org/pdf/2202.05120v4

[2] Haihan Zhang; Wendao Wu; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matrix–Vector Complexity of Low-Rank Approximation. 2026. arXiv:2609.35840v2; 2026-10-19.

https://arxiv.org/pdf/2609.35840v2

[3] Cameron Musco; Christopher Musco. Randomized Block Krylov Methods for Stronger and Faster Approximate Singular Value Decomposition. 2015. arXiv:1504.05477v4; 2015-10-30.

https://arxiv.org/pdf/1504.05477v4
