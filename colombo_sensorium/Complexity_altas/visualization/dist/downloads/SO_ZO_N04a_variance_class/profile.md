# Quadratic objective with known Hessian: independent value noise on a ball; finite-variance noise class

**Setting ID.** `SO_ZO_N04a_variance_class`

Single-objective optimization

Estimate the minimizer of a quadratic objective from noisy values queried in a bounded ball, measuring the global quadratic objective gap at the output.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Quadratic smoothness; structure: Quadratic objective

**ORACLE tags.** access order: Zeroth-order interface; interface family: Independent noisy value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Quadratic energy loss

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Estimate the minimizer of a quadratic objective from noisy values queried in a bounded ball, measuring the global quadratic objective gap at the output.

### Admissible model

$f(x)=\frac12(x-x_*)^\top A(x-x_*)$, where $A\in\mathbb{R}^{d\times d}$ is symmetric positive semidefinite and the center $x_*\in B_2(0,R)$ is unknown. The function is defined throughout the ambient space and has minimum value zero.

The matrix $A$ may be singular; only the component of the center in $\operatorname{range}(A)$ must then be estimated. Whether the matrix, spectrum and center are known is fixed by the Oracle interface.

### Oracle interface

A query at $x_t\in B_2(0,R)$ returns one scalar $Y_t=f(x_t)+\xi_t$.

$\xi_t$ is i.i.d. centered noise with $\mathbb{E}\xi_t^2\le\sigma_v^2$, independent of the algorithmic seed and preceding observations. Its distribution is unknown; the algorithm must cover every noise law satisfying the stated bound.

Every observation is charged independently. No same-sample coupling, sample handle, or noiseless function value is supplied.

The entire matrix $A$ is public. The algorithm may therefore depend on its rank, eigenvalues, and eigenspaces; the center $x_*$ is hidden.

The public inputs are $d$, $R$, $\sigma_v$, $\varepsilon$, $T$, $A$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in B_2(0,R)$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=\frac12(x-x_*)^\top A(x-x_*)=\frac12\|x-x_*\|_A^2$; it remains finite and nonnegative even when $A$ is singular.

For fixed known matrix $A$ and budget $T$, $r_T(A)=\inf_{\mathcal{A}_A:N\le T}\sup_{\|x_*\|_2\le R}\mathbb{E}[\ell(I,\widehat{x})]$. The variance-class model takes an additional supremum over admissible noise laws after the supremum over centers; the Gaussian model fixes the noise law.

### Resource accounting

Each scalar function value or noisy observation costs $1$ call. Every location in a multipoint finite difference, every initialization query, and every reference observation is charged.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. Require $\mathbb{E}[\ell(I,\widehat{x})]\le \varepsilon$, fixing the instance before averaging over algorithmic and feedback randomness.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$R$: Radius of the unknown-center localization ball and of the query/output ball **Domain:** $R>0$.

$x_*,x_t,\widehat{x}\in B_2(0,R)$

$\sigma_v$: Upper bound on scalar observation-noise scale **Domain:** $\sigma_v\ge0$.

$\mathbb{E}\xi^2\le\sigma_v^2$; conditional-variance assumptions are interpreted with respect to the specified interaction history.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$T$: Known query budget or argument of the risk curve **Domain:** $T\in\mathbb{N}_0$.

Use $N\le T$ in the fixed-budget specification and $\mathbb{E}[N]\le T$ in the expected-budget specification.

$A$: Hessian of the quadratic objective **Domain:** $A=A^\top\succeq0,\ A\in\mathbb{R}^{d\times d}$.

$r$: Hessian rank **Domain:** $r\in\{0,\ldots,d\}$.

$r=\operatorname{rank}(A)$

$\lambda_i$: Positive Hessian eigenvalues, with a trailing-zero convention **Domain:** $\lambda_1\ge\cdots\ge\lambda_r>0$.

$\lambda_{r+1}=0$; the positive spectrum is empty when $r=0$.

$S_k$: Sum of inverse square roots of the leading positive eigenvalues **Domain:** $k\in\{0,\ldots,r\}$.

$S_k=\sum_{i=1}^k\lambda_i^{-1/2}$, $S_0=0$.

$J_k$: Sum of the $-3/2$ powers of the leading positive eigenvalues **Domain:** $k\in\{0,\ldots,r\}$.

