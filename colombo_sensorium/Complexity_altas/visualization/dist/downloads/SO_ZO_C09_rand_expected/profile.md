# Goldstein stationarity with independent scalar noise

**Setting ID.** `SO_ZO_C09_rand_expected`

Single-objective optimization

Find an $(\rho,\varepsilon)$-Goldstein approximate stationary point of the population objective. The convex hull of Clarke subgradients within radius $\rho$ of the output must approach zero.

**Status.** Polynomial gap present

**TASK tags.** formulation: So goldstein stationarity; solution concept: Goldstein stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; initialization: Global initial gap; smoothness: Lipschitz function

**ORACLE tags.** access order: Zeroth-order interface; interface family: Independent noisy value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Goldstein stationarity

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find an $(\rho,\varepsilon)$-Goldstein approximate stationary point of the population objective. The convex hull of Clarke subgradients within radius $\rho$ of the output must approach zero.

### Admissible model

For every $x,y\in\mathbb{R}^d$, $|f(x)-f(y)|\le L\|x-y\|_2$.

$f_*:=\inf_{x\in\mathbb{R}^d}f(x)>-\infty$, and the given initial point $x_0$ satisfies $f(x_0)-f_*\le\Delta$.

### Oracle interface

A query at $x_t\in \mathbb{R}^d$ returns one scalar $Y_t=f(x_t)+\xi_t$.

Given the history $\mathcal{F}_{t-1}$ and current query, $\mathbb{E}[Y_t\mid\mathcal{F}_{t-1},x_t]=f(x_t)$ and $\mathbb{E}[(Y_t-f(x_t))^2\mid\mathcal{F}_{t-1},x_t]\le\sigma_v^2$ hold. Observations use fresh randomness and their distribution may depend on the query point; the same observation cannot be shared across locations.

Every observation is charged independently. No same-sample coupling, sample handle, or noiseless function value is supplied.

The public inputs are $d$, $L$, $\Delta$, $\rho$, $\varepsilon$, $\sigma_v$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

Let $\partial f(y)$ denote the Clarke subdifferential, and define $\partial_\rho f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\rho}\partial f(y)$. The base loss is $\ell(I,x)=\operatorname{dist}(0,\partial_\rho f(x))$ with tolerance $\varepsilon$; $\rho>0$ is independent of the accuracy.

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

$L$: Public upper bound on the objective Lipschitz constant **Domain:** $L>0$.

$|f(x)-f(y)|\le L\|x-y\|_2$ throughout the function domain specified in this profile.

$\Delta$: Known upper bound on the initial objective gap **Domain:** $\Delta\ge0$.

$f(x_0)-\inf_{x\in\mathbb{R}^d}f(x)\le\Delta$

$\rho$: Goldstein subdifferential neighborhood radius **Domain:** $\rho>0$.

It measures the neighborhood defining stationarity, not the radius of a query or feasible ball.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$\sigma_v$: Upper bound on scalar observation-noise scale **Domain:** $\sigma_v\ge0$.

$\mathbb{E}\xi^2\le\sigma_v^2$; conditional-variance assumptions are interpreted with respect to the specified interaction history.

$B_{\mathrm{raw}}$: Untruncated scale for the Goldstein lower bound **Domain:** $B_{\mathrm{raw}}\ge0$.

$B_{\mathrm{raw}}=\Delta\varepsilon/\rho$

$B_G$: Truncated hard-instance scale for the Goldstein lower bound **Domain:** $B_G\ge0$.

$B_G=\min\{\Delta\varepsilon/\rho,L^2\}$

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

$\partial f(x)$: Clarke subdifferential **Domain:** A nonempty compact convex subset at $x$ for a locally Lipschitz function, contained in $\mathbb{R}^d$.

Defined as the closed convex hull of gradient limits along differentiability points approaching $x$.

$\partial_\rho f(x)$: Goldstein neighborhood subdifferential **Domain:** $\rho>0$.

$\partial_\rho f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\rho}\partial f(y)$

$\operatorname{conv},\operatorname{dist}$: Convex hull and Euclidean distance **Domain:** Set operations.

$\operatorname{dist}(v,S)=\inf_{s\in S}\|v-s\|_2$

$Y_t,\xi_t,t$: Scalar-observation number, noise, and call index **Domain:** $Y_t,\xi_t\in\mathbb{R},\ t\in\mathbb{N}$.

Noise independence, distribution class and scale are fixed by this profile's oracle.

$\mathcal{F}_{t-1}$: The history before the current query **Domain:** The $\sigma$-algebra generated by the algorithm's seed and previous feedback.

The current query may depend on this history.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_0$: Public initial point **Domain:** $x_0\in\mathbb{R}^d$.

Belongs to the feasible domain required by the model.

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

### R1 - Parameter regime C09.R1

**Region.** $B_G=\min\{\Delta\varepsilon/\rho,L^2\}$, $\varepsilon^2\le cB_G$ and $d\ge C(B_G/\varepsilon^2)\log(2+B_G/\varepsilon^2)$, with $L,\Delta,\rho,\sigma_v>0$. The lower bound transfers from the exact-value hard subclass and contains no noise-amplitude factor.

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Polynomial gap

**Lower bound.** B2

$$
\Omega(dB_G/\varepsilon^2)
$$

**Upper bound.** B1

$$
O((\Delta+\rho L)(d^2\sigma_v^2/\rho^2+dL^2)/(\rho\varepsilon^3))
$$

