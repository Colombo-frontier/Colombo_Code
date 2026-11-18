# One-pass low-rank approximation from row streams, with real-register memory.

**Setting ID.** `MX_S_stream_real`

Matrix computation

After one pass over the rows of $A\in\mathbb{R}^{m\times n}$, return a rank-$k$ orthogonal right projection.

**Status.** Bounds missing

**TASK tags.** formulation: Row streaming lowrank; solution concept: Relative frobenius squared projection; task family: Matrix computation

**MODEL tags.** spectral structure: Arbitrary real matrix; structure: Row stream

**ORACLE tags.** feedback quality: Exact; interface family: Row stream; operation: Matrix stream update; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** memory: Exact-real register state; randomization: Private randomness allowed; restriction: No past requery; restriction: One pass

**OUTPUT tags.** certificate: No additional output certificate required; object: Orthogonal projector or basis

**METRIC tags.** criterion: Relative squared projection residual

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** measure: Arithmetic; measure: Memory registers; measure: Passes; measure: Stream rows

## 1. Setting specification

### Task

After one pass over the rows of $A\in\mathbb{R}^{m\times n}$, return a rank-$k$ orthogonal right projection.

### Admissible model

The input $A$ is an arbitrary real matrix with a row order fixed in advance. Assume $m,n\ge1$, $1\le k<\min\{m,n\}$, and $\varepsilon>0$.

### Oracle interface

The quantity $m,n,k,\varepsilon$ is public. Each call returns only the next complete row. Consumed rows are unavailable again, and the algorithm cannot query $Av$ or reread the input after the stream ends.

### Output

After the stream, use only retained state to output $P=P^{\mathsf T}=P^2\in\mathbb{R}^{n\times n}$ with $\operatorname{rank}(P)=k$; an orthonormal-basis representation is allowed. Returning $AP$ is unnecessary.

### Loss or accuracy criterion

Let $A_k$ be any best rank-$k$ Frobenius approximation. Success requires $\|A(I_n-P)\|_{\mathrm{F}}^2\le(1+\varepsilon)\|A-A_k\|_{\mathrm{F}}^2$; the residual is explicitly squared. When the optimal residual is zero, the row space must be recovered exactly.

### Resource accounting

The native resource is the maximum number $S_{\mathbb R}$ of simultaneously retained exact real registers. One pass is fixed by the protocol, and arithmetic is free. No bit width per register is specified.

The cost limit holds for every input and private seed. The final output must be decoded from the charged state, without an unregistered external cache.

### Algorithm views and success guarantees

Randomized single-pass streaming algorithms are permitted. State consists of exact-real registers updated by ordinary arithmetic and comparisons. Uncharged arbitrary encodings that compress the entire real input stream into one register are excluded. Apart from the single-pass and register-memory constraints, internal arithmetic time is unrestricted.

The algorithm is selected using only public inputs. For every admissible input fixed before its private seed is generated, the success event has probability at least $2/3$ over that private randomness.

**Budget convention.** One pass; peak memory is bounded for every input and random seed.

## 2. Notation and parameters

$m$: Number of rows of the input matrix **Domain:** $m\in\mathbb N,\ m\ge1$.

$A\in\mathbb R^{m\times n}$

$n$: Number of columns of the input matrix **Domain:** $n\in\mathbb N,\ n\ge1$.

$A\in\mathbb R^{m\times n}$

$k$: The exact rank of the orthogonal right projection returned after the stream. **Domain:** $k\in\mathbb N,\ 1\le k<\min\{m,n\}$.

$\operatorname{rank}(P)=k$

$\varepsilon$: Additional relative factor over the optimal squared Frobenius residual **Domain:** $\varepsilon>0$.

$\|A(I_n-P)\|_F^2\le(1+\varepsilon)\|A-A_k\|_F^2$

$A$: The input matrix arriving in a precommitted row order. **Domain:** $\mathbb R^{m\times n}$.