$J_k=\sum_{i=1}^k\lambda_i^{-3/2}$, $J_0=0$.

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $B_2(0,R)$.

$I$: Complete problem instance **Domain:** $I\in\mathcal{I}$.

Includes the unknown objective and its admissible feedback distribution or environment law. Public parameters are fixed before the quantifiers.

$\mathcal{I}$: Admissible instance class determined by the eight specification fields in this profile **Domain:** Instances satisfying the public parameter bounds.

$\mathcal{A}$: Algorithm or strategy **Domain:** Measurable adaptive strategies allowed in this profile.

The algorithm is selected before the hidden instance.

$\ell$: Base loss or residual **Domain:** $\ell:\mathcal{I}\times\mathcal{X}_{\mathrm{out}}\to[0,+\infty]$.

The exact formula appears in this profile's performance-criterion section.

$\mathbb{E},\Pr$: Expectation and probability **Domain:** Evaluated over the algorithmic and feedback randomness specified by this profile's guarantee.

Fix the instance first; aggregate cost and error separately.

$\inf,\sup$: Infimum and supremum **Domain:** Evaluated only over the variable sets explicitly specified in the formula.

In the risk definition, the infimum over algorithms precedes the supremum over instances or centers.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product **Domain:** $\|x\|_2=\sqrt{\langle x,x\rangle}$.

$\langle x,y\rangle=x^\top y$

$B_p(c,R)$: Closed norm ball **Domain:** $p\in[1,\infty],\ R\ge0$.

$B_p(c,R)=\{x:\|x-c\|_p\le R\}$; $B_2$ denotes the Euclidean ball.

$N,T$: Actual call count and declared budget **Domain:** $N,T\in\mathbb{N}_0$.

A fixed budget bounds every execution path; the Markov specification uses an expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching orders, and upper bounds with hidden logarithms **Domain:** Within the joint parameter window specified for each complexity regime.

Dependence of hidden constants on fixed parameters is stated separately for each bound. Tilde notation may hide logarithmic factors only in the declared variables.

$c,C,c_\alpha,C_\alpha$: Positive constant in a proof or asymptotic bound **Domain:** $0<c,C,c_\alpha,C_\alpha<\infty$.

Unsubscripted constants have the dependencies stated in the bound; constants subscripted by $\alpha$ may depend only on the fixed smoothness order.

$\log,\log_+,e$: Natural logarithm, truncated logarithm, and Euler's number **Domain:** $z>0$.

$\log_+(z)=\max\{0,\log z\}$; $e=\exp(1)$, and $\log_2$ denotes the base-two logarithm.

$r_T(A)$: Optimal risk with a known matrix **Domain:** $r_T(A)\ge0$.

For a fixed matrix, take the infimum over algorithms and the supremum over centers in the ball and admissible noise laws.

$r_T(\mathcal{A};A)$: Worst-center risk of a universal algorithm for a fixed hidden matrix **Domain:** $r_T(\mathcal{A};A)\ge0$.

Defined using the quantifier order of this profile's performance criterion; the matrix itself is not available for public parameter tuning.

$\|v\|_A$: Seminorm induced by a positive-semidefinite quadratic form **Domain:** $v\in\mathbb{R}^d$.

$\|v\|_A=\sqrt{v^\top Av}$

$f,f_*$: Population objective and its optimal value **Domain:** $f:\mathcal{X}_{\mathrm{fun}}\to\mathbb{R}$.

$f_*=\inf_{x\in \mathbb{R}^d}f(x)$.

$Y_t,\xi_t,t$: Scalar-observation number, noise, and call index **Domain:** $Y_t,\xi_t\in\mathbb{R},\ t\in\mathbb{N}$.

Noise independence, distribution class and scale are fixed by this profile's oracle.

$\mathcal{F}_{t-1}$: The history before the current query **Domain:** The $\sigma$-algebra generated by the algorithm's seed and previous feedback.

The current query may depend on this history.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=B_2(0,R)$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

$I_d,\preceq$: Identity matrix and positive-semidefinite order **Domain:** $I_d\in\mathbb{R}^{d\times d}$; the order applies to real symmetric matrices of the same size.

$A\preceq B$ means that $v^\top(B-A)v\ge0$ for every $v\in\mathbb{R}^d$.

$\mathfrak R_T$: Alias used in the source for the optimal worst-case expected quadratic risk **Domain:** $\mathfrak R_T\ge0$.

