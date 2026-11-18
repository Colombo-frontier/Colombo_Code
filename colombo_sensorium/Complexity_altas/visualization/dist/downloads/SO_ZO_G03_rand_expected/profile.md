# Global optimization in a Matérn RKHS with independent noisy values

**Setting ID.** `SO_ZO_G03_rand_expected`

Single-objective optimization

Find an approximate global minimizer of the unknown objective over $[0,1]^d$. Evaluate the final recommendation by simple regret $f(\widehat{x})-\min_{u\in [0,1]^d}f(u)$; losses incurred during queries are not accumulated.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; smoothness: Matern rkhs norm bound

**ORACLE tags.** access order: Zeroth-order interface; interface family: Independent noisy value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find an approximate global minimizer of the unknown objective over $[0,1]^d$. Evaluate the final recommendation by simple regret $f(\widehat{x})-\min_{u\in [0,1]^d}f(u)$; losses incurred during queries are not accumulated.

### Admissible model

$X=[0,1]^d$. The known kernel $k$ is a Matérn kernel with smoothness parameter $\nu>0$. Its amplitude and positive length scale are fixed and known.

The unknown objective belongs to the kernel's reproducing kernel Hilbert space $\mathcal{H}_k$ on $X$ and satisfies $\|f\|_{\mathcal{H}_k}\le B$ and $B>0$. Continuity and compactness ensure that a minimum is attained.

### Oracle interface

A query at $x_t\in [0,1]^d$ returns one scalar $Y_t=f(x_t)+\xi_t$.

Noise is independent, centered and sub-Gaussian: $\mathbb{E} e^{\lambda\xi_t}\le e^{\lambda^2 \sigma_v^2/2}$ for every $\lambda\in\mathbb{R}$. It is independent of the algorithmic seed and preceding observations. The noise class includes Gaussian noise at the same scale.

Every observation is charged independently. No same-sample coupling, sample handle, or noiseless function value is supplied.

The public inputs are $d$, $\nu$, $B$, $k$, $\sigma_v$, $\varepsilon$, $T$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in [0,1]^d$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in [0,1]^d}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

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

$\nu$: Matérn kernel smoothness parameter **Domain:** $\nu>0$.

$B$: Radius of the RKHS norm ball **Domain:** $B>0$.

$\|f\|_{\mathcal{H}_k}\le B$

$k$: Fully known positive-semidefinite kernel and its scale parameters **Domain:** $k:X\times X\to\mathbb{R}$.

$\mathcal{H}_k$ is the reproducing kernel Hilbert space of kernel $k$ on $X$.

$\sigma_v$: Standard scale of centered sub-Gaussian value noise **Domain:** $\sigma_v\ge0$.

$\mathbb{E}\exp(\lambda\xi)\le\exp(\lambda^2\sigma_v^2/2)$, $\lambda\in\mathbb{R}$.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$T$: Known query budget or argument of the risk curve **Domain:** $T\in\mathbb{N}_0$.

Use $N\le T$ in the fixed-budget specification and $\mathbb{E}[N]\le T$ in the expected-budget specification.

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $[0,1]^d$.

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

$r_T$: Error scale of the final recommendation under the budget **Domain:** $T\in\mathbb{N}_0$.

Under an expectation guarantee, the quantity is $\inf_{\mathcal{A}:N\le T}\sup_I\mathbb{E}[f(\widehat{x})-f_*]$. Under a fixed-success-probability guarantee, it is the $2/3$ quantile threshold with the same quantifier order.

$f,f_*$: Population objective and its optimal value **Domain:** $f:\mathcal{X}_{\mathrm{fun}}\to\mathbb{R}$.

$f_*=\inf_{x\in [0,1]^d}f(x)$.

$Y_t,\xi_t,t$: Scalar-observation number, noise, and call index **Domain:** $Y_t,\xi_t\in\mathbb{R},\ t\in\mathbb{N}$.

Noise independence, distribution class and scale are fixed by this profile's oracle.

