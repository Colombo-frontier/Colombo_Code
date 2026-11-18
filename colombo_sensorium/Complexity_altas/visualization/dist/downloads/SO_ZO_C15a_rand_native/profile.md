# Ball-restricted queries and a local objective gap: Goldstein stationarity

**Setting ID.** `SO_ZO_C15a_rand_native`

Single-objective optimization

Find an $(\rho,\varepsilon)$-Goldstein approximate stationary point of the population objective. The convex hull of Clarke subgradients within radius $\rho$ of the output must approach zero.

**Status.** Bounds missing; Infeasible task

**TASK tags.** formulation: So goldstein stationarity; solution concept: Goldstein stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; initialization: Local initial gap; stochastic model: Sample lipschitz second moment

**ORACLE tags.** access order: Zeroth-order interface; interface family: Reusable sample value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Goldstein stationarity

**GUARANTEE tags.** aggregation: Per instance; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find an $(\rho,\varepsilon)$-Goldstein approximate stationary point of the population objective. The convex hull of Clarke subgradients within radius $\rho$ of the output must approach zero.

The output is restricted to $X=B_2(x_0,R)$, while stationarity is defined for the full-space function.

### Admissible model

$f(x)=\mathbb{E}[F(x;Z)]$. The sample value at a reference point is integrable. Sample functions satisfy $|F(x;Z)-F(y;Z)|\le G(Z)\|x-y\|_2$ and $\mathbb{E}[G(Z)^2]\le L^2$ throughout $\mathbb{R}^d$; samplewise convexity is not required.

Let $X=B_2(x_0,R)$, and assume only the local objective-gap bound $f(x_0)-\min_{x\in X}f(x)\le\Delta$. The function remains defined throughout the ambient space; existence of a point in the output ball meeting the ordinary stationarity threshold is not additionally promised.

### Oracle interface

A new sample handle corresponds to an independent draw of the hidden sample $Z$. Given its handle and $x\in X=B_2(x_0,R)$, the interface returns the exact sample value $F(x;Z)$. The algorithm observes only handles and numerical values, not the underlying sample data or the complete sample function.

Sample handles may be retained for arbitrarily many paid evaluations. Responses using the same handle come from the same function, and distinct handles are independent.

The public inputs are $d$, $L$, $\Delta$, $\rho$, $R$, $\varepsilon$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in X=B_2(x_0,R)$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

Let $\partial f(y)$ denote the Clarke subdifferential, and define $\partial_\rho f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\rho}\partial f(y)$. The base loss is $\ell(I,x)=\operatorname{dist}(0,\partial_\rho f(x))$ with tolerance $\varepsilon$; $\rho>0$ is independent of the accuracy.

### Resource accounting

One scalar sample-function value costs $1$ call; two points with the same sample handle or Markov state cost $2$ calls. Batches, initialization and repeated visits are charged per value. An empty handle supplies no free instance information.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The error requirement is $\Pr(\ell(I,\widehat{x})\le \varepsilon)\ge2/3$.

Probability is over both the algorithm's seed and all feedback randomness, after fixing the instance and admissible environment law.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$L$: Moment budget of the sample Lipschitz coefficient **Domain:** $L>0$.

$\mathbb{E}[G(Z)^2]\le L^2$

$\Delta$: Known upper bound on the initial objective gap **Domain:** $\Delta\ge0$.

$f(x_0)-\min_{x\in B_2(x_0,R)}f(x)\le\Delta$

$\rho$: Goldstein subdifferential neighborhood radius **Domain:** $\rho>0$.

It measures the neighborhood defining stationarity, not the radius of a query or feasible ball.

$R$: Radius of the fixed query and output ball **Domain:** $R>0$.

$X=B_2(x_0,R)$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $X=B_2(x_0,R)$.

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

$f$: Population objective on the full ambient space **Domain:** $f:\mathbb{R}^d\to\mathbb{R}$.

Initialization controls only the minimum over $X=B_2(x_0,R)$; the global infimum need not be finite.

$\partial f(x)$: Clarke subdifferential **Domain:** A nonempty compact convex subset at $x$ for a locally Lipschitz function, contained in $\mathbb{R}^d$.

Defined as the closed convex hull of gradient limits along differentiability points approaching $x$.

$\partial_\rho f(x)$: Goldstein neighborhood subdifferential **Domain:** $\rho>0$.

$\partial_\rho f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\rho}\partial f(y)$

$\operatorname{conv},\operatorname{dist}$: Convex hull and Euclidean distance **Domain:** Set operations.

$\operatorname{dist}(v,S)=\inf_{s\in S}\|v-s\|_2$

$Z,F(\cdot;Z)$: Hidden sample and its associated sample function **Domain:** Samples lie in an admissible probability space; each sample function is real-valued on the declared domain.

The population objective is the expectation under the sample distribution or stationary distribution.

$G(Z)$: Random sample Lipschitz coefficient **Domain:** $G(Z)\ge0$.