In the known-matrix model the quantity is $r_T(A)$. The hidden-matrix lower bound inherits the same fixed-matrix risk; the matrix and algorithm quantifiers cannot be interchanged.

## 3. Complexity bracket

### Compared quantities

#### Q1 - fixed budget risk

$$
R^\star_{v,\pi}(B;\theta)=\inf_{\mathcal A\in\mathfrak A_v:\ C_\pi(\mathcal A,I)\le B\ \forall I}\sup_I\mathbb E[\ell(I,\mathcal A)]
$$

**Definition.** Error risk at a fixed declared budget

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - fixed budget risk

$$
R^\star_{v,\pi}(B;\theta)=\inf_{\mathcal A\in\mathfrak A_v:\ C_\pi(\mathcal A,I)\le B\ \forall I}\sup_I\mathbb E[\ell(I,\mathcal A)]
$$

**Definition.** Error risk at a fixed declared budget

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one paid scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime N04a.R1

**Region.** Fix $d,A\ne0,R,\sigma_v>0$ and the positive spectrum, then take $T\to\infty$. The Gaussian model fixes the noise law; the variance-class model takes the worst case over admissible noise laws.

**Quantity.** Q1

**Resource.** Error risk at a fixed declared budget

**Status.** Optimal

**Lower bound.** B3

$$
\liminf_{T\to\infty}T\mathfrak R_T\ge\sigma_v^2S_r^2/(2R^2)
$$

**Upper bound.** B1

$$
\limsup_{T\to\infty}T r_T\le\sigma_v^2S_r^2/(2R^2)
$$

**Gap or comparison.** $1\quad\text{(leading asymptotic constant for a fixed spectrum)}$

### R2 - Parameter regime N04a.R2

**Region.** $T\ge4r$. Order the positive eigenvalues nonincreasingly and set $k=\max\{j\in\{0,\ldots,r\}:T\ge\sigma_v^2S_jJ_j/R^4\}$, with $S_0=J_0=0$. Retain the Gaussian or finite-variance noise assumption of the specified view.

**Quantity.** Q2

**Resource.** Error risk at a fixed declared budget

**Status.** Optimal

**Lower bound.** B4

$$
\Omega(\sigma_v^2S_k^2/(R^2T)+R^2\lambda_{k+1})
$$

**Upper bound.** B2

$$
O(\sigma_v^2S_k^2/(R^2T)+R^2\lambda_{k+1})
$$

**Gap or comparison.** $O(1)$

### R3 - Parameter regime N04a.R3

**Region.** $A=0$; the noise bound is arbitrary and $\varepsilon\ge0$.

**Quantity.** Q3

**Resource.** one paid scalar function value

**Status.** Optimal

**Lower bound.** B7

$$
0
$$

**Upper bound.** B6

$$
0
$$

### R4 - Parameter regime N04a.R4

**Region.** The matrix $A\ne0$ is public, with $\sigma_v=0$ and $0<\varepsilon<\lambda_1R^2/2$.

**Quantity.** Q3

**Resource.** one paid scalar function value

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B5

$$
r+1
$$

### R5 - Parameter regime N04a.R_zero_accuracy

**Region.** The matrix $A\ne0$ is public, with $\varepsilon\ge\lambda_1R^2/2$.

**Quantity.** Q3

**Resource.** one paid scalar function value

**Status.** Optimal

**Lower bound.** B7

$$
0
$$

**Upper bound.** B6

$$
0
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Scalar observations follow the independent-noise, conditional-noise, or mixed-error law specified here; every repeated observation is charged separately.

**Guarantee mapping.** Fix the matrix and positive spectrum before taking the budget to infinity. The finite-spectrum budget theorem is used only within its stated threshold. A fixed-matrix asymptotic result does not imply uniformity over matrices.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** $T$ is the number of scalar observations actually obtained. The source's observation index before the final decision is expressed in this unit.

### B1 - Spectral-direction finite differences and constrained linear estimation

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\limsup_{T\to\infty}T r_T\le\sigma_v^2 S_r^2/(2R^2)
$$

**Sources.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf)

**Conditions.** Fix $d,A\ne0,R,\sigma_v>0$ and its positive spectrum. The matrix is known and $T\to\infty$. The upper bound covers every independent centered noise law with variance at most $\sigma_v^2$.

**Local argument.** A1

