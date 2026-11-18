# Nonconvex first-order stationarity with Hessian–vector products

**Setting ID.** `SO_HO_HOI04_S_rand`

Single-objective optimization

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

**Status.** Polynomial gap present; Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Gradient hvp; operation: Gradient hvp; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is $C^2$ and bounded below; nonconvexity is allowed.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

$$\|D^{2}f(x)-D^{2}f(y)\|_{\mathrm{op},2}\le M_2\|x-y\|_{2}.$$

The gradient satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$.

Admissible parameter domain:

$$0<\varepsilon_g\le c\min\{\beta^2/M_2,\Delta^{2/3}M_2^{1/3}\},\quad\beta,M_2,\Delta>0$$

### Oracle interface

Two separately charged queries are available: at $x$, obtain exact $(f(x),\nabla f(x))$; at a point and direction $(x,v)$, obtain exact $\nabla^2f(x)v$, with $v\in\mathbb{R}^d$. A directional query returns one vector.

The public inputs are $x_0$, the target accuracy, and $d$, $\varepsilon_g$, $\beta$, $M_2$, $\Delta$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\|\nabla f(\widehat{x})\|_2.$$

The criterion uses the gradient norm itself. Squared norms, expectations, and probability guarantees are recorded separately and are not substituted automatically.

### Resource accounting

Each joint exact value-and-gradient response or single-direction Hessian–vector product costs one unit. Recovering a matrix using $d$ basis vectors requires $d$ directional queries.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\|\nabla f(\widehat{x})\|_2\le \varepsilon_g\right]\ge\frac23.$$

Expectation or probability is evaluated after fixing the instance; randomness comes from the algorithm's private random seed.

The running-cost guarantee is specified separately under RESOURCE.

## 2. Notation and parameters

$x,\widehat{x},x_0$: Query or decision point, algorithm output, and public initial point. **Domain:** $\mathbb{R}^d$.

$\mathbb{R}^d$: Real coordinate space; vectors use the Euclidean norm unless otherwise stated. **Domain:** $d$ is a positive integer.

$\langle u,v\rangle,\ \|u\|_2$: Euclidean inner product and norm.

$$\langle u,v\rangle=u^\top v,\qquad\|u\|_2=\sqrt{\langle u,u\rangle}.$$

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,2\}$ and $D^0f=f$.

$\|T\|_{\mathrm{op}},\ \|T\|_{\mathrm{op},2}$: Induced operator norm of a Euclidean multilinear tensor; the spectral norm for matrices.

$$\|T\|_{\mathrm{op}}=\|T\|_{\mathrm{op},2}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|.$$

$\mathcal{E}$: Base error defined in the metric specification; expectation or probability aggregation is imposed by the guarantee.

$N$: Total number of original oracle calls; the unit cost is specified in the resource convention. **Domain:** $N\in\mathbb{Z}_{\ge0}$.

$T^*$: Minimum worst-case budget for one algorithm to meet the requirement on the full instance class, within the specified regime, guarantee and resource projection. Expected-resource specifications instead minimize the per-instance expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching bounds up to constants, and upper bounds omitting the declared logarithmic factors. **Domain:** Hidden constants, fixed parameters, and omitted logarithmic variables are specified for each bound.

$\inf,\sup,\min,\max$: Infimum, supremum, attained minimum and attained maximum.

$c,C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<c,C<\infty$.

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\varepsilon_g$: Target accuracy **Domain:** $\varepsilon_g>0$.

$\beta$: Gradient Lipschitz budget **Domain:** $\beta>0$.

$M_2$: Hessian Lipschitz bound **Domain:** $M_2>0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$c$: Sufficiently small tolerance constant **Domain:** $0<c<1$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each exact value/gradient reply or directional HVP costs one call; internal computation is unrestricted.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each exact value/gradient reply or directional HVP costs one call; internal computation is unrestricted.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Common small-accuracy window

**Region.** $0<\varepsilon_g\le c\min\{\beta^2/M_2,\Delta^{2/3}M_2^{1/3}\},\quad\beta,M_2,\Delta>0$

**Quantity.** Q1

**Resource.** Each exact value/gradient reply or directional HVP costs one call; internal computation is unrestricted.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(1+\Delta\beta^{1/2}M_2^{1/4}\varepsilon_g^{-7/4})
$$

### R2 - Compatibility window for the randomized lower-bound construction

**Region.** $\Theta_0\cap\{d\ge d_0(\beta,M_2,\Delta,\varepsilon_g)\}$

**Quantity.** Q2

