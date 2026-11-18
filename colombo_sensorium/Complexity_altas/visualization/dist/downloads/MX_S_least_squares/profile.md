# Full-column-rank least squares: relative prediction error

**Setting ID.** `MX_S_least_squares`

Matrix computation

Solve $x^\star=\arg\min_{x\in\mathbb R^n}\|Ax-b\|_2^2$.

**Status.** Bounds missing

**TASK tags.** formulation: Least squares; solution concept: Least squares excess; task family: Matrix computation

**MODEL tags.** spectral structure: Full column rank

**ORACLE tags.** feedback quality: Exact; interface family: Exact two sided matvec; operation: Matrix left matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Vector

**METRIC tags.** criterion: Relative prediction error

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N left; measure: N right

## 1. Setting specification

### Task

Solve $x^\star=\arg\min_{x\in\mathbb R^n}\|Ax-b\|_2^2$.

### Admissible model

The matrix $A\in\mathbb{R}^{m\times n}$ has full column rank, with $m\ge n\ge1$, singular-value condition number $\sigma_1(A)/\sigma_n(A)\le\kappa$, and $\kappa\ge1$. The assumption $b\in\operatorname{range}(A)$ is not required.

### Oracle interface

Inputs $m,n,\kappa,\varepsilon,b\in\mathbb{R}^m,x_0\in\mathbb{R}^n$ are public and $A$ is hidden. Query $Av$ for any $v\in\mathbb{R}^n$ or $A^{\mathsf T}u$ for any $u\in\mathbb{R}^m$. Both are exact responses from the same fixed matrix. Computing $A^{\mathsf T}Av$ costs two calls.

### Output

Return any $\widehat x\in\mathbb R^n$, without restriction to the span of historical query vectors. No residual value or certificate is required.

### Loss or accuracy criterion

Use loss $\ell(\widehat{x})=\|A(\widehat{x}-x^\star)\|_2^2/\|A(x_0-x^\star)\|_2^2$ and require $\ell\le\varepsilon$. If the denominator is zero, the output must be an exact solution.

This quantity is the ratio of the least-squares objective gap to its initial gap. It is not relative total residual, which includes the irreducible fitting error $\|Ax^\star-b\|_2$.

### Resource accounting

Retain the joint budget $(N_{\mathrm{r}},N_{\mathrm{l}})$, whose coordinates count single-vector calls to $Av$ and $A^{\mathsf T}u$, respectively. This setting explicitly uses the equal-weight scalarization $N=N_{\mathrm{r}}+N_{\mathrm{l}}$. Each column of a block is charged separately.

The budget bounds calls for every fixed input and every private seed. Reading public inputs, exact real arithmetic, storage, and postprocessing are free. One call applies the interface to one vector.

### Algorithm views and success guarantees

Algorithms may use private randomness and choose query vectors adaptively from the declared domain using all previous responses. Queries and outputs may be arbitrary measurable functions of the transcript; no Krylov or linear-span restriction applies. Exact internal arithmetic, storage, and communication are free in this oracle model. A block query is charged by its number of columns.

The algorithm is selected using only public inputs. For every admissible input fixed before its private seed is generated, the success event has probability at least $2/3$ over that private randomness.

**Budget convention.** A fixed worst-case budget respected for every input and private seed.

## 2. Notation and parameters

$m$: Number of rows of the full-column-rank input matrix **Domain:** $m\in\mathbb N,\ m\ge n$.

$A\in\mathbb R^{m\times n}$

$n$: Number of columns of the full-column-rank input matrix, also the solution-vector dimension **Domain:** $n\in\mathbb N,\ 1\le n\le m$.

$x\in\mathbb R^n$

$\kappa$: Public upper bound on the singular-value condition number of the input matrix **Domain:** $\kappa\ge1$.

$\sigma_1(A)/\sigma_n(A)\le\kappa$

$\varepsilon$: Squared prediction-error tolerance relative to the squared initial prediction error. **Domain:** $\varepsilon>0$.

$\|A(\widehat x-x^\star)\|_2^2\le\varepsilon\|A(x_0-x^\star)\|_2^2$

$A$: Hidden full-column-rank input matrix **Domain:** $\mathbb R^{m\times n}$.

$b$: Public right-hand side, which need not lie in the column space of $A$. **Domain:** $\mathbb R^m$.

$x_0$: Public initial point **Domain:** $\mathbb R^n$.

$x^\star$: Unique least-squares solution **Domain:** $\mathbb R^n$.

$x^\star=(A^{\mathsf T}A)^{-1}A^{\mathsf T}b$

$\widehat x$: Algorithm output **Domain:** $\mathbb R^n$.

$\sigma_i(A)$: Input singular values in nonincreasing order. **Domain:** $1\le i\le n$.

$\sigma_1(A)\ge\cdots\ge\sigma_n(A)>0$

$\ell(\widehat x)$: Squared loss relative to the initial prediction error **Domain:** A zero denominator requires an exact solution.

