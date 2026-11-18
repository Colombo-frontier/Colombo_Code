# Global optimization in a squared-exponential RKHS: exact values

**Setting ID.** `SO_ZO_G05`

Single-objective optimization

Find an approximate global minimizer of the unknown objective over $X$. Evaluate the final recommendation by simple regret $f(\widehat{x})-\min_{u\in X}f(u)$; losses incurred during queries are not accumulated.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; smoothness: Squared exponential rkhs norm bound

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find an approximate global minimizer of the unknown objective over $X$. Evaluate the final recommendation by simple regret $f(\widehat{x})-\min_{u\in X}f(u)$; losses incurred during queries are not accumulated.

### Admissible model

$X\subset\mathbb{R}^d$ is a known compact domain with nonempty interior. The known kernel $k$ is the squared-exponential kernel, with fixed known amplitude and positive length scale.

The unknown objective belongs to the kernel's reproducing kernel Hilbert space $\mathcal{H}_k$ on $X$ and satisfies $\|f\|_{\mathcal{H}_k}\le B$ and $B>0$. Continuity and compactness ensure that a minimum is attained.

### Oracle interface

At any finite query point $x$ in $X$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

The public inputs are $d$, $B$, $k$, $X$, $\varepsilon$, $T$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in X$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in X}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

Each scalar function value or noisy observation costs $1$ call. Every location in a multipoint finite difference, every initialization query, and every reference observation is charged.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

#### Deterministic

Only deterministic strategies are allowed. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The requirement $\ell(I,\widehat{x})\le \varepsilon$ holds deterministically for each instance.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

#### Randomized

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The error requirement is $\Pr(\ell(I,\widehat{x})\le \varepsilon)\ge2/3$.

Probability is over the algorithm's random seed only.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

**Output qualification.** Random selection among previously queried points is permitted, subject to the declared success guarantee.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$B$: Radius of the RKHS norm ball **Domain:** $B>0$.

$\|f\|_{\mathcal{H}_k}\le B$

$k$: Fully known positive-semidefinite kernel and its scale parameters **Domain:** $k:X\times X\to\mathbb{R}$.

$\mathcal{H}_k$ is the reproducing kernel Hilbert space of kernel $k$ on $X$.

$X$: Fully known feasible or search domain **Domain:** $X\subset\mathbb{R}^d$; compact with nonempty interior.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$T$: Known query budget or argument of the risk curve **Domain:** $T\in\mathbb{N}_0$.

Use $N\le T$ in the fixed-budget specification and $\mathbb{E}[N]\le T$ in the expected-budget specification.

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $X$.

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

$f_*=\inf_{x\in X}f(x)$.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=X$ and $\mathcal{X}=X$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime G05.R1

**Region.** Deterministic strategies; fixed $d,B>0$, the complete squared-exponential kernel, and a compact domain $X$ with nonempty interior; $\log(B/\varepsilon)$ is sufficiently large.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Optimal

**Lower bound.** B2

$$
\Omega_d((a/\log a)^d)
$$

**Upper bound.** B1

$$
O_d((a/\log a)^d)
$$

**Gap or comparison.** $O_d(1)$

### R2 - Applicability window of an individual theorem

**Region.** Fix the dimension, complete squared-exponential kernel and $B>0$, with sufficiently small target accuracy. The one-dimensional branch uses the corresponding exact expected-improvement construction in the source.

**Views.** Randomized

**Quantity.** Q2

**Resource.** One scalar function value or observation

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Kernel interpolation and expected improvement under a fixed prior

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left((\log(B/\varepsilon)/\log\log(B/\varepsilon))^d\right)
$$

**Sources.** [1](https://arxiv.org/html/2607.29245v2) [2](https://proceedings.neurips.cc/paper/2021/file/b1300291698eadedb559786c809cc592-Paper.pdf) [3](https://arxiv.org/html/2602.17940v1) [4](https://arxiv.org/html/2502.06363v1)

**Conditions.** Fix the dimension, complete squared-exponential kernel and $B>0$, with sufficiently small target accuracy. The one-dimensional branch uses the corresponding exact expected-improvement construction in the source.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2607.29245v2) theorem: Theorem 7.4, obtained by inverting the exponential error bound

