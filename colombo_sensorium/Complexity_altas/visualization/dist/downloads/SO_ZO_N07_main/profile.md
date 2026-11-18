# Higher-order smooth convex optimization with independent value noise

**Setting ID.** `SO_ZO_N07_main`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Higher order holder operator; smoothness: Lipschitz gradient; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Independent noisy value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

### Admissible model

$f:\mathbb{R}^d\to\mathbb{R}$ is differentiable and satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$ for every $x,y\in\mathbb{R}^d$.

$f$ is globally convex and has a global minimizer $x_*\in B_2(x_0,R)$; $x_0$ and $R$ are known.

$\alpha>2$. Set $m=\lceil\alpha\rceil-1$ and $\gamma_\alpha=\alpha-m\in(0,1]$. The $m$th derivative of $f$ satisfies $\|D^mf(x)-D^mf(y)\|_{\mathrm{op}}\le H_\alpha\|x-y\|_2^{\gamma_\alpha}$ for every $x,y$ in the ambient space.

Derivative tensors use the Euclidean induced operator norm, the supremum of their absolute value over tuples of Euclidean unit vectors.

### Oracle interface

A query at $x_t\in \mathbb{R}^d$ returns one scalar $Y_t=f(x_t)+\xi_t$.

$\xi_t$ is i.i.d. centered noise with $\mathbb{E}\xi_t^2\le\sigma_v^2$, independent of the algorithmic seed and preceding observations. Its distribution is unknown; the algorithm must cover every noise law satisfying the stated bound.

Every observation is charged independently. No same-sample coupling, sample handle, or noiseless function value is supplied.

The public inputs are $d$, $\beta$, $R$, $\sigma_v$, $\alpha$, $H_\alpha$, $\varepsilon$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in \mathbb{R}^d}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

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

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\|x_*-x_0\|_2\le R$

$\sigma_v$: Upper bound on scalar observation-noise scale **Domain:** $\sigma_v\ge0$.

$\mathbb{E}\xi^2\le\sigma_v^2$; conditional-variance assumptions are interpreted with respect to the specified interaction history.

$\alpha$: Higher-order smoothness order **Domain:** $\alpha>2$.

Use $m=\lceil\alpha\rceil-1$ and $\gamma_\alpha=\alpha-m$ for the integer derivative order and its Hölder exponent.

$H_\alpha$: Hölder modulus of the highest derivative in the specified tensor norm **Domain:** $H_\alpha>0$.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$Q$: Smoothness accuracy ratio **Domain:** $Q>0$.

$Q=\beta R^2/\varepsilon$

$B_\alpha$: Ratio of high-order regularity to target accuracy **Domain:** $B_\alpha>0$.

$B_\alpha=H_\alpha R^\alpha/\varepsilon$

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $\mathbb{R}^d$.

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

$f_*=\inf_{x\in \mathbb{R}^d}f(x)$.

$Y_t,\xi_t,t$: Scalar-observation number, noise, and call index **Domain:** $Y_t,\xi_t\in\mathbb{R},\ t\in\mathbb{N}$.

Noise independence, distribution class and scale are fixed by this profile's oracle.

$\mathcal{F}_{t-1}$: The history before the current query **Domain:** The $\sigma$-algebra generated by the algorithm's seed and previous feedback.

The current query may depend on this history.

$\nabla f,\nabla^2f,D^jf$: Gradient, Hessian, and higher Fréchet derivatives **Domain:** $\nabla f\in\mathbb{R}^d,\ \nabla^2f\in\mathbb{R}^{d\times d}$; $D^jf$ is a $j$-linear form.

Used only at derivative orders and on regions where the model guarantees its existence.

$\|\cdot\|_{\mathrm{op}}$: Euclidean induced matrix or tensor operator norm **Domain:** Take the supremum over Euclidean unit input vectors of the corresponding order.

$\|T\|_{\mathrm{op}}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|$

$m,\gamma_\alpha$: Integer derivative order and Hölder exponent of the high-order regularity condition **Domain:** $m\ge2,\ 0<\gamma_\alpha\le1$.

$m=\lceil\alpha\rceil-1$, $\gamma_\alpha=\alpha-m$

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

$x_0$: Public initial point **Domain:** $x_0\in\mathbb{R}^d$.

Belongs to the feasible domain required by the model.

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

### R1 - Parameter regime N07.R1

