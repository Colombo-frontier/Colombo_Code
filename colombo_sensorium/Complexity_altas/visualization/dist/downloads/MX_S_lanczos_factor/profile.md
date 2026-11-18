# Lanczos approximation of matrix functions: worst-case approximation factor

**Setting ID.** `MX_S_lanczos_factor`

Matrix computation

Compare the $t$-step Lanczos function approximation $y_t=V_t h(T_t)V_t^*b$ with the best approximation in $\mathcal{K}_t(A,b)$, under $T_t=V_t^*AV_t$.

**Status.** Fully optimal

**TASK tags.** formulation: Matrix function action; solution concept: Krylov near optimality ratio; task family: Matrix computation

**MODEL tags.** spectral structure: Hermitian positive definite; spectral structure: Hermitian positive stieltjes; spectral structure: Stieltjes extension

**ORACLE tags.** feedback quality: Exact; interface family: Exact complex matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** named method: Lanczos fa; randomization: Deterministic

**OUTPUT tags.** certificate: No additional output certificate required; object: Vector

**METRIC tags.** criterion: Worst case approximation factor

**GUARANTEE tags.** mode: Deterministic

**RESOURCE tags.** measure: N right

## 1. Setting specification

### Task

Compare the $t$-step Lanczos function approximation $y_t=V_t h(T_t)V_t^*b$ with the best approximation in $\mathcal{K}_t(A,b)$, under $T_t=V_t^*AV_t$.

### Admissible model

The matrix $A\in\mathbb{C}^{d\times d}$ is Hermitian positive definite with actual condition number $\kappa=\lambda_{\max}(A)/\lambda_{\min}(A)>1$ and at least $t+1$ distinct eigenvalues; $1\le t<d$. Also $b\ne0$ and $\alpha\in\mathbb{R}$. The function class consists of $h$ or functions whose $z\mapsto h(z)/z$ is Stieltjes: it admits the representation $\int_0^\infty(z+s)^{-1}\,d\nu(s)$ with positive measure $\nu$ satisfying $\int_0^\infty(1+s)^{-1}\,d\nu(s)<\infty$.

### Oracle interface

The data $d,t,\kappa,\alpha,h,b$ are public and $A$ is hidden. For any complex vector $v$, the interface returns exact $Av$. Internal complex arithmetic and scalar function evaluations are free.

### Output

Return the fixed algorithm's $y_t$. Substituting the best Krylov approximation would change the object being evaluated.

### Loss or accuracy criterion

Define the weighted norm $\|z\|_{A^\alpha}=(z^*A^\alpha z)^{1/2}$ and Krylov space $\mathcal{K}_t(A,b)=\operatorname{span}\{b,Ab,\ldots,A^{t-1}b\}$. Compare the fixed Lanczos output with the best approximation in that space through the error ratio $$
\mathcal{C}=\frac{\|h(A)b-y_t\|_{A^\alpha}}{\min_{y\in\mathcal{K}_t(A,b)}\|h(A)b-y\|_{A^\alpha}}.
$$. Use the conventions $0/0=1$ and positive numbers divided by zero equal $+\infty$.

### Resource accounting

The quantity is the dimensionless approximation factor $\mathcal{C}$, not the minimum query count for a target tolerance. The algorithm uses at most $t$ exact matrix-vector products. Internal arithmetic and scalar-function evaluations are uncharged.

### Algorithm views and success guarantees

The exact Lanczos function-approximation algorithm is fixed, without minimization over general algorithms. Equivalent orthonormal-basis implementations are allowed if they produce the same mathematical approximation.

The upper bound holds deterministically for every admissible fixed input. The lower bound concerns worst-case inputs for the fixed algorithm. The supremum over admissible inputs gives the stated sharp factor, generally through arbitrarily close lower examples.

**Budget convention.** For fixed t, Lanczos uses at most t matrix actions and possibly fewer under early termination. The native comparison target is an error factor.

## 2. Notation and parameters

$d$: Order of the Hermitian input matrix **Domain:** $d\in\mathbb N,\ d\ge t+1$.

$A\in\mathbb C^{d\times d}$

