# Quadratic objective with unknown Hessian: independent value noise on a ball; Gaussian noise

**Setting ID.** `SO_ZO_N04b_gaussian`

Single-objective optimization

Estimate the minimizer of a quadratic objective from noisy values queried in a bounded ball, measuring the global quadratic objective gap at the output.

**Status.** Fully optimal

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Quadratic smoothness; structure: Quadratic objective

**ORACLE tags.** access order: Zeroth-order interface; interface family: Independent noisy value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Quadratic energy loss

**GUARANTEE tags.** mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Estimate the minimizer of a quadratic objective from noisy values queried in a bounded ball, measuring the global quadratic objective gap at the output.

### Admissible model

$f(x)=\frac12(x-x_*)^\top A(x-x_*)$, where $A\in\mathbb{R}^{d\times d}$ is symmetric positive semidefinite and the center $x_*\in B_2(0,R)$ is unknown. The function is defined throughout the ambient space and has minimum value zero.

The matrix $A$ may be singular; only the component of the center in $\operatorname{range}(A)$ must then be estimated. Whether the matrix, spectrum and center are known is fixed by the Oracle interface.

### Oracle interface

A query at $x_t\in B_2(0,R)$ returns one scalar $Y_t=f(x_t)+\xi_t$.

$\xi_t$ is drawn i.i.d. from $N(0,\sigma_v^2)$, independently of the algorithmic seed and preceding observations.

Every observation is charged independently. No same-sample coupling, sample handle, or noiseless function value is supplied.

The matrix $A$, its rank, and its eigenspaces are hidden. Spectrum-dependent expressions describe performance and are not public tuning inputs.

The public inputs are $d$, $R$, $\sigma_v$, $\varepsilon$, $T$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in B_2(0,R)$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=\frac12(x-x_*)^\top A(x-x_*)=\frac12\|x-x_*\|_A^2$; it remains finite and nonnegative even when $A$ is singular.

For a strategy that does not depend on $A$, write $r_T(\mathcal{A};A)=\sup_{\|x_*\|_2\le R}\mathbb{E}[\ell(I,\widehat{x})]$. The variance-class specification additionally takes the supremum over admissible noise distributions.

### Resource accounting

Each scalar function value or noisy observation costs $1$ call. Every location in a multipoint finite difference, every initialization query, and every reference observation is charged.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

There is one universal algorithm independent of the hidden matrix $A$. For each fixed nonzero positive-semidefinite $A$ and $d,R,\sigma_v$, as $T\to\infty$, its risk uniformly over centers in the ball attains the displayed order. Entry into the asymptotic regime may depend on the fixed spectrum. The variance-class specification additionally requires uniformity over admissible noise laws.

The quantifiers select one algorithm first and then state an asymptotic conclusion for each fixed matrix. They do not take a uniform finite-budget supremum over matrix sequences that degenerate with $T$.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$R$: Radius of the unknown-center localization ball and of the query/output ball **Domain:** $R>0$.

$x_*,x_t,\widehat{x}\in B_2(0,R)$

$\sigma_v$: Standard deviation of independent Gaussian value noise **Domain:** $\sigma_v\ge0$.

$\xi\sim N(0,\sigma_v^2)$

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

### R1 - Parameter regime N04b.R1

**Region.** Use one algorithm independent of the hidden matrix. For each fixed $A\ne0$ and $d,R,\sigma_v>0$, take $T\to\infty$. The risk is uniform over centers in $B_2(0,R)$; entry into the asymptotic regime may depend on the fixed matrix.

**Quantity.** Q1

**Resource.** Error risk at a fixed declared budget

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(\sigma_v^2S_r^2/(R^2T))
$$

**Upper bound.** B1

$$
O(\sigma_v^2S_r^2/(R^2T))
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Scalar observations follow the independent-noise, conditional-noise, or mixed-error law specified here; every repeated observation is charged separately.

**Guarantee mapping.** Fix the matrix and positive spectrum before taking the budget to infinity. The finite-spectrum budget theorem is used only within its stated threshold. A fixed-matrix asymptotic result does not imply uniformity over matrices.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** $T$ is the number of scalar observations actually obtained. The source's observation index before the final decision is expressed in this unit.

### B1 - Hessian estimation, spectral truncation and two-stage correction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\limsup_{T\to\infty}T\sup_{x_\star}\mathbb{E}[f(\hat{x})-f^*]\le C\sigma_v^2S_r^2/R^2
$$

**Sources.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf)

**Conditions.** Use one algorithm independent of the hidden matrix. For each fixed $A\ne0$, $d,R,\sigma_v>0$ and positive spectrum, evaluate the center-uniform risk within the ball as $T\to\infty$.

**Source location.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf) theorem: Theorem 2.4 / Section 4; pdf pages: 3; printed pages: 3

**Source location.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf) theorem: Theorem 2.4 / Section 4

### B2 - Statistical lower-bound reduction with a known Hessian

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\liminf_{T\to\infty}T\mathfrak R_T\ge\frac{\sigma_v^2}{2R^2}S_r^2
$$

**Sources.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf)

**Conditions.** For each fixed $A\ne0$, $d,R,\sigma_v>0$, and positive spectrum, the Gaussian asymptotic lower bound for the public-matrix model applies.

**Local argument.** A1

**Source location.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf) theorem: Known-Hessian quadratic model; Theorems 2.3–2.4 and Appendix C, used as context for the displayed independent argument

**Source location.** [1](https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf) theorem: Known-Hessian quadratic model; Theorems 2.3–2.4 and Appendix C, used as context for the displayed independent argument

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

## References

[1] Yu, Wang, Huang, Lei and Lee. Sample Complexity for Quadratic Bandits: Hessian Dependent Bounds and Optimal Algorithms. NeurIPS 2023.

https://proceedings.neurips.cc/paper_files/paper/2023/file/6e60a9023d2c63f7f0856910129ae753-Paper-Conference.pdf