**Region.** Fix $\alpha>2$; require $d\ge256$, $\beta,R,H_\alpha,\sigma_v>0$ and $0<\varepsilon\le c_\alpha\min\{H_\alpha R^\alpha,\beta R^2\}$. Set $Q=\beta R^2/\varepsilon$ and $B_\alpha=H_\alpha R^\alpha/\varepsilon$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Other quantified gap

**Lower bound.** B2

$$
\Omega_\alpha(d^2\sigma_v^2\varepsilon^{-2}\min\{\sqrt d,B_\alpha^{2/\alpha},Q\})
$$

**Upper bound.** B1, B3

$$
O_\alpha(d^2\sigma_v^2\varepsilon^{-2}\min\{B_\alpha^{2/(\alpha-1)},Q\}+d(1+Q))
$$

**Gap or comparison.** $O_\alpha(\min\{B_\alpha^{2/(\alpha-1)},Q\}/\min\{\sqrt d,B_\alpha^{2/\alpha},Q\}+\varepsilon^2(1+Q)/(d\sigma_v^2\min\{\sqrt d,B_\alpha^{2/\alpha},Q\}))$

### R2 - Parameter regime N07.R_curvature_matched

**Region.** Fix $\alpha>2$; require $d\ge256$, $\beta,R,H_\alpha,\sigma_v>0$ and $0<\varepsilon\le c_\alpha\min\{H_\alpha R^\alpha,\beta R^2\}$. Also require $Q\le\min\{\sqrt d,B_\alpha^{2/\alpha}\}$ and $d^2\sigma_v^2Q/\varepsilon^2\ge Cd(1+Q)$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Optimal

**Lower bound.** B2

$$
\Omega_\alpha(d^2\sigma_v^2 Q/\varepsilon^2)
$$

**Upper bound.** B3

$$
O(d^2\sigma_v^2 Q/\varepsilon^2)
$$

**Gap or comparison.** $O_\alpha(1)$

### R3 - Parameter regime N07.R_zero

**Region.** $\varepsilon\ge\beta R^2/2$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Optimal

**Lower bound.** B5

$$
0
$$

**Upper bound.** B4

$$
0
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Scalar observations follow the independent-noise, conditional-noise, or mixed-error law specified here; every repeated observation is charged separately.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - High-order randomized finite differences or ordinary smoothed gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O_\alpha(d^2\sigma_v^2 B_\alpha^{2/(\alpha-1)}/\varepsilon^2+d(1+Q))
$$

**Sources.** [1](https://arxiv.org/pdf/2610.05517v2)

**Conditions.** Fix $\alpha>2$ and $R,H_\alpha,\beta>0$. Tensors use the operator norm, and noise is independent, centered and variance bounded.

**Source location.** [1](https://arxiv.org/pdf/2610.05517v2) theorem: Theorem 4(a), $\tau=0$; pdf pages: 7

### B2 - Gaussian tests for higher-order smooth convex functions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_\alpha(d^2\sigma_v^2\varepsilon^{-2}\min\{\sqrt d,B_\alpha^{2/\alpha},Q\})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.05517v2)

**Conditions.** $d\ge256$, fixed $\alpha>2$ and $\sigma_v>0$, with $0<\varepsilon\le c_\alpha\min\{H_\alpha R^\alpha,\beta R^2\}$.

**Source location.** [1](https://arxiv.org/pdf/2610.05517v2) theorem: Theorem 5(a); pdf pages: 7

### B3 - High-order randomized finite differences or ordinary smoothed gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(d^2\sigma_v^2 Q/\varepsilon^2+d(1+Q))
$$

**Sources.** [1](https://arxiv.org/pdf/2610.05517v2)

**Conditions.** Use only gradient smoothness on the same instance class. When taking the minimum with a higher-order upper bound, each branch must satisfy its own assumptions.

**Source location.** [1](https://arxiv.org/pdf/2610.05517v2) theorem: Theorem 4(b), V=beta, PDF p.7; pdf pages: 7

### B4 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge \beta R^2/2$.

**Local argument.** A1

### B5 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge \beta R^2/2$.

**Local argument.** A1

## 5. Local arguments

### A1 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

## References

[1] Loginov, Dvinskikh, Tupitsa, Osmanov, Dorn and Gasnikov. Minimax Oracle Call Complexity, Rounds and Admissible Noise in Zeroth-Order Optimization of Highly Smooth Functions. arXiv:2610.05517v2, 2026-10-14.

https://arxiv.org/pdf/2610.05517v2