The model's difference inequality holds for each sample, with the moment budget fixed as specified here.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=X=B_2(x_0,R)$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_0$: Public initial point **Domain:** $x_0\in\mathbb{R}^d$.

Belongs to the feasible domain required by the model.

$c_R,C_R,C_0$: Universal constant in the radius window and sufficient large-radius condition **Domain:** $0<c_R\le C_R<\infty,\ C_0>0$.

The lower bound guarantees only the existence of a hard radius in $[c_R\Delta/\varepsilon,C_R\Delta/\varepsilon]$; all constants are fixed as in the source theorem.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar sample-function value; two points using the same handle cost two calls

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar sample-function value; two points using the same handle cost two calls

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - radius supremum cost

$$
C^\star_{v,\pi,\mathrm{rad}}(\varepsilon;\theta)=\sup_{R\ \mathrm{in\ the\ declared\ window}}C^\star_{v,\pi}(\varepsilon;\theta,R)
$$

**Definition.** Oracle complexity, with a supremum over the stated localization-radius window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime C15a.R2

**Region.** $L>\varepsilon$ and $0<R<\Delta/\varepsilon$. The model controls only the objective gap within the ball and does not additionally guarantee a Goldstein stationary point in the ball satisfying the required threshold.

**Quantity.** Q1

**Resource.** One scalar sample-function value; two points using the same handle cost two calls

**Status.** Infeasible task

**Lower bound.** B3

$$
+\infty
$$

### R2 - Additional theorem window

**Region.** $R\ge C_0(\Delta/\varepsilon+\rho)$ and $0<\varepsilon\le L$. This per-instance upper bound requires the specified radius to satisfy the stated sufficient condition.

**Quantity.** Q2

**Resource.** One scalar sample-function value; two points using the same handle cost two calls

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(1+dL^2\Delta/(\rho\varepsilon^3))
$$

### R3 - Additional theorem window

**Region.** $\varepsilon\le cL$, $\Delta\ge C\rho\varepsilon$ and $d\ge C[1+\log(2+\Delta L^2/(\rho\varepsilon^3))]$. There exists a hard radius satisfying $R\in[c_R\Delta/\varepsilon,C_R\Delta/\varepsilon]$. The lower bound is not asserted for every radius in this window.

**Quantity.** Q3

**Resource.** Oracle complexity, with a supremum over the stated localization-radius window

**Status.** Upper bound missing

**Lower bound.** B2

$$
\sup_{R\in[c_R\Delta/\varepsilon,C_R\Delta/\varepsilon]}N^*(R,\varepsilon)=\Omega(dL^2\Delta/(\rho\varepsilon^3))
$$

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Preserve sample handles and their reuse limits. Each queried point returns one sample value; sample data and sample gradients are not available for free.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Two-point nonconvex reduction within the local ball

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(1+dL^2\Delta/(\rho\varepsilon^3))
$$

**Sources.** [1](https://arxiv.org/html/2610.00275v2)

**Conditions.** $R\ge C_0(\Delta/\varepsilon+\rho)$ and $0<\varepsilon\le L$. This per-instance upper bound requires the specified radius to satisfy the stated sufficient condition.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [1](https://arxiv.org/html/2610.00275v2) theorem: Proposition A.1

**Source location.** [1](https://arxiv.org/html/2610.00275v2) theorem: Proposition A.1; pdf pages: 19; printed pages: 19

### B2 - Sample hard family within a ball, or a linear function without a stationary point

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(dL^2\Delta/(\rho\varepsilon^3))
$$

**Sources.** [1](https://arxiv.org/html/2610.00275v2)

**Conditions.** $\varepsilon\le cL$, $\Delta\ge C\rho\varepsilon$ and $d\ge C[1+\log(2+\Delta L^2/(\rho\varepsilon^3))]$. There exists a hard radius satisfying $R\in[c_R\Delta/\varepsilon,C_R\Delta/\varepsilon]$. The lower bound is not asserted for every radius in this window.

**Guarantee conversion.** The source guarantees a hard radius somewhere in $R\asymp\Delta/\varepsilon$. Retain the supremum over that radius window; do not combine it with an upper bound for an arbitrary fixed radius.

**Source location.** [1](https://arxiv.org/html/2610.00275v2) theorem: Corollary 4.2

**Source location.** [1](https://arxiv.org/html/2610.00275v2) theorem: Corollary 4.2; pdf pages: 7; printed pages: 7

### B3 - Sample hard family within a ball, or a linear function without a stationary point

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N^*=+\infty
$$

**Sources.** [1](https://arxiv.org/html/2610.00275v2)

**Conditions.** Existence of a stationary point is not promised; $L>\varepsilon$ and $0<R<\Delta/\varepsilon$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [1](https://arxiv.org/html/2610.00275v2) theorem: Proposition 4.3

## References

[1] Zhang et al.. Joint Lower Bounds for Zeroth-Order Nonconvex Optimization on Euclidean Balls. arXiv:2610.00275v2, 2026-10-19.

https://arxiv.org/html/2610.00275v2