**Gap or comparison.** $O((\Delta+\rho L)(d\sigma_v^2/\rho^2+L^2)/(\rho\varepsilon B_G))$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Scalar observations follow the independent-noise, conditional-noise, or mixed-error law specified here; every repeated observation is charged separately.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Smoothing with independent value noise and a nonconvex reduction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\frac{\Delta+\rho L}{\rho\varepsilon^3}\left(\frac{d^2\sigma_v^2}{\rho^2}+dL^2\right)\right)
$$

**Sources.** [1](https://arxiv.org/html/2605.06549v1)

**Conditions.** Includes independent additive value noise; the normalized leading term is $d^2\rho^{-3}\varepsilon^{-3}$.

**Source location.** [1](https://arxiv.org/html/2605.06549v1) theorem: Theorem 3.1, Assumption 1.1 and Eq. (4)

**Source location.** [1](https://arxiv.org/html/2605.06549v1) theorem: Theorem 3.1, Assumption 1.1 and Eq. (4); pdf pages: 6; printed pages: 6

### B2 - Exact-value Goldstein hard subclass

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(dB_G/\varepsilon^2)
$$

**Sources.** [2](https://arxiv.org/html/2610.19652v1) [3](https://arxiv.org/html/2609.00045v3) [4](https://arxiv.org/pdf/2610.00245v2) [5](https://arxiv.org/html/2610.17074v1)

**Conditions.** $B_G=\min\{\Delta\varepsilon/\rho,L^2\}$ and $\varepsilon^2\le cB_G,d\ge C(B_G/\varepsilon^2)\log(2+B_G/\varepsilon^2)$; no dependence on the noise magnitude is included.

**Local argument.** A1

**Source location.** [2](https://arxiv.org/html/2610.19652v1) theorem: Exact-oracle reduction in Corollary 10.7

**Source location.** [2](https://arxiv.org/html/2610.19652v1) theorem: Exact-oracle reduction in Corollary 10.7; pdf pages: 24; printed pages: 24

## 5. Local arguments

### A1 - Oracle and subclass transfers for nonconvex lower bounds

**Scope.** Each bound keeps the source's fixed cap, output convention, accuracy window, and lower-bound algorithm class. Dimension-free supremum statements remain distinct from fixed-dimension statements.

The registered lower bounds follow by exact simulation or class containment, with no added dimension factor.

For identical stochastic samples or identical finite-sum components, use the same exact-value hard function for every label. The oracle response is then exactly one source value, so the source's computational lower bound transfers one-for-one. When the target observes fresh additive Gaussian values, an exact-value algorithm can generate the independent Gaussian perturbations itself; an algorithm for that noisier interface would therefore contradict the stronger exact-value lower. The exact-value source cap $B=\min\{\beta\Delta,L^2\}$ and its high-dimensional window remain in force. A smooth-only class may choose the proof-only budget $L=\sqrt{\beta\Delta}$ inside the hard subclass; this does not add a public Lipschitz parameter.

The second-moment sample class is contained in each $r$-moment class for $1<r\le2$, by $(\mathbb EG^r)^{1/r}\le(\mathbb EG^2)^{1/2}$. Thus the source Goldstein statistical lower transfers to the larger heavy-tail class, but it does not establish a matching heavy-tail exponent. A composite class that includes $\psi=0$ contains the corresponding noncomposite hard family. With $X=\mathbb R^d$, the normal-cone residual is the unconstrained Goldstein residual. These embeddings support the registered composite and constrained-normal-cone lower bounds only where those model members are allowed; they do not automatically support a compact-set Frank--Wolfe-gap lower bound.

A value-and-gradient incremental oracle can simulate a selected-component value by discarding the gradient. Dense26 Theorem 3.1 consequently transfers its $\Omega(n+\sqrt n\,\beta\Delta/\varepsilon^2)$ lower, with $n\ge1024$ and the registered dimension window. The same stronger-oracle ordering transfers the Hessian-Lipschitz and higher-order-smooth first-order lower theorems to exact values. A second-order stationary output necessarily satisfies its first-order gradient requirement, so the first-order lower also limits that stronger task. If the theorem states that some sufficiently large finite dimension is hard, retain $\sup_{d\ge1}N^*(d,\varepsilon)$ or its explicit hard-dimension bound; do not present it as a result for every fixed $d$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [2](https://arxiv.org/html/2610.19652v1) [3](https://arxiv.org/html/2609.00045v3) [4](https://arxiv.org/pdf/2610.00245v2) [5](https://arxiv.org/html/2610.17074v1)

## References

[1] Chengchang Liu, Zongqi Wan, Haishan Ye and John C.S. Lui. Stochastic Non-Smooth Non-Convex Optimization with Decision-Dependent Distributions. arXiv:2605.06549v1, 2026-05-07.

https://arxiv.org/html/2605.06549v1

[2] Xia and Yuan. On Global Joint Lower Bounds in Zeroth-Order Nonconvex Optimization. arXiv:2610.19652v1, 2026-10-14.

https://arxiv.org/html/2610.19652v1

[3] Peng, Tang and Jia. Dense Weak Hiding: Closing Complexity Gaps in Nonconvex and PL Finite-Sum Optimization under Individual Smoothness. arXiv:2609.00045v3, 2026-10-10.

https://arxiv.org/html/2609.00045v3

[4] Zhang et al.. Matching Lower Bounds for Randomized First-Order Methods in Hessian-Lipschitz Nonconvex Optimization. arXiv:2610.00245v2, 2026-10-19.

https://arxiv.org/pdf/2610.00245v2

[5] Zhang et al.. Matching Randomized First-Order Bounds for Higher-Order Smooth Nonconvex Optimization. arXiv:2610.17074v1, 2026.

https://arxiv.org/html/2610.17074v1
