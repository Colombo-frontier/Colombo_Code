# Goldstein stationarity of Lipschitz objectives with exact values

**Setting ID.** `SO_ZO_C06`

Single-objective optimization

Find an $(\rho,\varepsilon)$-Goldstein approximate stationary point of the population objective. The convex hull of Clarke subgradients within radius $\rho$ of the output must approach zero.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Other quantified gap

The deterministic view also has a quantified gap with exponential dependence on dimension. Its explicit form is stated below; the polynomial badge describes the randomized windows.

**Additional gap: Deterministic / Parameter regime C07.R1.** $O\!\left(\left[1+\left(\frac{2\Delta}{\rho\varepsilon}+1\right)\left(1+\frac{4L}{\varepsilon}\right)^d\right]\left(\frac{2\varepsilon}{L-\varepsilon}\right)^{(d-2)/2}\right)$

**TASK tags.** formulation: So goldstein stationarity; solution concept: Goldstein stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; initialization: Global initial gap; smoothness: Lipschitz function

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Goldstein stationarity

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find an $(\rho,\varepsilon)$-Goldstein approximate stationary point of the population objective. The convex hull of Clarke subgradients within radius $\rho$ of the output must approach zero.

### Admissible model

For every $x,y\in\mathbb{R}^d$, $|f(x)-f(y)|\le L\|x-y\|_2$.

$f_*:=\inf_{x\in\mathbb{R}^d}f(x)>-\infty$, and the given initial point $x_0$ satisfies $f(x_0)-f_*\le\Delta$.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

The public inputs are $d$, $L$, $\Delta$, $\rho$, $\varepsilon$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

Let $\partial f(y)$ denote the Clarke subdifferential, and define $\partial_\rho f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\rho}\partial f(y)$. The base loss is $\ell(I,x)=\operatorname{dist}(0,\partial_\rho f(x))$ with tolerance $\varepsilon$; $\rho>0$ is independent of the accuracy.

### Resource accounting

Each scalar function value or noisy observation costs $1$ call. Every location in a multipoint finite difference, every initialization query, and every reference observation is charged.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

#### Randomized expected

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. Require $\mathbb{E}[\ell(I,\widehat{x})]\le \varepsilon$, fixing the instance before averaging over algorithmic and feedback randomness.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

**Output qualification.** Random selection among previously queried points is permitted, subject to the declared success guarantee.

#### Deterministic

Only deterministic strategies are allowed. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The requirement $\ell(I,\widehat{x})\le \varepsilon$ holds deterministically for each instance.

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

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_0$: Public initial point **Domain:** $x_0\in\mathbb{R}^d$.

Belongs to the feasible domain required by the model.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Randomized expected

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime C06.R1

**Region.** $B_G=\min\{\Delta\varepsilon/\rho,L^2\}$, $\varepsilon^2\le cB_G$ and $d\ge C(B_G/\varepsilon^2)\log(2+B_G/\varepsilon^2)$. Also require $\Delta\varepsilon/\rho\le L^2$.

**Views.** Randomized expected

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Polynomial gap

**Lower bound.** B2

$$
\Omega(d\Delta/(\rho\varepsilon))
$$

**Upper bound.** B1

$$
O(dL^2\Delta/(\rho\varepsilon^3))
$$

**Gap or comparison.** $O(L^2/\varepsilon^2)$

### R2 - Parameter regime C06.R2

**Region.** $B_G=\min\{\Delta\varepsilon/\rho,L^2\}$, $\varepsilon^2\le cB_G$ and $d\ge C(B_G/\varepsilon^2)\log(2+B_G/\varepsilon^2)$. Also require $\Delta\varepsilon/\rho>L^2$.

**Views.** Randomized expected

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Polynomial gap

**Lower bound.** B2

$$
\Omega(dL^2/\varepsilon^2)
$$

**Upper bound.** B1

$$
O(dL^2\Delta/(\rho\varepsilon^3))
$$

**Gap or comparison.** $O(\Delta/(\rho\varepsilon))$

### R3 - Parameter regime C07.R1

**Region.** $d\ge3$, $\rho<\Delta/L$ and $0<\varepsilon<L/3$. The strategy is deterministic, and both queries and outputs may lie anywhere in the ambient space.

**Views.** Deterministic

**Quantity.** Q2

**Resource.** One scalar function value or observation

**Status.** Other quantified gap

**Lower bound.** B4

$$
\Omega(((L-\varepsilon)/(2\varepsilon))^{(d-2)/2})
$$

**Upper bound.** B3

$$
1+(2\Delta/(\rho\varepsilon)+1)(1+4L/\varepsilon)^d
$$

**Gap or comparison.** $O\!\left(\left[1+\left(\frac{2\Delta}{\rho\varepsilon}+1\right)\left(1+\frac{4L}{\varepsilon}\right)^d\right]\left(\frac{2\varepsilon}{L-\varepsilon}\right)^{(d-2)/2}\right)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Online-to-nonconvex conversion with randomized two-point smoothing

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized expected

**Witness or lower-bound scope.** Randomized witness

$$
O(dL^2\Delta/(\rho\varepsilon^3))
$$