**Source location.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf) theorem: Known-Hessian quadratic model; Theorems 2.3–2.4 and Appendix C, used as context for the displayed independent argument

**Source location.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf) theorem: Known-Hessian quadratic model; Theorems 2.3–2.4 and Appendix C, used as context for the displayed independent argument

### B2 - Spectral-direction finite differences and constrained linear estimation

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O(\sigma_v^2 S_k^2/(R^2T)+R^2\lambda_{k+1})
$$

**Sources.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf)

**Conditions.** $T\ge4r$, with $\lambda_1\ge\cdots\ge\lambda_r>0$. Set $\lambda_{r+1}=0$, where $k=\max\{j\in\{0,\ldots,r\}:T\ge\sigma_v^2S_jJ_j/R^4\}$.

**Local argument.** A2

### B3 - Fisher-information lower bound for quadratics with a fixed spectrum

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\liminf_{T\to\infty}T\mathfrak R_T\ge\sigma_v^2 S_r^2/(2R^2)
$$

**Sources.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf)

**Conditions.** Fix $d,A\ne0,R,\sigma_v>0$ and its positive spectrum, with $T\to\infty$. Gaussian noise yields both the Gaussian-model lower bound and a worst-case lower bound over the full variance-bounded class.

**Local argument.** A1

**Source location.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf) theorem: Known-Hessian quadratic model; Theorems 2.3–2.4 and Appendix C, used as context for the displayed independent argument

**Source location.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf) theorem: Known-Hessian quadratic model; Theorems 2.3–2.4 and Appendix C, used as context for the displayed independent argument

### B4 - Fisher-information lower bound for quadratics with a fixed spectrum

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\sigma_v^2 S_k^2/(R^2T)+R^2\lambda_{k+1})
$$

**Sources.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf)

**Conditions.** $T\ge4r$, with $\lambda_1\ge\cdots\ge\lambda_r>0$. Set $\lambda_{r+1}=0$, where $k=\max\{j\in\{0,\ldots,r\}:T\ge\sigma_v^2S_jJ_j/R^4\}$.

**Local argument.** A2

### B5 - Recovery of the linear coefficient when the Hessian is known

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
r+1
$$

**Sources.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf)

**Conditions.** $A$ is known and $\sigma_v=0$; $r=\operatorname{rank}(A)$.

**Local argument.** A3

**Source location.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf) theorem: Report quadratic audit section 1.2 and origin-plus-positive-eigenvector reconstruction

### B6 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $A=0$ or $\varepsilon\ge\lambda_1R^2/2$.

**Local argument.** A4

### B7 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $A=0$ or $\varepsilon\ge\lambda_1R^2/2$.

**Local argument.** A4

## 5. Local arguments

### A1 - Known-Hessian quadratic risk: the sharp fixed-spectrum constant

**Scope.** A fixed positive spectrum of a public positive semidefinite matrix; query/output ball of radius $R$; independent centered noise of variance at most $\sigma_v^2$. The lower bound uses Gaussian noise or a worst-case variance class containing it.

Let $\lambda_1,\ldots,\lambda_r>0$ be the positive eigenvalues and $S_r=\sum_i\lambda_i^{-1/2}$. For fixed $A,d,R,\sigma_v$,
$$\lim_{T\to\infty}T\mathfrak R_T=\frac{\sigma_v^2S_r^2}{2R^2}.$$
This is not a uniform statement for spectra that degenerate with $T$.

In an eigenbasis write the unknown center coordinates as $\theta_i$. Allocate $t_i=\lceil(T-2r)\lambda_i^{-1/2}/(2S_r)\rceil$ repetitions to each of $\pm Re_i$, for $T>2r$. The total is at most $T$. The estimator $\widehat\theta_i=-(\bar Y_i^+-\bar Y_i^-)/(2R\lambda_i)$ is unbiased with variance at most $\sigma_v^2/(2R^2\lambda_i^2t_i)$. Its expected quadratic loss is at most $\sigma_v^2S_r^2/[2R^2(T-2r)]$. Projection onto the query/output ball in the $A$ seminorm cannot increase this loss because the true center is feasible.