$P$: Right orthogonal projector returned after the stream ends **Domain:** $\mathbb R^{n\times n}$.

$P=P^{\mathsf T}=P^2,\quad\operatorname{rank}(P)=k$

$I_n$: The order-n identity matrix. **Domain:** $\mathbb R^{n\times n}$.

$A_k$: Best Frobenius approximation of rank at most $k$ **Domain:** $\mathbb R^{m\times n}$.

$A_k\in\arg\min_{\operatorname{rank}(B)\le k}\|A-B\|_F$

$\|M\|_{\mathrm F}$: The Frobenius norm. **Domain:** An arbitrary real or complex matrix.

$\|M\|_{\mathrm F}=(\sum_{ij}|M_{ij}|^2)^{1/2}=(\sum_i\sigma_i(M)^2)^{1/2}$

$c,C$: Positive universal constants in the corresponding bound. Identically named constants in different theorems need not have the same value. **Domain:** Independent of the dimension, accuracy, and probability parameters tracked by this bound.

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

$S_{\mathbb R}$: Maximum number of exact real registers retained simultaneously during execution **Domain:** $\mathbb N_0$.

$M^\star_{\mathrm{real}}$: Minimum worst-case number of real registers needed for the one-pass output guarantee **Domain:** $\mathbb N_0\cup\{+\infty\}$.

$\ell$: Number of rows in the Frequent Directions sketch **Domain:** $\mathbb N$.

$\ell=\lceil k+k/\varepsilon\rceil\le n$

## 3. Complexity bracket

### Compared quantities

#### Q1 - memory complexity

$$
M^\star_{\mathrm{real}}(m,n,k,\varepsilon)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - Frequent Directions sketch-size window

**Region.** Assume $1\le k<\min\{m,n\}$, $0<\varepsilon<1$, and $\lceil k+k/\varepsilon\rceil\le n$.

**Quantity.** Q1

**Resource.** Number of real-valued registers

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(nk/\varepsilon)
$$

**Comparison argument.** Only feasible joint resource points are asserted. No unconditional real-register lower bound is claimed.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The same choice of $\ell$ simultaneously attains the space, time, and one-pass requirements.

**Oracle mapping.** A single-pass row-arrival interface with row order fixed in advance. Each step reveals only the current complete row; no Av, A^T u, selectable-row query, or rereading is available.

**Guarantee mapping.** The verified Frequent Directions upper bound is deterministic and holds for every fixed real-valued row stream, so it meets the required success probability of at least $2/3$.

**Output mapping.** Return only a right rank-k subspace or basis satisfying ||A-A P_hat||_F² <= (1+epsilon)||A-A_k||_F²; neither the complete product A P_hat nor an unsquared residual is the output target.

**Resource mapping.** The native resource is peak exact-real registers $S_{\mathbb R}$. One pass is a fixed protocol and arithmetic is free; register bit lengths are unspecified. The cap holds for every input and seed. Final output decodes only from charged state, without unrecorded external storage.

### B1 - Deterministic one-pass Frequent Directions sketch

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
S_{\mathbb{R}}\le Cn\left\lceil k+\frac{k}{\varepsilon}\right\rceil
$$

**Sources.** [1](https://arxiv.org/pdf/1501.01711)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**memory registers.** O(n ceil(k+k/eps))

**passes.** 1

**arithmetic.** O(m n ceil(k+k/eps))

**stream rows.** m

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/1501.01711) theorem: Theorems 1.2 and 1.5; section: §1.4; pdf pages: 4

Store O(n ell) floating-point numbers; accuracy is interpreted through an exact-arithmetic analysis. Set ell=ceil(k+k/epsilon). The output is a rank-k projection, not a higher-rank bicriteria approximation.

## References

[1] Mina Ghashami; Edo Liberty; Jeff M. Phillips; David P. Woodruff. Frequent Directions: Simple and Deterministic Matrix Sketching. 2016. arXiv:1501.01711; SIAM Journal on Computing publication.

https://arxiv.org/pdf/1501.01711