**Resource.** Each exact value/gradient reply or directional HVP costs one call; internal computation is unrestricted.

**Status.** Polynomial gap

**Lower bound.** B2

$$
\Omega(\Delta M_2^{1/2}\varepsilon_g^{-3/2})
$$

**Upper bound.** B1

$$
O(\Delta\beta^{1/2}M_2^{1/4}\varepsilon_g^{-7/4})
$$

**Gap or comparison.** $O(\beta^{1/2}M_2^{-1/4}\varepsilon_g^{-1/4})$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Two separately charged queries are available: at $x$, obtain exact $(f(x),\nabla f(x))$; at a point and direction $(x,v)$, obtain exact $\nabla^2f(x)v$, with $v\in\mathbb{R}^d$. A directional query returns one vector.

**Guarantee mapping.** Success probability at least 2/3 for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each joint exact value-and-gradient response or single-direction Hessian–vector product costs one unit. Recovering a matrix using $d$ basis vectors requires $d$ directional queries.

### B1 - Accelerated nonconvex method with approximate Hessians

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
1+\Delta\beta^{1/2}M_2^{1/4}\varepsilon_g^{-7/4}
$$

**Sources.** [1](https://proceedings.nips.cc/paper_files/paper/2025/file/3dc910c921507a5d51d3dac0202b2618-Paper-Conference.pdf) [2](https://arxiv.org/abs/1710.11606v3) [3](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $0<\varepsilon_g\le c\min\{\beta^2/M_2,\Delta^{2/3}M_2^{1/3}\},\quad\beta,M_2,\Delta>0$

**Dimension conditions.** $0<\varepsilon_g\le c\min\{\beta^2/M_2,\Delta^{2/3}M_2^{1/3}\},\quad\beta,M_2,\Delta>0$

**Local argument.** A1, A2, A3

**Source location.** [1](https://proceedings.nips.cc/paper_files/paper/2025/file/3dc910c921507a5d51d3dac0202b2618-Paper-Conference.pdf) theorem: Theorem 1 and gradient-only consequence, PDF pp. 2–3; pdf pages: 3

### B2 - Transfer from full-Hessian hard instances to the Hessian-vector interface

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Delta M_2^{1/2}\varepsilon_g^{-3/2}
$$

**Sources.** [2](https://arxiv.org/abs/1710.11606v3) [3](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $\Theta_0\cap\{d\ge d_0(\beta,M_2,\Delta,\varepsilon_g)\}$

**Dimension conditions.** $\Theta_0\cap\{d\ge d_0(\beta,M_2,\Delta,\varepsilon_g)\}$

**Local argument.** A1, A2, A3

**Source location.** [2](https://arxiv.org/abs/1710.11606v3) theorem: Theorem 2. The joint-regularity scaling and transfer to HVP access are derived in the local arguments “Simultaneous regularity budgets and common lower-bound scaling” and “Direction of transfer between complete jets and HVPs”.

## 5. Local arguments

### A1 - Direction of transfer between complete jets and HVPs

**Scope.** Information simulation only; all regularity, guarantee, dimension, and query-domain conditions remain in force.

**Algorithm scope.** Information simulation only; all regularity, guarantee, dimension, and query-domain conditions remain in force.

A complete jet simulates an HVP action at the same point with at most one query; lower bounds transfer from the stronger jet interface to the weaker HVP interface.

For each action of a T-call HVP algorithm, query one complete jet at that action's point and compute the requested Hessian–vector product or return its requested value/gradient portion by free internal arithmetic. The transcript, output, and success probability are unchanged and the cost is at most T. Consequently a lower bound for complete jets also constrains HVP algorithms. The reverse implication is generally invalid because complete Hessians contain more information.

The target model must also contain the source hard family. In particular, a highest-order $M_2$-only hard construction need not satisfy every arbitrarily small $\beta$-smoothness budget. Where multiple budgets are imposed, retain the fixed positive scales, small-accuracy window, and sufficient dimension required by the common-scaling argument.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [2](https://arxiv.org/abs/1710.11606v3)

### A2 - Simultaneous regularity budgets and common lower-bound scaling

**Scope.** Jointly declared positive regularity budgets. Deterministic and randomized lower bounds retain their distinct sufficient dimensions and source scope.

**Algorithm scope.** Jointly declared positive regularity budgets. Deterministic and randomized lower bounds retain their distinct sufficient dimensions and source scope.

For jointly bounded derivative Lipschitz moduli, the first-order scale is $A=\Delta\min_{1\le j\le k}M_j^{1/j}\varepsilon_g^{-(j+1)/j}$, with $M_1=\beta$.

For each fixed j, use the jth-order regularized method, reading only the relevant part of the complete k-jet. Its budget is $C_j[1+\Delta M_j^{1/j}\varepsilon_g^{-(j+1)/j}]$. All parameters are public, so an algorithm may select the smallest proved budget. This minimum is an envelope of complete algorithms.

For the lower bound, use the robust CDHS smooth chain $h_N$, whose initial gap is at most $C_kN$, whose gradient stays bounded away from zero before completion, and whose jth-derivative Lipschitz modulus is at most a constant $\ell_j$ depending only on j. Set $f(x)=a h_N(x/b)$ with
$$a/b=K_k\varepsilon_g,\qquad
b=\max_{1\le j\le k}(K_k\ell_j\varepsilon_g/M_j)^{1/j}.$$
Then $\operatorname{Lip}(D^jf)=a\ell_j/b^{j+1}\le M_j$ for every j simultaneously. Choosing N proportional to $\Delta/a$ gives N of order A. For A above a fixed k-dependent threshold, deterministic resisting rotations fit in $d\ge C_k(1+A)$; the classical randomized radial construction fits in $d\ge C_k(1+A)^2\log(3+A)$. These are sufficient dimensions.

If the primary result is stated as time to query a successful point, append one complete-jet query at the algorithm's final output. A lower bound of N then gives an original-budget lower bound N-1, of the same order in the nontrivial A region. This handles arbitrary unqueried outputs without changing the success quantifier.

For $k=2$, the common scaling gives $A=\Delta\min\{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}\}$. Keep the zero-query region $\varepsilon_g^2\ge2\beta\Delta$ separate; the whole domain is not uniformly Theta(1+A). Dimension improvements proved for a highest-order-only model do not automatically preserve all lower-order budgets.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [2](https://arxiv.org/abs/1710.11606v3)

### A3 - High-order regularized descent with full parameter dependence

**Scope.** Fixed derivative order, complete exact jets, full-space queries, bounded initial gap, and free global known-model solution. Zero modulus is treated by polynomial recovery.

**Algorithm scope.** Fixed derivative order, complete exact jets, full-space queries, bounded initial gap, and free global known-model solution. Zero modulus is treated by polynomial recovery.

With a Lipschitz kth derivative and fixed $k\ge2$, first-order stationarity uses $O_k(1+\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k})$ complete jets.

At x, form $m_x(s)=T_k(f;x,s)+a_kM_k\|s\|^{k+1}$, choosing $a_k$ sufficiently large, depending only on k, to dominate the Taylor remainder with slack. For $M_k>0$ the model is coercive, so it has a global minimizer, available under the declared free internal computation. Comparing the model at s and zero and applying the value remainder gives
$$f(x)-f(x+s)\ge c_kM_k\|s\|^{k+1}.$$
Model first-order optimality and the gradient remainder give
$$\|\nabla f(x+s)\|\le C_kM_k\|s\|^k.$$
If the next point is not $\varepsilon_g$-stationary, the decrease is at least $c_kM_k^{-1/k}\varepsilon_g^{(k+1)/k}$. The total decrease is at most $\Delta$, so after the displayed number of calls, including initialization and final verification, stationarity is reached.

This is the parameter restoration of the regularized-model argument in BGMST17, Lemmas 2.1–2.3 and Theorem 2.5. Its normalization is $(k-1)!L=M_k$. Separate function and derivative evaluations in the source cost only a fixed multiple when complete jets are charged as one. The argument is about information calls and does not assert an inexpensive arithmetic implementation of global nonconvex model minimization.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [3](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

## References

[1] Deeksha Adil, Brian Bullins, Aaron Sidford, Chenyi Zhang. Balancing Gradient and Hessian Queries in Non-Convex Optimization. NeurIPS 2025 final conference PDF.

https://proceedings.nips.cc/paper_files/paper/2025/file/3dc910c921507a5d51d3dac0202b2618-Paper-Conference.pdf

[2] Yair Carmon, John C. Duchi, Oliver Hinder, Aaron Sidford. Lower Bounds for Finding Stationary Points I. arXiv:1710.11606v3; Mathematical Programming 184 (2020).

https://arxiv.org/abs/1710.11606v3

[3] E. G. Birgin; J. L. Gardenghi; J. M. Martínez; S. A. Santos; Ph. L. Toint. Worst-case evaluation complexity for unconstrained nonlinear optimization using high-order regularized models. NAXYS-05-2015, 2015-07-10; Mathematical Programming 163 (2017), 359–368.

https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf
