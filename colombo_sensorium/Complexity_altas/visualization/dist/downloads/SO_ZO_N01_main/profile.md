# Lipschitz convex optimization with independent value noise

**Setting ID.** `SO_ZO_N01_main`

Single-objective optimization

Minimize $f$ globally over $B_2(0,1)$ and return a point with small objective gap.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Other quantified gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Lipschitz function; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Independent noisy value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $B_2(0,1)$ and return a point with small objective gap.

### Admissible model

$f:B_2(0,1)\to\mathbb{R}$ is convex and $1$-Lipschitz, with range contained in the prescribed interval $[a_0,a_0+C_f]$. The endpoint $a_0$ and constant length $C_f>0$ are known. The unit ball, Lipschitz bound and fixed range length together define this normalized instance class.

### Oracle interface

A query at $x_t\in B_2(0,1)$ returns one scalar $Y_t=f(x_t)+\xi_t$.

Noise is independent, centered and sub-Gaussian: $\mathbb{E} e^{\lambda\xi_t}\le e^{\lambda^2 1/2}$ for every $\lambda\in\mathbb{R}$. It is independent of the algorithmic seed and preceding observations. The noise class includes Gaussian noise at the same scale.

Every observation is charged independently. No same-sample coupling, sample handle, or noiseless function value is supplied.

The public inputs are $d$, $\varepsilon$, $a_0$, $C_f$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in B_2(0,1)$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in B_2(0,1)}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

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

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$d_0$: Universal dimension threshold required by the lower bound **Domain:** $d_0>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $B_2(0,1)$.

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

$f,f_*$: Population objective and its optimal value **Domain:** $f:\mathcal{X}_{\mathrm{fun}}\to\mathbb{R}$.

$f_*=\inf_{x\in B_2(0,1)}f(x)$.

$Y_t,\xi_t,t$: Scalar-observation number, noise, and call index **Domain:** $Y_t,\xi_t\in\mathbb{R},\ t\in\mathbb{N}$.

Noise independence, distribution class and scale are fixed by this profile's oracle.

$\mathcal{F}_{t-1}$: The history before the current query **Domain:** The $\sigma$-algebra generated by the algorithm's seed and previous feedback.

The current query may depend on this history.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=B_2(0,1)$ and $\mathcal{X}=B_2(0,1)$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$a_0,C_f$: Left endpoint and length of the known value-range interval **Domain:** $a_0\in\mathbb{R},\ C_f>0$.

$a_0\le f(x)\le a_0+C_f$; the range length is fixed by the normalization of this profile.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one paid scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime N01.R1

**Region.** $d\ge d_0$ and $Cd^{-1/4}\le\varepsilon\le c$. The domain radius, Lipschitz constant, noise scale and known range length are fixed at the model's normalized values. The constant $c,C>0$ is the universal window constant in the source theorem.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Optimal

**Lower bound.** B1

$$
\Omega(d^2\varepsilon^{-4})
$$

**Upper bound.** B2

$$
O(d^2\varepsilon^{-4})
$$

**Gap or comparison.** $O(1)$

### R2 - Parameter regime N01.R2

**Region.** $d\ge d_0$ and $Cd^{-1/2}\le\varepsilon\le cd^{-1/4}$; the normalization scales of the model are fixed.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Other quantified gap

**Lower bound.** B1

$$
\Omega(d^{5/2}\varepsilon^{-2})
$$

**Upper bound.** B2

$$
O(d^2\varepsilon^{-4})
$$

**Gap or comparison.** $O(d^{-1/2}\varepsilon^{-2})$

### R3 - Parameter regime N01.R3

**Region.** $d\ge d_0$ and $0<\varepsilon\le cd^{-1/2}$; normalization scales are fixed, and joint dependence is tracked in $d,\varepsilon$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Polynomial gap

**Lower bound.** B1

$$
\Omega(d^{5/2}\varepsilon^{-2})
$$

**Upper bound.** B3

$$
\widetilde{O}(d^3\varepsilon^{-2})
$$

**Gap or comparison.** $\widetilde{O}(\sqrt d)$

### R4 - Parameter regime N01.R4

**Region.** $d=1$ and $0<\varepsilon\le c$; the normalization scales of the model are fixed.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Optimal

**Lower bound.** B5

$$
\Omega(\varepsilon^{-2})
$$

**Upper bound.** B4

$$
O(\varepsilon^{-2})
$$

**Gap or comparison.** $O(1)$

### R5 - Parameter regime N01.R_zero

**Region.** $\varepsilon\ge1$.

**Quantity.** Q1

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

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Statistical-testing hard family of noisy convex functions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\min\{d^{5/2}\varepsilon^{-2},d^2\varepsilon^{-4}\}\right)
$$