For the lower bound use independent cosine-squared priors supported on $[-a/\sqrt r,a/\sqrt r]$, with $a<R$. Each coordinate has prior Fisher information $\pi^2r/a^2$. Under Gaussian value noise the score contribution in coordinate $i$ is controlled by $\lambda_i^2 E_i/\sigma_v^2$, where $E_i=\mathbb E\sum_t(x_{t,i}-\theta_i)^2$. Adaptivity adds no extra Fisher term after conditioning on the past, and $\sum_iE_i\le T(R+a)^2$. Coordinate van Trees bounds followed by Cauchy--Schwarz give
$$\mathfrak R_T\ge\frac{\sigma_v^2S_r^2}{2\{T(R+a)^2+\sigma_v^2\pi^2r a^{-2}\operatorname{tr}(A^{\dagger2})\}}.$$
Take $a$ proportional to $T^{-1/4}$, truncated below $R/2$. The extra Fisher term is $o(T)$ for a fixed positive spectrum, proving the lower constant. Giving $A$ to an unknown-Hessian algorithm can only help, so this lower bound also applies in the corresponding unknown-Hessian model. It does not assert that an algorithm without $A$ attains the same sharp constant.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf)

### A2 - A finite-budget spectral bracket with a product threshold

**Scope.** Known fixed positive spectrum sorted in decreasing order; $T\ge4r$; Gaussian noise for the lower bound or a worst-case variance class containing it.

Define $S_j=\sum_{i\le j}\lambda_i^{-1/2}$ and $J_j=\sum_{i\le j}\lambda_i^{-3/2}$, and let
$$k=\max\{j\le r:T\ge\sigma_v^2S_jJ_j/R^4\},$$
with $k=0$ if the set is empty and $\lambda_{r+1}=0$. Then
$$\mathfrak R_T\asymp\frac{\sigma_v^2S_k^2}{R^2T}+R^2\lambda_{k+1}.$$
The threshold contains the product $S_jJ_j$.

Scale $x=Rz$ and observations by $\sigma_v$, reducing to $R=\sigma_v=1$ with Hessian $R^2A/\sigma_v$. In normalized coordinates, estimate the leading $k$ eigencoordinates using the allocation in the asymptotic lemma and set the rest to zero. The estimated-coordinate risk is $O(S_k^2/T)$; the omitted coordinates contribute at most $\lambda_{k+1}/2$. Projection in the quadratic seminorm preserves the upper bound. For $k=0$, return zero.

For the lower bound on the leading coordinates, choose independent signs with squared coordinate amplitudes $a_i^2=\lambda_i^{-3/2}S_k/(2T)$. The product-threshold condition ensures $\sum_i a_i^2=S_kJ_k/(2T)\le1/2$, so all centers are feasible. Reveal the other signs for each coordinate test, or use data processing for their mixtures. Adjacent Gaussian transcript divergences are proportional to $\lambda_i^2a_i^2\mathbb E\sum_tx_{t,i}^2$. The total query-energy constraint $\sum_i\mathbb E\sum_tx_{t,i}^2\le T$, the two-point testing inequality, and Cauchy--Schwarz give risk at least a universal positive constant times $S_k^2/T$.

If $k<r$, put $T'=S_{k+1}J_{k+1}>T$. Apply the same construction at the next integer budget above $T'$ and use monotonicity of minimax risk in the budget. This yields a universal constant times $S_{k+1}/J_{k+1}\ge\lambda_{k+1}$, where the last inequality uses decreasing spectral order. The maximum of these two lower bounds is within a factor two of their sum. Scaling back gives the statement. The order of eigenvalues and the product threshold are essential; this displayed argument, not an assumed published erratum, supports the corrected formula.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf)

### A3 - Noiseless recovery with a public quadratic matrix

**Scope.** A public positive semidefinite matrix $A$, a center in $B_2(R)$, and exact values; $r=\operatorname{rank}(A)$.

At most $r+1$ values recover a global minimizer in the feasible ball.

Write $f(x)=\tfrac12(x-x_*)^\top A(x-x_*)$. Query zero and $te_i$ along each positive-eigenvalue direction, for any public $0<t\le R$. Then
$$\theta_i=\frac{\lambda_it^2/2+f(0)-f(te_i)}{\lambda_it}.$$
The positive-eigenspace projection of $x_*$ has norm at most $R$ and is a minimizer; nullspace coordinates do not affect the objective. If $r=0$, zero is already optimal and needs no query.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A4 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

## References

[1] Yu, Wang, Huang, Lei and Lee. Sample Complexity for Quadratic Bandits: Hessian Dependent Bounds and Optimal Algorithms. NeurIPS 2023.

https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf
