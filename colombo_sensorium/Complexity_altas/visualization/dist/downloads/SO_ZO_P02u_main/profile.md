# Strongly convex population objective with a uniform sample Lipschitz bound: at most two values per sample

**Setting ID.** `SO_ZO_P02u_main`

Single-objective optimization

Minimize $f$ globally over $B_2(0,R)$ and return a point with small objective gap.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; smoothness: Sample function lipschitz as; structure: Expectation of sample functions

**ORACLE tags.** access order: Zeroth-order interface; interface family: Same sample paired value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $B_2(0,R)$ and return a point with small objective gap.

### Admissible model

Each sample function $F(\cdot;Z)$ is convex on $B_2(0,R)$ and satisfies $\mathbb{E}|F(0;Z)|<\infty$, so $f(x)=\mathbb{E}[F(x;Z)]$ is well defined. The optimization domain is $B_2(0,R)$.

For almost every sample, $|F(x;Z)-F(y;Z)|\le L\|x-y\|_2$ holds for all $x,y$ in the ball.

The population objective $f$ is $\mu$-strongly convex on the optimization ball. The statistical subregion assumes $L\ge2\mu R$.

### Oracle interface

A new sample handle corresponds to an independent draw of the hidden sample $Z$. Given its handle and $x\in B_2(0,R)$, the interface returns the exact sample value $F(x;Z)$. The algorithm observes only handles and numerical values, not the underlying sample data or the complete sample function.

At most two paid evaluations are allowed per handle; the second point may depend on the first response. Distinct handles are independent.

Projection and the stated proximal operations over known geometry are free.

The public inputs are $d$, $L$, $\mu$, $R$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in B_2(0,R)$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in B_2(0,R)}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

One scalar sample-function value costs $1$ call; two points with the same sample handle or Markov state cost $2$ calls. Batches, initialization and repeated visits are charged per value. An empty handle supplies no free instance information.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. Require $\mathbb{E}[\ell(I,\widehat{x})]\le \varepsilon$, fixing the instance before averaging over algorithmic and feedback randomness.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$L$: Moment budget of the sample Lipschitz coefficient **Domain:** $L>0$.

$G(Z)\le L$ almost surely.

$\mu$: Public lower bound on the strong-convexity modulus **Domain:** $\mu>0$.

$R$: Feasible-ball radius **Domain:** $R>0$.

The output must belong to $B_2(0,R)$; the query radius is specified separately in the interface.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

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

$f,f_*$: Population objective and its optimal value **Domain:** $f:\mathcal{X}_{\mathrm{fun}}\to\mathbb{R}$.

$f_*=\inf_{x\in B_2(0,R)}f(x)$.

$Z,F(\cdot;Z)$: Hidden sample and its associated sample function **Domain:** Samples lie in an admissible probability space; each sample function is real-valued on the declared domain.

The population objective is the expectation under the sample distribution or stationary distribution.

$G(Z)$: Random sample Lipschitz coefficient **Domain:** $G(Z)\ge0$.

The model's difference inequality holds for each sample, with the moment budget fixed as specified here.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=B_2(0,R)$ and $\mathcal{X}=B_2(0,R)$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$h,K$: Smoothing step size and number of projected iterations **Domain:** $0<h<R,\ K\in\mathbb{N}$.

Each iteration obtains two values, with $T=2K$; the smoothing-error term is $2hL$.

$\mathfrak R_T$: Optimal worst-case expected objective gap under a fixed scalar budget **Domain:** $T\in\mathbb{N}_0$.

$\mathfrak R_T=\inf_{\mathcal{A}:N\le T}\sup_I\mathbb{E}[f(\widehat{x})-f_*]$

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

### R1 - Parameter regime P02u.R1

**Region.** $L\ge2\mu R$, $d\ge1$ and $0<\varepsilon\le c\mu R^2$. Sample functions are almost surely $L$-Lipschitz on the ball, and their expectation is $\mu$-strongly convex.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(dL^2/(\mu\varepsilon))
$$

### R2 - Parameter regime P02u.R_zero

**Region.** $\varepsilon\ge LR$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Optimal

**Lower bound.** B3

$$
0
$$

**Upper bound.** B2

$$
0
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Preserve sample handles and their reuse limits. Each queried point returns one sample value; sample data and sample gradients are not available for free.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Same-sample two-point smoothing and weighted projected SGD

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathbb{E}[f(\widehat{x})-f_*]\le\frac{4dL^2}{\mu(K+1)}+2hL,\qquad T=2K
$$