**Source location.** [1](https://arxiv.org/html/2607.29245v2) theorem: Theorem 7.4, obtained by inverting the exponential error bound; pdf pages: 21; printed pages: 21

### B2 - Deterministic information lower bound for the squared-exponential RKHS

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\mathrm{Det}:\ \Omega\!\left((\log(B/\varepsilon)/\log\log(B/\varepsilon))^d\right)
$$

**Sources.** [1](https://arxiv.org/html/2607.29245v2)

**Conditions.** Fix the dimension, complete squared-exponential kernel and $B>0$, with sufficiently small target accuracy. The algorithmic quantifier is restricted to deterministic adaptive strategies.

**Guarantee conversion.** Covers deterministic algorithms only; this bound does not apply to the randomized view.

**Source location.** [1](https://arxiv.org/html/2607.29245v2) theorem: Theorem 7.4; Lemma F.3

**Source location.** [1](https://arxiv.org/html/2607.29245v2) theorem: Theorem 7.4; Lemma F.3

**Source location.** [1](https://arxiv.org/html/2607.29245v2) theorem: Theorem 7.4; Lemma F.3; pdf pages: 21; printed pages: 21

**Source location.** [1](https://arxiv.org/html/2607.29245v2) theorem: Theorem 7.4; Lemma F.3; pdf pages: 38; printed pages: 38

### B3 - Kernel interpolation and expected improvement under a fixed prior

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left((\log(B/\varepsilon)/\log\log(B/\varepsilon))^d\right)
$$

**Sources.** [1](https://arxiv.org/html/2607.29245v2) [2](https://proceedings.neurips.cc/paper/2021/file/b1300291698eadedb559786c809cc592-Paper.pdf) [3](https://arxiv.org/html/2602.17940v1) [4](https://arxiv.org/html/2502.06363v1)

**Conditions.** Fix the dimension, complete squared-exponential kernel and $B>0$, with sufficiently small target accuracy. The one-dimensional branch uses the corresponding exact expected-improvement construction in the source.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2607.29245v2) theorem: Theorem 7.4, obtained by inverting the exponential error bound

**Source location.** [1](https://arxiv.org/html/2607.29245v2) theorem: Theorem 7.4, obtained by inverting the exponential error bound; pdf pages: 21; printed pages: 21

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

**Sources.** [2](https://proceedings.neurips.cc/paper/2021/file/b1300291698eadedb559786c809cc592-Paper.pdf) [3](https://arxiv.org/html/2602.17940v1) [4](https://arxiv.org/html/2502.06363v1) [1](https://arxiv.org/html/2607.29245v2)

## References

[1] Emmanuel Vazquez and Sébastien Petit. Simple-regret rates and minimax optimality of fixed-prior expected improvement in Matern and squared-exponential RKHSs. arXiv:2607.29245v2, 2026-09-16.

https://arxiv.org/html/2607.29245v2

[2] Vakili, Bouziani, Jalali, Bernacchia and Shiu. Optimal Order Simple Regret for Gaussian Process Bandits. NeurIPS 2021.

https://proceedings.neurips.cc/paper/2021/file/b1300291698eadedb559786c809cc592-Paper.pdf

[3] Shogo Iwazaki. Tighter Regret Lower Bound for Gaussian Process Bandits with Squared Exponential Kernel in Hypersphere. arXiv:2602.17940v1, 2026-02-20.

https://arxiv.org/html/2602.17940v1

[4] Shogo Iwazaki and Shion Takeno. Improved Regret Analysis in Gaussian Process Bandits: Optimality for Noiseless Reward, RKHS norm, and Non-Stationary Variance. arXiv:2502.06363v1, 2025.

https://arxiv.org/html/2502.06363v1