**Sources.** [1](https://www.jmlr.org/papers/volume25/23-1159/23-1159.pdf) [5](https://arxiv.org/html/2610.00275v2)

**Conditions.** The objective is globally $L$-Lipschitz, its initial gap is at most $\Delta$, and the specified Goldstein radius is $\rho$. The source controls the expected residual; constant rescaling also yields a fixed success probability.

**Local argument.** A1

**Source location.** [1](https://www.jmlr.org/papers/volume25/23-1159/23-1159.pdf) theorem: Theorem 5, specialized to a single deterministic sample; pdf pages: 5; printed pages: 5

### B2 - Randomized hard family for Goldstein stationarity

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized expected

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(dB_G/\varepsilon^2),\quad B_G=\min\{\Delta\varepsilon/\rho,L^2\}
$$

**Sources.** [2](https://arxiv.org/html/2610.19652v1)

**Conditions.** $\varepsilon^2\le cB_G$; $d\ge C(B_G/\varepsilon^2)\log(2+B_G/\varepsilon^2)$.

**Source location.** [2](https://arxiv.org/html/2610.19652v1) theorem: Corollary 10.7

**Source location.** [2](https://arxiv.org/html/2610.19652v1) theorem: Corollary 10.7; pdf pages: 24; printed pages: 24

### B3 - Deterministic directional-grid descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1+(2\Delta/(\rho\varepsilon)+1)(1+4L/\varepsilon)^d
$$

**Sources.** [3](https://arxiv.org/html/2609.38082v1)

**Conditions.** Deterministic directional-grid descent; $\rho,\varepsilon>0$.

**Source location.** [3](https://arxiv.org/html/2609.38082v1) theorem: Theorem 2.3

**Source location.** [3](https://arxiv.org/html/2609.38082v1) theorem: Theorem 2.3; pdf pages: 7; printed pages: 7

### B4 - Exponential hard family for local oracles

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega\!\left(((L-\varepsilon)/(2\varepsilon))^{(d-2)/2}\right)
$$

**Sources.** [3](https://arxiv.org/html/2609.38082v1) [4](https://arxiv.org/html/2609.23837v1)

**Conditions.** $d\ge3$, $\rho<\Delta/L$ and $0<\varepsilon<L/3$. The hard construction limits local information and therefore covers deterministic algorithms receiving only exact scalar values.

**Source location.** [3](https://arxiv.org/html/2609.38082v1) theorem: DY26, Theorem 2.2; related result in Kdet26, Theorem 3.1

**Source location.** [3](https://arxiv.org/html/2609.38082v1) theorem: DY26, Theorem 2.2; related result in Kdet26, Theorem 3.1; pdf pages: 6; printed pages: 6

**Source location.** [4](https://arxiv.org/html/2609.23837v1) theorem: DY26, Theorem 2.2; related result in Kdet26, Theorem 3.1

**Source location.** [4](https://arxiv.org/html/2609.23837v1) theorem: DY26, Theorem 2.2; related result in Kdet26, Theorem 3.1; pdf pages: 3; printed pages: 3

## 5. Local arguments

### A1 - Goldstein-to-gradient and deterministic-sample specializations

**Scope.** Global Lipschitz/sample-moment assumptions of the cited two-point theorem; the stated same-sample access and scalar charging convention.

For a $\beta$-smooth mean, a Goldstein residual at radius $\rho$ controls gradient norm by an additive $\beta\rho$. Choosing $\rho$ proportional to $\varepsilon/\beta$ gives the registered $O(dL^2\beta\Delta/\varepsilon^4)$ smooth upper.

Every gradient $\nabla f(y)$ for $\|y-x\|\le\rho$ differs from $\nabla f(x)$ by at most $\beta\rho$. The same holds for every vector in their convex hull. Therefore $\|\nabla f(x)\|\le\operatorname{dist}(0,\partial_\rho f(x))+\beta\rho$. Apply the source Goldstein algorithm at residual tolerance $\varepsilon/2$ and $\rho=\varepsilon/(2\beta)$, retaining the source's nontrivial accuracy window. Its $O(dL^2\Delta/(\rho\varepsilon^3))$ bound becomes the displayed smooth rate. Each paired estimator costs two scalar calls.

A single deterministic sample function is a legal specialization of the stochastic two-point model; the resulting algorithm can still be randomized. This gives the exact-value Goldstein upper. At moment exponent $r=2$, the heavy-tail stationarity model coincides with the second-moment model. Choosing the auxiliary smoothing radius $h=\min\{\rho/2,\Delta/L\}$ controls initial smoothing error by the original gap scale and avoids inserting an artificial $\Delta+\rho L$ term into that bound.

For the bounded-query smooth variant, use the source's Goldstein algorithm with tolerance $\varepsilon/2$ and the same auxiliary radius. Its query-domain requirement becomes $R\ge C(\Delta/\varepsilon+\varepsilon/\beta)$. Retain its native success probability and the additive startup term; a success guarantee of $1/2$ is not silently changed to $2/3$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://www.jmlr.org/papers/volume25/23-1159/23-1159.pdf) [5](https://arxiv.org/html/2610.00275v2)

## References

[1] Kornowski and Shamir. An Algorithm with Optimal Dimension-Dependence for Zero-Order Nonsmooth Nonconvex Stochastic Optimization. JMLR 25(122):1--14, 2024.

https://www.jmlr.org/papers/volume25/23-1159/23-1159.pdf

[2] Xia and Yuan. On Global Joint Lower Bounds in Zeroth-Order Nonconvex Optimization. arXiv:2610.19652v1, 2026-10-14.

https://arxiv.org/html/2610.19652v1

[3] Yixi Ding and Ya-Xiang Yuan. Exponential Deterministic Query Complexity of Goldstein Stationarity. arXiv:2609.38082v1, 2026-09-29.

https://arxiv.org/html/2609.38082v1

[4] Guy Kornowski. The Exponential Price of Determinism in Nonsmooth Nonconvex Optimization. arXiv:2609.23837v1, 2026.

https://arxiv.org/html/2609.23837v1

[5] Zhang et al.. Joint Lower Bounds for Zeroth-Order Nonconvex Optimization on Euclidean Balls. arXiv:2610.00275v2, 2026-10-19.

https://arxiv.org/html/2610.00275v2
