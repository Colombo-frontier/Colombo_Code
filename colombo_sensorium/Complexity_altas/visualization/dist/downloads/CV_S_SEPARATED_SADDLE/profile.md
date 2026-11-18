# Bilinearly coupled saddle-point problems: separate block gradients and matrix products

**Setting ID.** `CV_S_SEPARATED_SADDLE`

Matrix computation

$$
\min_{x\in\mathbb{R}^{d_x}}\max_{y\in\mathbb{R}^{d_y}}a(x)+y^\top Bx-b(y).
$$

**Status.** Logarithmic gap present

**TASK tags.** formulation: Bilinearly coupled saddle; solution concept: Weighted squared distance; task family: Matrix computation; task family: Minimax; task family: Saddle point

**MODEL tags.** convexity: Smooth strongly convex; initialization: Initial distance; spectral structure: Spectral norm bound; structure: Separable bilinear

**ORACLE tags.** feedback quality: Exact; interface family: Separate gradient matvec; operation: Block gradient; operation: Matrix left matvec; operation: Matrix right matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: Linear span

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal dual pair; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Weighted squared distance

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** measure: N b; measure: N f; measure: N g; precision: Bit precision not counted

## 1. Setting specification

### Task

$$
\min_{x\in\mathbb{R}^{d_x}}\max_{y\in\mathbb{R}^{d_y}}a(x)+y^\top Bx-b(y).
$$

### Admissible model

The function $a$ is $\mu_x$-strongly convex and $\beta_x$-smooth; $b$ is $\mu_y$-strongly convex and $\beta_y$-smooth. These conditions hold on the respective full Euclidean spaces.

Assume $B\in\mathbb{R}^{d_y\times d_x}$ and $\|B\|_{\rm op}\le\beta_{xy}$. A positive smallest singular value is not promised. The unique saddle point $(x^\star,y^\star)$ exists.

The initial point satisfies $\mu_x\|x_0-x^\star\|_2^2+\mu_y\|y_0-y^\star\|_2^2\le R^2$.

### Oracle interface

Dimensions, domains, initial point, tolerance, and parameters marked public are supplied before querying. Analytic representations of the hidden functions or operators are not disclosed.

$$
x\mapsto\nabla a(x),\quad y\mapsto\nabla b(y),\quad v\mapsto Bv,\quad u\mapsto B^\top u.
$$

Every interface is exact. The quantities $a,b,B$ are hidden; left and right matrix products may be chosen separately. No proximal mapping or linear-system solve is supplied.

### Output

Return $(\widehat{x},\widehat{y})\in\mathbb{R}^{d_x+d_y}$ subject to the stated memory-subspace restriction; no additional certificate is required.

### Loss or accuracy criterion

$$
\mu_x\|\widehat{x}-x^\star\|_2^2+\mu_y\|\widehat{y}-y^\star\|_2^2.
$$

### Resource accounting

Retain joint budget $(N_f,N_g,N_B)$, with both multiplication directions included in $N_B$. Given public costs $\tau_f,\tau_g,\tau_B>0$, compare $\tau_fN_f+\tau_gN_g+\tau_BN_B$.

Sequential-call model. All resource upper bounds must be attained jointly by one algorithm with one parameter choice.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Use the deterministic block-memory class in Borodich et al., Definition 3.1. New queries and outputs lie in the maintained blockwise memory subspaces, which are updated by the prescribed gradients and matrix actions. The lower bound does not cover arbitrary nonlinear query algorithms.

The same deterministic algorithm must satisfy the guarantee for every admissible instance.

$$
\mu_x\|\widehat{x}-x^\star\|_2^2+\mu_y\|\widehat{y}-y^\star\|_2^2\le\varepsilon.
$$

**Budget convention.** sequential total time tau_f N_f+tau_g N_g+tau_B N_B

## 2. Notation and parameters

$d_x$: The primal-block dimension. **Domain:** $d_x\in\mathbb N$.

$x\in\mathbb R^{d_x}$

$d_y$: Dual-block dimension **Domain:** $d_y\in\mathbb N$.

$y\in\mathbb R^{d_y}$

$d$: Sum of the two block dimensions; complexity takes the worst case over all admissible finite dimensions. **Domain:** $d=d_x+d_y,\ d_x,d_y\in\mathbb N$.

$d=d_x+d_y$

$\varepsilon$: The tolerance for final curvature-weighted squared distance. **Domain:** $\varepsilon>0$.

$\mu_x\|\widehat x-x^\star\|_2^2+\mu_y\|\widehat y-y^\star\|_2^2\le\varepsilon$

$R^2$: Public bound on the initial curvature-weighted squared distance **Domain:** $R^2>0$.

$\mu_x\|x_0-x^\star\|_2^2+\mu_y\|y_0-y^\star\|_2^2\le R^2$

$\beta_x$: Upper bound on the Euclidean gradient Lipschitz constant of the hidden function $ a $ **Domain:** $\beta_x\ge\mu_x>0$.