$\mathcal{F}_{t-1}$: The history before the current query **Domain:** The $\sigma$-algebra generated by the algorithm's seed and previous feedback.

The current query may depend on this history.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=[0,1]^d$ and $\mathcal{X}=[0,1]^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime G03.R1

**Region.** Fix $d,\nu>1/2,B>0,\sigma_v>0$ and the complete Matérn kernel; $X=[0,1]^d$ and sufficiently small $\varepsilon/B$.

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega_{d,\nu}(\varepsilon^{-2-d/\nu})
$$

**Upper bound.** B1

$$
\widetilde{O}_{d,\nu}(\varepsilon^{-2-d/\nu})
$$

**Gap or comparison.** $\operatorname{polylog}(1/\varepsilon)$

### R2 - Parameter regime G03.R2

**Region.** Fix $d\ge1,0<\nu\le1/2,B>0,\sigma_v>0$ and the complete Matérn kernel; require $X=[0,1]^d$, $\varepsilon/B\to0$ and $\varepsilon/\sigma_v\to0$.

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega_{d,\nu,k}(\sigma_v^2\varepsilon^{-2}(B/\varepsilon)^{d/\nu})
$$

**Upper bound.** B3

$$
O_{d,\nu,k}(\sigma_v^2\varepsilon^{-2}(B/\varepsilon)^{d/\nu}\log(2+B/\varepsilon))
$$

**Gap or comparison.** $O_{d,\nu,k}(\log(2+B/\varepsilon))$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Scalar observations follow the independent-noise, conditional-noise, or mixed-error law specified here; every repeated observation is charged separately.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Maximum variance reduction or repeated grid sampling

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde{O}(\varepsilon^{-2-d/\nu})
$$