$\ell(\widehat x)=\|A(\widehat x-x^\star)\|_2^2/\|A(x_0-x^\star)\|_2^2$

$t$: Number of conjugate-gradient iterations on the normal-equation matrix $A^\top A$ **Domain:** $\mathbb N_0$.

$N_{\rm r}=t,\ N_{\rm l}=t+1$

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

$\delta_0,\eta_0$: Two fixed auxiliary parameters in the instantiation of the DEM26 lower bound **Domain:** A fixed constant.

$\delta_0=\eta_0=1/2$

$B_{\rm normal},c_{\rm normal}$: Normal-equation matrix and right-hand side **Domain:** $\mathbb R^{n\times n}\times\mathbb R^n$.

$B_{\rm normal}=A^{\mathsf T}A,\quad c_{\rm normal}=A^{\mathsf T}b$

$\Phi_{\rm saddle}(x,y)$: Associated saddle-point formulation of the least-squares problem **Domain:** In the associated reduction, $x\in\mathbb R^n$ and $y\in\mathbb R^m$.

$\Phi_{\rm saddle}(x,y)=y^{\mathsf T}(Ax-b)-\tfrac12\|y\|_2^2$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star_{Av,A^{\mathsf T}u}(\varepsilon;m,n,\kappa)
$$

**Scope.** Within the cited complete specification, select an algorithm before taking the worst case over all fixed inputs. Information permissions remain unchanged.

**Optimization direction.** minimize

### R1 - Basic accuracy regime

**Region.** $m\ge n\ge1$, $\kappa\ge2$, $0<\varepsilon<1$.

**Quantity.** Q1

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1, B2

$$
\min\{n,1+2C\kappa\log(4/\varepsilon)\}
$$

**Comparison argument.** A feasible upper bound has been verified. A lower bound for an interface returning only A^T A v cannot be directly applied to the two channels (Av,A^T u).

### R2 - High-accuracy matching window from the 2026 result

**Region.** Assume $\kappa\ge2$, $m\ge n\ge C\kappa^{13}$, and $n^{-4}\le\varepsilon\le n^{-2}$. The universal constant $C$ is inherited from the theorem and is not assigned an arbitrary numerical value.

**Quantity.** Q1

**Resource.** Sum of right and left matrix-vector product query counts.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega(\kappa\log n)
$$

**Upper bound.** B1, B2

$$
O(\kappa\log n)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** The source accuracy is tied to dimension; a constant-factor match is asserted only in the stated high-accuracy band.

## 4. Bounds and supporting evidence

### B1 - Deterministic CG on the normal equations, charging two calls per AᵀA product.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le1+2\lceil C\kappa\log(4/\varepsilon)\rceil
$$