**Sources.** [4](https://arxiv.org/html/2607.18652v3)

**Conditions.** $d\ge d_0$ and $0<\varepsilon<c$. The hard subclass uses unit-variance Gaussian noise and satisfies the fixed range and unit Lipschitz bound.

**Source location.** [4](https://arxiv.org/html/2607.18652v3) theorem: Theorem 1.1

**Source location.** [4](https://arxiv.org/html/2607.18652v3) theorem: Theorem 1.1; pdf pages: 3; printed pages: 3

### B2 - One-point smoothing and convex averaging

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(d^2\varepsilon^{-4})
$$

**Sources.** [2](https://arxiv.org/abs/cs/0408007) [1](https://arxiv.org/pdf/2406.06506)

**Conditions.** Unit ball, unit Lipschitz bound and a known fixed value range. Centered noise has a bounded second moment, and the scalar-query budget is fixed.

**Local argument.** A1

**Source location.** [2](https://arxiv.org/abs/cs/0408007) theorem: Theorem 2, PDF p.9; noisy-value second-moment extension and convex averaging; pdf pages: 9

### B3 - Noisy online Newton method with convex averaging

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}(d^3\varepsilon^{-2})
$$

**Sources.** [1](https://arxiv.org/pdf/2406.06506) [2](https://arxiv.org/abs/cs/0408007)

**Conditions.** Known fixed value range, unit symmetric ball and centered sub-Gaussian noise. Convex averaging and the bounded objective gap on the failure event give the expectation guarantee.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/pdf/2406.06506) theorem: Theorem 2, PDF p.2; symmetric ball M=d^{-1/2}; online-to-batch and failure-probability allocation; pdf pages: 2

### B4 - Noisy convex interval search in one dimension

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\varepsilon^{-2})
$$

**Sources.** [3](https://arxiv.org/html/2607.12938v1)

**Conditions.** $d=1$. Minimize a convex function over the known interval. Its range length is fixed, and the noise is independent, centered and sub-Gaussian.

**Source location.** [3](https://arxiv.org/html/2607.12938v1) theorem: Corollary 4.2, PDF p.4; proof Appendix A.2, PDF p.12; pdf pages: 4

**Source location.** [3](https://arxiv.org/html/2607.12938v1) theorem: Corollary 4.2, PDF p.4; proof Appendix A.2, PDF p.12; pdf pages: 12

### B5 - Two-point Gaussian testing

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\varepsilon^{-2})
$$

**Conditions.** $d=1$ and $0<\varepsilon<c$; the Gaussian noise has fixed unit variance.

**Local argument.** A2

### B6 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge 1$.

**Local argument.** A3

### B7 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge 1$.

**Local argument.** A3

## 5. Local arguments

### A1 - Noisy-value extensions of normalized convex algorithms

**Scope.** A public bounded objective-value range, the normalized feasible ball, the stated centered noise class, and a fixed scalar-call cap.

The one-point finite-second-moment construction gives $O(d^2\varepsilon^{-4})$. Under the stronger centered sub-Gaussian noise model, the online Newton result gives $\widetilde O(d^3\varepsilon^{-2})$ after an explicit online-to-batch transfer.

For the one-point branch use $g=dYu/h$ at a perturbed point, where $Y$ is the noisy scalar value and $u$ is uniform on the sphere. Centered noise preserves the ball-smoothing gradient identity. The public value range and second-moment noise bound give $\mathbb E\|g\|^2=O(d^2/h^2)$. Work on a shrunken unit ball; Lipschitz smoothing and comparator shrinkage cost $O(h)$. Projected averaging gives total expected gap $O(d/(h\sqrt T)+h)$. Choose $h$ proportional to $\varepsilon$ and $T=O(d^2\varepsilon^{-4})$.

For the online Newton branch, use Theorem 2 of the cited source with the symmetric-ball geometric parameter $M=d^{-1/2}$. On a fixed stochastic objective, convexity bounds the loss of the average of the played feasible points by average expected regret. Allocate the theorem's failure probability so that its contribution, multiplied by the public maximum possible objective gap, is at most a fixed fraction of $\varepsilon$. Choose its regret budget for the remaining fraction. Substituting the normalized ball parameter and solving for the horizon gives the displayed $\widetilde O(d^3\varepsilon^{-2})$ scalar cost. The stronger sub-Gaussian assumption is retained; this branch is not transferred to an unrestricted finite-variance class.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [2](https://arxiv.org/abs/cs/0408007) [1](https://arxiv.org/pdf/2406.06506)

### A2 - A one-dimensional Gaussian testing lower bound

**Scope.** Queries and output in $[-1,1]$; convex normalized Lipschitz functions in a public bounded value range; fresh unit-variance Gaussian values; expected loss.

For $T\ge1$, worst-instance expected error is at least $3/(32\sqrt T)$ on the displayed two-function family, giving $\Omega(\varepsilon^{-2})$ calls at small accuracy.

Let $a=1/(4\sqrt T)$ and $f_v(x)=a(1+vx)$ for $v\in\{-1,1\}$. These functions are convex, $a$-Lipschitz, take values in $[0,2a]\subseteq[0,1]$, and have minimum zero. At any legal query, the mean difference is at most $2a$, so the adaptive transcript KL divergence is at most $2Ta^2=1/8$. Include the internal random seed in the transcript; its common distribution adds no divergence. Pinsker gives total variation at most $1/4$. Decode $v$ from $-\operatorname{sign}(\widehat x)$ with a fixed tie rule. An incorrect sign implies gap at least $a$. The average testing error is at least $(1-1/4)/2=3/8$, proving the claim. A matching upper theorem is a separate primary result and is not the source of this lower argument.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A3 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

## References

[1] Fokkema, van der Hoeven, Lattimore and Mayo. Online Newton Method for Bandit Convex Optimisation. COLT 2024 extended abstract; full version arXiv:2406.06506v1.

https://arxiv.org/pdf/2406.06506

[2] Flaxman, Kalai and McMahan. Online Convex Optimization in the Bandit Setting: Gradient Descent without a Gradient. SODA 2005.

https://arxiv.org/abs/cs/0408007

[3] Carpentier, Rouyer, Tsybakov and Akhavan. Sharp Optimal Algorithm for Derivative-Free Stochastic Convex Optimization in One Dimension. arXiv:2607.12938v1, 2026.

https://arxiv.org/html/2607.12938v1

[4] Nived Rajaraman and Yanjun Han. The Price of Hidden Curvature: Improved Lower Bounds for Bandit Convex Optimization. arXiv:2607.18652v3, 2026-08-20.

https://arxiv.org/html/2607.18652v3