$t$: The step count of the exact Lanczos algorithm being evaluated. **Domain:** $t\in\mathbb N,\ 1\le t<d$.

$\mathcal K_t(A,b)=\operatorname{span}\{b,Ab,\ldots,A^{t-1}b\}$

$\kappa$: Actual spectral condition number of the positive definite input matrix **Domain:** $\kappa>1$.

$\kappa=\lambda_{\max}(A)/\lambda_{\min}(A)$

$\alpha$: Matrix-power exponent in the error norm **Domain:** $\alpha\in\mathbb R$.

$\|z\|_{A^\alpha}=(z^*A^\alpha z)^{1/2}$

$A$: The hidden matrix is Hermitian positive definite and has at least t + 1 distinct eigenvalues. **Domain:** $\mathbb C^{d\times d}$.

$b$: Public nonzero initial vector **Domain:** $\mathbb C^d\setminus\{0\}$.

$h$: A public function with $h$ or $z\mapsto h(z)/z$ in the Stieltjes class. **Domain:** Scalar function on the positive real axis.

$\nu,s$: Positive measure and integration variable in the Stieltjes representation. **Domain:** $s\ge0,\ \int_0^\infty(1+s)^{-1}\,d\nu(s)<\infty$.

Either $h(z)$ or $h(z)/z$ equals $\int_0^\infty(z+s)^{-1}\,d\nu(s)$; MODEL specifies the function class.

$\mathcal K_t(A,b)$: Order-t Krylov subspace **Domain:** A linear subspace of $\mathbb C^d$.

$\mathcal K_t(A,b)=\operatorname{span}\{b,Ab,\ldots,A^{t-1}b\}$

$V_t,T_t$: Orthonormal basis matrix of the Krylov subspace and the compressed Hermitian matrix **Domain:** Use the actual subspace dimension if exact termination occurs early.

$V_t^*V_t=I,\quad T_t=V_t^*AV_t$

$y_t$: Function approximation by a fixed Lanczos algorithm. **Domain:** $\mathbb C^d$.

$y_t=V_t h(T_t)V_t^*b$

$\|z\|_{A^\alpha}$: Weighted vector norm defined by a power of the input matrix **Domain:** A nonnegative real.

$\|z\|_{A^\alpha}=(z^*A^\alpha z)^{1/2}$

$\mathcal C$: Ratio of fixed-Lanczos error to the best error in the same Krylov space. **Domain:** $[0,\infty]$, with the convention $0/0=1$.

$\mathcal C=\frac{\|h(A)b-y_t\|_{A^\alpha}}{\min_{y\in\mathcal K_t(A,b)}\|h(A)b-y\|_{A^\alpha}}$

$E$: Exponent in the sharp approximation factor **Domain:** $E\ge1/2$.

$E=\max\{\alpha,1-\alpha\}$

$\zeta$: An arbitrary relative slack approaching the supremal worst-case factor. **Domain:** $0<\zeta\le1$.

$N$: The exact matrix–vector product count of the fixed algorithm. **Domain:** $\mathbb N_0$.

$N\le t$

$(\cdot)^*$: Conjugate transpose **Domain:** Complex matrix or vector.

$\lambda_i(A)$: Eigenvalues of a real symmetric or Hermitian matrix in nonincreasing order. **Domain:** $1\le i\le d$.

$\lambda_1(A)\ge\cdots\ge\lambda_d(A)$

$\|z\|_2$: Euclidean norm of a vector **Domain:** Finite-dimensional real or complex vector.

$\|z\|_2=(\sum_i|z_i|^2)^{1/2}$

## 3. Complexity bracket

### Compared quantities

#### Q1 - fixed budget risk

$$
\sup_{A,h,b}C\!\left(h,A,b,t,\|\cdot\|_{A^\alpha}\right)
$$

**Scope.** The algorithm is fixed to exact single-start Lanczos-FA. For the given d, κ, t, and α, take the supremum of the error approximation factor over all admissible A, h, and b. There is no infimum over algorithms and no conversion to minimum query complexity at a prescribed tolerance.

**Optimization direction.** minimize

### R1 - Nondegenerate Lanczos approximation factor