$\|\nabla a(u)-\nabla a(v)\|_2\le\beta_x\|u-v\|_2$

$\beta_y$: A Euclidean Lipschitz bound on the gradient of the hidden function $ b $. **Domain:** $\beta_y\ge\mu_y>0$.

$\|\nabla b(u)-\nabla b(v)\|_2\le\beta_y\|u-v\|_2$

$\beta_{xy}$: Spectral norm bound on the bilinear coupling matrix **Domain:** $\beta_{xy}>0$.

$\|B\|_{\rm op}\le\beta_{xy}$

$\mu_x$: Lower bound on the strong convexity constant of the hidden function $a$ **Domain:** $\mu_x>0$.

$a(u)\ge a(v)+\langle\nabla a(v),u-v\rangle+\frac{\mu_x}2\|u-v\|_2^2$

$\mu_y$: Lower bound on the strong convexity constant of the hidden function $b$ **Domain:** $\mu_y>0$.

$b(u)\ge b(v)+\langle\nabla b(v),u-v\rangle+\frac{\mu_y}2\|u-v\|_2^2$

$\kappa_x$: The primal-block condition number. **Domain:** $\kappa_x,\kappa_y\ge1$.

$\beta_x/\mu_x$

$\kappa_y$: Condition number of the dual-variable block **Domain:** $\kappa_x,\kappa_y\ge1$.

$\beta_y/\mu_y$

$\kappa_{xy}$: Dimensionless squared coupling scale **Domain:** $\kappa_{xy}>0$.

$\beta_{xy}^2/(\mu_x\mu_y)$

$\tau_f$: The public time cost of one $\nabla a$ call. **Domain:** Positive real number.

$\tau_g$: Public time cost of one call to $\nabla b$ **Domain:** Positive real number.

$\tau_B$: Public time cost of one $Bv$ or $B^{\mathsf T}u$ call **Domain:** Positive real number.

$a,b$: The two hidden separable strongly convex functions. **Domain:** $a:\mathbb R^{d_x}\to\mathbb R,\ b:\mathbb R^{d_y}\to\mathbb R$.

$B$: Hidden bilinear coupling matrix **Domain:** $\mathbb R^{d_y\times d_x}$.

$f$: The bilinearly coupled payoff function. **Domain:** $\mathbb R^{d_x}\times\mathbb R^{d_y}\to\mathbb R$.

$f(x,y)=a(x)+y^{\mathsf T}Bx-b(y)$

$\Phi$: Primal value function obtained by global maximization over the dual variable **Domain:** $\mathbb R^{d_x}\to\mathbb R$.

$\Phi(x)=a(x)+\sup_{y\in\mathbb R^{d_y}}\{y^{\mathsf T}Bx-b(y)\}$

$F$: Saddle-point operator defined by the payoff function **Domain:** $\mathbb R^{d_x+d_y}\to\mathbb R^{d_x+d_y}$.

$F(x,y)=(\nabla a(x)+B^{\mathsf T}y,\ \nabla b(y)-Bx)$

$x^\star,y^\star$: Two variable blocks of the unique saddle point **Domain:** $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$\nabla a(x^\star)+B^{\mathsf T}y^\star=0,\quad \nabla b(y^\star)-Bx^\star=0$

$y^\star(x)$: The unique dual maximizer at fixed primal x. **Domain:** $\mathbb R^{d_y}$.

$y^\star(x)=\arg\min_y\{b(y)-y^{\mathsf T}Bx\}$

$x_0,y_0$: Public initial point **Domain:** $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$\widehat x,\widehat y$: Two variable blocks returned by the algorithm **Domain:** $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$N_f,N_g,N_B$: Count ∇a, ∇b, and Bv/Bᵀu calls separately. **Domain:** $\mathbb N_0^3$.

$Q^\star(\varepsilon)$: Minimum worst-case weighted time to accuracy epsilon within the block-memory algorithm class **Domain:** Nonnegative extended real value.

$\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I(\tau_fN_f+\tau_gN_g+\tau_BN_B)$

$\mathfrak A_\varepsilon$: Deterministic algorithms obeying the stated block-memory restrictions and error guarantee **Domain:** Algorithm class.

$R$: The nonnegative square root of the public initial squared scale R². **Domain:** Positive real number.

$R=\sqrt{R^2}$

$c$: The small-accuracy window constant in the source lower bound. **Domain:** A fixed positive universal constant.

$0<\varepsilon<cR^2/e$

$e$: Base of the natural logarithm **Domain:** A fixed mathematical constant.

$\|z\|_2$: Euclidean norm of a vector **Domain:** Finite-dimensional real or complex vector.

$\|z\|_2=(\sum_i|z_i|^2)^{1/2}$

$\|M\|_{\mathrm{op}}$: The matrix operator norm induced by the Euclidean norm. **Domain:** Any compatible matrix.