**Sources.** [1](https://jmlr.org/papers/volume18/16-632/16-632.pdf)

**Conditions.** Samples are convex on the feasible ball and almost surely $L$-Lipschitz; the population objective is $\mu$-strongly convex. Use $K$ projected iterations in the shrunken ball, with $0<h<R$ and $T=2K$.

**Local argument.** A2

### B2 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge LR$.

**Local argument.** A3

### B3 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge LR$.

**Local argument.** A3

## 5. Local arguments

### A1 - Ball smoothing and the same-sample directional moment

**Scope.** A fresh sample each round; the same sample supplies both values; sample Lipschitz modulus $G$ on the stated query neighborhood; $\mathbb E G^r\le L^r$, $1<r\le2$.

With ball smoothing $f_h(x)=\mathbb E_{U\sim\operatorname{Unif}(B_2)}f(x+hU)$ and a sphere direction $u$,
$$g_h(x)=\frac d{2h}[F(x+hu;Z)-F(x-hu;Z)]u,\quad\mathbb E g_h=\nabla f_h,\quad\mathbb E\|g_h\|^r\le(\sqrt{2d}L)^r.$$
For $r=2$, the bound is $2dL^2$.

For each fixed sample, the scalar difference $a(u)=F(x+hu;Z)-F(x-hu;Z)$ is odd on the sphere, hence has mean zero, and has Lipschitz constant at most $2hG$. Sphere Poincare gives $\mathbb E_u a(u)^2\le4h^2G^2/(d-1)$ for $d\ge2$. Thus $\mathbb E_u\|g_h\|^2\le d^2G^2/(d-1)\le2dG^2$; for $d=1$ the difference quotient is directly bounded by $G$. Apply Jensen only to the direction expectation and then integrate over the sample:
$$\mathbb E_{Z,u}\|g_h\|^r\le\mathbb E_Z(\mathbb E_u\|g_h\|^2)^{r/2}\le(2d)^{r/2}\mathbb E G^r.$$
No second moment of $G$ is needed when $r<2$. The divergence theorem for ball convolution gives the unbiasedness identity. Integrability follows from the Lipschitz difference bound. Convexity gives $f_h\ge f$, and $|f_h-f|\le hL$; mean strong convexity is preserved on the region where every translated point satisfies it. All statements hold conditionally on the past when the next sample and direction are fresh. Reusing an old adaptively explored sample does not automatically preserve this conditional moment calculation.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://jmlr.org/papers/volume18/16-632/16-632.pdf)

### A2 - Projected optimization with same-sample two-point values

**Scope.** Optimization/output in $B_2(R)$; all two-point queries remain in the prescribed ball; mean strong convexity suffices. A uniformly sampled finite-sum component is also a valid fresh sample.

For a $\mu$-strongly-convex mean with $\mathbb E G^2\le L^2$, $K$ rounds and $T=2K$ scalar calls give
$$\mathbb E[f(\bar x_K)-f_*]\le\frac{4dL^2}{\mu(K+1)}+2hL.$$
The merely convex branch uses $O(d(LR/\varepsilon)^2)$ values.

Run the paired estimator on $K_h=B_2(R-h)$ and let $x_{h,*}$ minimize $f_h$ there. The shrinkage comparator $y=(1-h/R)x_*$ gives $f_h(y)\le f_*+2hL$. Set $V=2dL^2$, $\eta_t=2/[\mu(t+1)]$, and $D_t=\mathbb E\|x_t-x_{h,*}\|^2$. Projection and strong convexity yield
$$\mathbb E[f_h(x_t)-f_h(x_{h,*})]\le\frac{\mu(t-1)}4D_t-\frac{\mu(t+1)}4D_{t+1}+\frac{V}{\mu(t+1)}.$$
Multiply by $t$, telescope, and average with weights $2t/[K(K+1)]$. The initial distance coefficient is zero and the last is nonpositive, giving $2V/[\mu(K+1)]$. Add the comparator error. For expected accuracy choose, for example, $h=\varepsilon/(8L)$ and $K+1\ge8dL^2/(\mu\varepsilon)$. For success probability $2/3$, use $h=\varepsilon/(12L)$ and $K+1\ge24dL^2/(\mu\varepsilon)$, making the expected nonnegative gap at most $\varepsilon/3$ before Markov.

For convex objectives, the projected averaging recursion with step $R/\sqrt{VK}$ gives expected optimization error at most $R\sqrt{V/K}$, plus the same smoothing/shrinkage error. Uniform component sampling makes the estimator unbiased for the finite-sum mean and costs exactly two selected-component values per round. Neither the oracle nor the components need be stochastic in that case; the algorithm supplies the randomness. These bounds also hold under an almost-sure Lipschitz promise, since it implies the required second moment. The Gaussian lower construction in the separate lower lemma does not acquire that stronger promise.

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

[1] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. JMLR 18(52):1--11, 2017.

https://jmlr.org/papers/volume18/16-632/16-632.pdf