**Region.** Assume $\kappa>1$, integers $t\ge1$ and $d\ge t+1$, and $\alpha\in\mathbb{R}$. The input matrix has at least $t+1$ distinct eigenvalues.

**Quantity.** Q1

**Resource.** Worst-case approximation factor of the fixed algorithm over admissible inputs.

**Status.** Optimal

**Lower bound.** B2

$$
\frac12(\kappa^{E/2}+\kappa^{-E/2}),\quad E=\max\{\alpha,1-\alpha\}
$$

**Upper bound.** B1

$$
\frac12(\kappa^{E/2}+\kappa^{-E/2}),\quad E=\max\{\alpha,1-\alpha\}
$$

**Gap or comparison.** $0$

**Comparison argument.** For the fixed Lanczos algorithm, the instancewise upper factor is attained arbitrarily closely by worst-case inputs. The dimensionless approximation factor is sharp; this is not query optimality over general algorithms.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact $Av$ access for a complex Hermitian positive definite matrix. Queries follow the fixed single-start Lanczos recurrence initialized at public $b$; they are not chosen by a general algorithm.

**Guarantee mapping.** Fully deterministic. The upper bound holds for every instance. For a suitable A, the lower bound provides h and b achieving any factor 1-eta; letting eta tend to zero gives a supremum, without claiming equality on every instance.

**Output mapping.** The output must be the fixed Lanczos-FA value f_t. Compare its A^α-norm error with the minimum error in the same K_t(A,b), using the convention 0/0 = 1.

**Resource mapping.** The native comparison quantity is the dimensionless approximation factor $\mathcal C$, not the minimum query count needed for a tolerance. The algorithm uses at most $t$ exact matrix–vector products. Internal arithmetic and scalar function evaluations are free.

### B1 - Per-input approximation-factor upper bound for the fixed exact Lanczos algorithm

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{C}\le \frac{1}{2}(\kappa^{E/2}+\kappa^{-E/2}),\quad E=\max\{\alpha,1-\alpha\}
$$

**Sources.** [1](https://arxiv.org/pdf/2608.07160v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** t

**factor.**

$$
\frac12(\kappa^{E/2}+\kappa^{-E/2}),\quad E=\max\{\alpha,1-\alpha\}
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://arxiv.org/pdf/2608.07160v1) theorem: Theorems 1 and 2; section: §1.2; pdf pages: 3; 4; equations: (4); (6)

Let $S=\{h:h\text{ or }h/z\text{ is Stieltjes}\}$. For each $A$ with at least $t+1$ eigenvalues and condition number $\kappa$, suitable $h,b$ attain any prescribed fraction $1-\eta$ in the lower bound.

### B2 - A worst-case function and starting vector for fixed Lanczos.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** The stated restricted deterministic class

$$
\sup\mathcal{C}\ge \frac{1}{2}(\kappa^{E/2}+\kappa^{-E/2}),\quad E=\max\{\alpha,1-\alpha\}
$$

**Sources.** [1](https://arxiv.org/pdf/2608.07160v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N right.** t

**factor.**

$$
\frac12(\kappa^{E/2}+\kappa^{-E/2}),\quad E=\max\{\alpha,1-\alpha\}
$$

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Derivation.** For each $0<\zeta\le1$, Theorem 2 supplies an admissible input attaining the stated factor times $(1-\zeta)$. Letting $\zeta\downarrow0$ gives the lower bound on the supremum approximation ratio. A finite instance need not attain the supremum exactly.

**Source location.** [1](https://arxiv.org/pdf/2608.07160v1) theorem: Theorems 1 and 2; section: §1.2; pdf pages: 3; 4; equations: (4); (6)

Let $S=\{h:h\text{ or }h/z\text{ is Stieltjes}\}$. For each $A$ with at least $t+1$ eigenvalues and condition number $\kappa$, suitable $h,b$ attain any prescribed fraction $1-\eta$ in the lower bound.

## References

[1] Tyler Chen; David Persson. Optimal near-optimality bounds for the Lanczos method for matrix functions. 2026. arXiv:2608.07160v1; 2026-08-07.

https://arxiv.org/pdf/2608.07160v1