$\|M\|_{\mathrm{op}}=\max_{\|z\|_2=1}\|Mz\|_2=\sigma_1(M)$

$\langle u,v\rangle$: Euclidean inner product **Domain:** Real vector of the same dimension.

$\langle u,v\rangle=u^{\mathsf T}v$

$\log$: Natural logarithm **Domain:** Positive real argument.

$\log x=\ln x$

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
Q^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I(\tau_fN_f+\tau_gN_g+\tau_BN_B)
$$

**Scope.** worst case over every finite dimension, unless a stated theorem window supplies d; no fixed-d saturation inferred

**Optimization direction.** minimize

Take the infimum over deterministic block-memory algorithms satisfying the weighted squared-distance guarantee. Cost uses the three public operation weights, and the worst case ranges over all admissible finite-dimensional inputs.

### R1 - The source theorem’s applicability window.

**Region.** $\beta_x>4\mu_x,\ \beta_y>4\mu_y,\ \beta_{xy}>18\sqrt{\mu_x\mu_y},\ 0<\varepsilon<cR^2/e$

**Quantity.** Q1

**Resource.** Weighted query cost $\tau_fN_f+\tau_gN_g+\tau_BN_B$.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega((\tau_f\sqrt{\kappa_x}+\tau_g\sqrt{\kappa_y}+\tau_B\sqrt{\kappa_{xy}})\log(cR^2/\varepsilon))
$$

**Upper bound.** B1

$$
O((\tau_f\sqrt{\kappa_x}+\tau_g\sqrt{\kappa_y}+\tau_B\sqrt{\kappa_{xy}})\log((1+12\kappa_x+12\kappa_y)R^2/\varepsilon))
$$

**Gap or comparison.** $O(1+\log(1+\kappa_x+\kappa_y)/\log(cR^2/\varepsilon))$

**Comparison argument.** Both formulas refer to the same weights and a single achievable vector. Expanded log in upper depends on conditioning, so joint-parameter constant-factor closure is not asserted.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - restarted multi-level accelerated algorithm; one joint schedule

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Block gradients and matrix actions in the restarted multilevel accelerated method follow a fixed schedule and the source memory-subspace model.

$$
O((\tau_f\sqrt{\kappa_x}+\tau_g\sqrt{\kappa_y}+\tau_B\sqrt{\kappa_{xy}})\log((1+12\kappa_x+12\kappa_y)R^2/\varepsilon))
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v267/main/assets/borodich25a/borodich25a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N f.**

$$
O(\sqrt{\kappa_x}\log((1+12\kappa_x+12\kappa_y)R^2/\varepsilon))
$$

**N g.**

$$
O(\sqrt{\kappa_y}\log((1+12\kappa_x+12\kappa_y)R^2/\varepsilon))
$$

**N B.**

$$
O(\sqrt{\kappa_{xy}}\log((1+12\kappa_x+12\kappa_y)R^2/\varepsilon))
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v267/main/assets/borodich25a/borodich25a.pdf) theorem: Theorem3.3, Corollary4.8, Assumptions2.6--2.7; section: Sections2--4; pdf pages: 5; 6; 8

This profile sets both minimum-singular-value promises for the source coupling matrix to zero, retaining only its spectral-norm bound. The richer spectral family is recorded as additional applicability. Both initialization logarithms and all three operation costs remain explicit.

### B2 - time-indexed first-order block memory hard family

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** The stated restricted deterministic class

**Algorithm-scope qualification.** The lower bound relies on zero-respecting or block-memory linear-span restrictions. This view requires only deterministic algorithms.

$$
\Omega((\tau_f\sqrt{\kappa_x}+\tau_g\sqrt{\kappa_y}+\tau_B\sqrt{\kappa_{xy}})\log(cR^2/\varepsilon))
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v267/main/assets/borodich25a/borodich25a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**weighted time constraint.**

$$
\Omega((\tau_f\sqrt{\kappa_x}+\tau_g\sqrt{\kappa_y}+\tau_B\sqrt{\kappa_{xy}})\log(cR^2/\varepsilon))
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v267/main/assets/borodich25a/borodich25a.pdf) theorem: Theorem3.3, Corollary4.8, Assumptions2.6--2.7; section: Sections2--4; pdf pages: 5; 6; 8

This profile sets both minimum-singular-value promises for the source coupling matrix to zero, retaining only its spectral-norm bound. The richer spectral family is recorded as additional applicability. Both initialization logarithms and all three operation costs remain explicit.

## References

[1] Ekaterina Borodich; Alexander Gasnikov; Dmitry Kovalev. On Linear Convergence in Smooth Convex-Concave Bilinearly-Coupled Saddle-Point Optimization: Lower Bounds and Optimal Algorithms. 2025. ICML, PMLR267:5045--5100.

https://raw.githubusercontent.com/mlresearch/v267/main/assets/borodich25a/borodich25a.pdf