**Sources.** [2](https://arxiv.org/pdf/1708.07788v2)

**Oracle correspondence.** Exact right products Av, v in R^n, and left products A^T u, u in R^m, are charged separately. One A^T Av evaluation costs two native calls.

**Guarantee conversion.** The verified normal-equation and reconstruction algorithms are deterministic and satisfy the required success probability of at least 2/3 per fixed input. Retain full column rank and public b and x0.

**Output rule.** Return $\widehat x\in\mathbb R^n$. The criterion is $\|A(\widehat x-x^\star)\|_2^2$ relative to $\|A(x_0-x^\star)\|_2^2$, measuring excess prediction error rather than total observed residual.

**Resource conversion.** Retain joint budget $(N_{\mathrm r},N_{\mathrm l})$ for single-vector $Av$ and $A^{\mathsf T}u$ calls, with the explicit equal-weight scalarization $N=N_{\mathrm r}+N_{\mathrm l}$. Charge each block column separately. The budget is a worst-case cap for every input and private seed, not an expected count. Reading public inputs and internal exact-real arithmetic, storage, and postprocessing are uncharged; query complexity is not runtime or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** t

**N left.** t+1

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** A product AᵀAv uses one Av and one Aᵀu query. Form Aᵀb once before iterating. The same t-step implementation jointly achieves (t, t + 1), where t = ceil(Cκ log(4/ε)).

**Local argument.** A1

### B2 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le n
$$

**Oracle correspondence.** Exact right products Av, v in R^n, and left products A^T u, u in R^m, are charged separately. One A^T Av evaluation costs two native calls.

**Guarantee conversion.** The verified normal-equation and reconstruction algorithms are deterministic and satisfy the required success probability of at least 2/3 per fixed input. Retain full column rank and public b and x0.

**Output rule.** Return $\widehat x\in\mathbb R^n$. The criterion is $\|A(\widehat x-x^\star)\|_2^2$ relative to $\|A(x_0-x^\star)\|_2^2$, measuring excess prediction error rather than total observed residual.

**Resource conversion.** Retain joint budget $(N_{\mathrm r},N_{\mathrm l})$ for single-vector $Av$ and $A^{\mathsf T}u$ calls, with the explicit equal-weight scalarization $N=N_{\mathrm r}+N_{\mathrm l}$. Charge each block column separately. The budget is a worst-case cap for every input and private seed, not an expected count. Reading public inputs and internal exact-real arithmetic, storage, and postprocessing are uncharged; query complexity is not runtime or bit complexity.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** n

**N left.** 0

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** Standard-basis queries reveal every matrix column.

**Local argument.** A2

### B3 - General randomized adaptive queries; randomly rotated spectral families and polynomial-approximation lower bounds

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c\kappa\log n
$$

**Sources.** [1](https://proceedings.mlr.press/v336/derezinski26a.html)

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

**Derivation.** Take $\delta_0=\eta_0=1/2$ in the source Theorem 2.8, with sufficient dimension $n\ge C\kappa^{13}$. Use its symmetric invertible hard matrix $n\times n$ as a consistent least-squares instance and set $x_0=0$. If $m>n$, append zero rows to the matrix and right-hand side. This preserves full column rank, the singular-value condition number, and the cost of both query directions. The loss is exactly $\|A\widehat x-b\|_2^2/\|b\|_2^2$, so $\varepsilon\le n^{-2}$ implies the source residual threshold $1/n$. Three independent repetitions, each followed by one right product to check the residual, raise success probability from $2/3$ to $26/27$. The original budget is therefore at least $c\kappa\log n-O(1)$. In the strip $n^{-4}\le\varepsilon\le n^{-2}$, the normal-equation CG upper bound $O(\kappa\log(1/\varepsilon))$ matches it. This does not establish a fixed-small-dimension optimum.

**Source location.** [1](https://proceedings.mlr.press/v336/derezinski26a.html) theorem: Theorem 2.8, PDF p.9; Appendix D.2

Take $\delta_0=\eta_0=1/2$ in the source Theorem 2.8, with sufficient dimension $n\ge C\kappa^{13}$. Use its symmetric invertible hard matrix $n\times n$ as a consistent least-squares instance and set $x_0=0$. If $m>n$, append zero rows to the matrix and right-hand side. This preserves full column rank, the singular-value condition number, and the cost of both query directions. The loss is exactly $\|A\widehat x-b\|_2^2/\|b\|_2^2$, so $\varepsilon\le n^{-2}$ implies the source residual threshold $1/n$. Three independent repetitions, each followed by one right product to check the residual, raise success probability from $2/3$ to $26/27$. The original budget is therefore at least $c\kappa\log n-O(1)$. In the strip $n^{-4}\le\varepsilon\le n^{-2}$, the normal-equation CG upper bound $O(\kappa\log(1/\varepsilon))$ matches it. This does not establish a fixed-small-dimension optimum.

## 5. Local arguments

### A1 - Deterministic CG on the normal equations, charging two calls per AᵀA product.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Let $B=A^{\mathsf T}A$ and $x^\star=B^{-1}A^{\mathsf T}b$. Full column rank makes $B$ positive definite, with $\kappa(B)=\kappa(A)^2\le\kappa^2$. Form the initial normal-equation residual $A^{\mathsf T}(b-Ax_0)$ using one right and one transpose product; a zero residual identifies the exact least-squares minimizer. Each subsequent $Bv$ uses one product with $A$ and one with $A^{\mathsf T}$.
CG gives
$$\|x_t-x^\star\|_B^2\le4\left(\frac{\kappa-1}{\kappa+1}\right)^{2t}\|x_0-x^\star\|_B^2.$$
Because $\|e\|_B^2=\|Ae\|_2^2$, the ratio is exactly the declared excess least-squares loss, including inconsistent systems. It is not relative total fitting residual. Choose $t=O(\kappa\log(4/\varepsilon))$. The implementation uses $t+1$ calls in each channel. Enlarging the universal ceiling constant absorbs initialization and gives the registered scalar form $1+2\lceil C\kappa\log(4/\varepsilon)\rceil$. In a joint-budget statement, take the displayed iteration allowance at least one larger than the number of CG updates; both actual channel counts then satisfy the recorded upper allowances. Exact arithmetic and public-data processing are uncharged.

**Sources.** [2](https://arxiv.org/pdf/1708.07788v2)

### A2 - Deterministic reconstruction using the standard basis, followed by free exact solution of the target task

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Query the $n$ standard basis vectors of $\mathbb R^n$ to recover the full rectangular matrix $A$. Full column rank makes $(A^{\mathsf T}A)^{-1}A^{\mathsf T}b$ the unique least-squares minimizer, even if $Ax=b$ is inconsistent. Exact internal linear algebra is uncharged, and the excess loss is zero. The joint query budget is $(n,0)$.

## References

[1] Michał Dereziński; Ethan N. Epperly; Raphael A. Meyer. The matrix-vector complexity of Ax = b. 2026. PMLR proceedings PDF, 34 pages.

https://proceedings.mlr.press/v336/derezinski26a.html

[2] Cameron Musco; Christopher Musco; Aaron Sidford. Stability of the Lanczos Method for Matrix Function Approximation. 2018. arXiv:1708.07788v2, revised 2024-11-18; SODA 2018.

https://arxiv.org/pdf/1708.07788v2