**Sources.** [5](https://proceedings.neurips.cc/paper/2021/file/b1300291698eadedb559786c809cc592-Paper.pdf) [1](https://arxiv.org/html/2602.17940v1) [2](https://arxiv.org/html/2502.06363v1) [6](https://arxiv.org/html/2607.29245v2)

**Conditions.** A conservative universal logarithmic factor is $\log^{3+d/\nu}(1/\varepsilon)$. The sharper expression $\log^{(4\nu+d)/(2\nu)}$ from V21 requires its spectral and discretization assumptions.

**Local argument.** A1

**Source location.** [5](https://proceedings.neurips.cc/paper/2021/file/b1300291698eadedb559786c809cc592-Paper.pdf) theorem: V21, Corollary 1; spectral assumptions in I26, Section 1.1; IT25, Theorem 5.1; pdf pages: 8; printed pages: 8

**Source location.** [1](https://arxiv.org/html/2602.17940v1) theorem: V21, Corollary 1; spectral assumptions in I26, Section 1.1; IT25, Theorem 5.1; pdf pages: 10; printed pages: 10

**Source location.** [2](https://arxiv.org/html/2502.06363v1) theorem: V21, Corollary 1; spectral assumptions in I26, Section 1.1; IT25, Theorem 5.1

**Source location.** [2](https://arxiv.org/html/2502.06363v1) theorem: V21, Corollary 1; spectral assumptions in I26, Section 1.1; IT25, Theorem 5.1; pdf pages: 8; printed pages: 8

### B2 - Gaussian testing in a Matérn RKHS

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\sigma_v^2\varepsilon^{-2}(B/\varepsilon)^{d/\nu}\right)
$$

**Sources.** [4](https://proceedings.mlr.press/v65/scarlett17a/scarlett17a.pdf)

**Conditions.** $\varepsilon/B$ is sufficiently small; $d,\nu$ and the kernel scale are fixed.

**Source location.** [4](https://proceedings.mlr.press/v65/scarlett17a/scarlett17a.pdf) theorem: Theorem 1(2); pdf pages: 3; printed pages: 3

### B3 - Repeated grid sampling

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O_{d,\nu,k}\!\left((B/\varepsilon)^{d/\nu}\left[1+\sigma_v^2\varepsilon^{-2}\log(2+B/\varepsilon)\right]\right)
$$

**Sources.** [3](https://gaussianprocess.org/gpml/chapters/RW4.pdf)

**Conditions.** Fix $d\ge 1,0<\nu \le 1/2,$, the known Matérn kernel and its fixed positive length scale and amplitude $,B>0$. Require $0<\varepsilon \le c_k B$, with independent centered $\sigma_v -subGaussian$ noise. N is the size of a cube grid with covering radius $h=(\varepsilon /(4C_k B))^{1/\nu }$, and $N\le C_{d,\nu ,k}(B/\varepsilon )^{d/\nu }$.

**Local argument.** A2

**Source location.** [3](https://gaussianprocess.org/gpml/chapters/RW4.pdf) theorem: RKHS reproducing inequality + Matérn spectral density (4.15) + repeated grid observations; pdf pages: 6; printed pages: 84

## 5. Local arguments

### A1 - Information-gain and exponential-error conversions

**Scope.** Fixed dimension, RKHS radius, kernel scales, and noise parameters unless the individual bound explicitly tracks them jointly; preserve each cited discretization and spectral assumption.

The registered noisy RKHS upper rates follow by inserting the applicable information-gain bound into maximum variance reduction. The noiseless squared-exponential call rate follows by inverting its exponential error estimate.

For maximum variance reduction, the cited primary theorem bounds simple regret through the posterior maximum variance and maximum information gain. Use the theorem's own confidence allocation and a polynomial-size approximation grid; bounded RKHS function amplitude controls the contribution of the failure event when converting to expected regret. For the Matern kernel, the compatible polynomial information-gain exponent is $d/(2\nu+d)$. Solving the resulting error-versus-horizon inequality gives the call exponent $2+d/\nu$. The conservative displayed logarithmic allowance $\log^{3+d/\nu}(1/\varepsilon)$ is retained; the tighter source logarithm is used only with its additional spectral and discretization hypotheses.

For the squared-exponential kernel, insert the refined information-gain bound from Theorem 5.1 of the cited primary source into the maximum variance reduction guarantee. With fixed nuisance parameters, the resulting sufficient horizon is
$$O\!\left(\varepsilon^{-2}\frac{\log^{d+2}(1/\varepsilon)}{[\log\log(1/\varepsilon)]^d}\right).$$
For a sphere domain, use a polynomial-size sphere net instead of a convex-domain grid. A smooth fixed kernel gives a bounded RKHS derivative and hence a uniform Lipschitz modulus, so a sufficiently fine net contributes the chosen approximation error. The confidence union bound depends on the logarithm of the net size; the variance-selection and information-gain steps themselves are applied on that finite legal set. This explicitly supplies the required domain transfer.

For noiseless squared-exponential optimization, the cited exponential bound has the form $C B\exp[-cT^{1/d}\log T]$ after its startup conditions. Put $L_\varepsilon=\log(B/\varepsilon)$. Choosing $T=C'[L_\varepsilon/\log L_\varepsilon]^d$ makes $T^{1/d}\log T$ at least a constant multiple of $L_\varepsilon$ for sufficiently small $\varepsilon/B$, giving the registered inverse rate. The one-dimensional exact expected-improvement case retains the source's separate construction. Constants and sufficiently-small-accuracy thresholds may depend on the fixed dimension and kernel; the inversion does not claim parameter-uniformity.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [5](https://proceedings.neurips.cc/paper/2021/file/b1300291698eadedb559786c809cc592-Paper.pdf) [1](https://arxiv.org/html/2602.17940v1) [2](https://arxiv.org/html/2502.06363v1) [6](https://arxiv.org/html/2607.29245v2)

### A2 - Repeated-grid optimization for a low-smoothness Matern RKHS

**Scope.** A fixed-dimensional cube, a public Matern kernel with fixed positive scale and amplitude, RKHS norm at most $B>0$, independent centered $\sigma_v$-sub-Gaussian noise, and fixed $0<\nu\le1/2$.

For $0<\varepsilon\le c_kB$, a deterministic observation budget suffices:
$$O_{d,\nu,k}\!\left((B/\varepsilon)^{d/\nu}[1+\sigma_v^2\varepsilon^{-2}\log(2+B/\varepsilon)]\right).$$

The reproducing inequality gives
$$|f(x)-f(y)|\le B\|k_x-k_y\|_{\mathcal H_k},\qquad\|k_x-k_y\|_{\mathcal H_k}^2=2[k(0)-k(x-y)].$$
The Matern spectral density is a constant multiple of $(a^2+\|\omega\|^2)^{-\nu-d/2}$ for fixed $a>0$. With $r=\|x-y\|\le1$, use $1-\cos t\le\min\{t^2/2,2\}$ and split the radial integral at $1/r$. The two parts are bounded by
$$Cr^2\int_0^{1/r}t^{d+1}(a^2+t^2)^{-\nu-d/2}\,dt\le C'r^{2\nu},\quad C\int_{1/r}^{\infty}t^{d-1}(a^2+t^2)^{-\nu-d/2}\,dt\le C'r^{2\nu}.$$
Thus $|f(x)-f(y)|\le C_kB\|x-y\|^\nu$. Also $|f(x)|\le B\sqrt{k(0)}=:M_0$, so any simple regret is at most $2M_0$.

Use a Cartesian $h$-net with $h=(\varepsilon/(4C_kB))^{1/\nu}$ and cardinality $N\le C_{d,\nu,k}(B/\varepsilon)^{d/\nu}$. At each point take
$$m=\max\{1,\lceil32\sigma_v^2\varepsilon^{-2}\log(16NM_0/\varepsilon)\rceil\}$$
independent observations. Output the smallest empirical mean. A union bound makes the probability that any mean error exceeds $\varepsilon/4$ at most $\varepsilon/(8M_0)$. On its complement, net approximation and the two relevant mean errors give regret at most $3\varepsilon/4$. The bad-event contribution is at most $2M_0\cdot\varepsilon/(8M_0)=\varepsilon/4$. Hence expected regret is at most $\varepsilon$ with the fixed cap $Nm$. Keeping $m\ge1$ explains the startup term. This explicit argument does not require extending a different algorithm's theorem beyond its own range of $\nu$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [3](https://gaussianprocess.org/gpml/chapters/RW4.pdf)

## References

[1] Shogo Iwazaki. Tighter Regret Lower Bound for Gaussian Process Bandits with Squared Exponential Kernel in Hypersphere. arXiv:2602.17940v1, 2026-02-20.

https://arxiv.org/html/2602.17940v1

[2] Shogo Iwazaki and Shion Takeno. Improved Regret Analysis in Gaussian Process Bandits: Optimality for Noiseless Reward, RKHS norm, and Non-Stationary Variance. arXiv:2502.06363v1, 2025.

https://arxiv.org/html/2502.06363v1

[3] Carl Edward Rasmussen, Christopher K. I. Williams. Gaussian Processes for Machine Learning. Official author-hosted Chapter4, Matérn spectral density equation4.15; read 2026-10-29.

https://gaussianprocess.org/gpml/chapters/RW4.pdf

[4] Scarlett, Bogunovic and Cevher. Lower Bounds on Regret for Noisy Gaussian Process Bandit Optimization. COLT 2017, PMLR 65.

https://proceedings.mlr.press/v65/scarlett17a/scarlett17a.pdf

[5] Vakili, Bouziani, Jalali, Bernacchia and Shiu. Optimal Order Simple Regret for Gaussian Process Bandits. NeurIPS 2021.

https://proceedings.neurips.cc/paper/2021/file/b1300291698eadedb559786c809cc592-Paper.pdf

[6] Emmanuel Vazquez and Sébastien Petit. Simple-regret rates and minimax optimality of fixed-prior expected improvement in Matern and squared-exponential RKHSs. arXiv:2607.29245v2, 2026-09-16.

https://arxiv.org/html/2607.29245v2
