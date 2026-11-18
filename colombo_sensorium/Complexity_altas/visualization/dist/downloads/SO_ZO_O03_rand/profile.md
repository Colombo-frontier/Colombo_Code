# Exact comparison feedback for smooth nonconvex first-order stationarity

**Setting ID.** `SO_ZO_O03_rand`

Single-objective optimization

Find an approximate first-order stationary point of the population objective $f$: an output point with sufficiently small gradient norm. The mathematical object is $\nabla f$, and information is acquired through the zeroth-order interface specified below.

**Status.** Fully optimal

**TASK tags.** formulation: First order stationarity; solution concept: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; initialization: Global initial gap; smoothness: Lipschitz gradient

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact comparison; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: First order stationarity

**GUARANTEE tags.** aggregation: Per instance; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find an approximate first-order stationary point of the population objective $f$: an output point with sufficiently small gradient norm. The mathematical object is $\nabla f$, and information is acquired through the zeroth-order interface specified below.

### Admissible model

$f:\mathbb{R}^d\to\mathbb{R}$ is differentiable and satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$ for every $x,y\in\mathbb{R}^d$.

$f_*:=\inf_{x\in\mathbb{R}^d}f(x)>-\infty$, and the given initial point $x_0$ satisfies $f(x_0)-f_*\le\Delta$.

### Oracle interface

Any finite point pair $(x,y)\in\mathbb{R}^d\times\mathbb{R}^d$ may be queried, returning $\operatorname{sign}(f(x)-f(y))\in\{-1,0,1\}$. Equal values produce zero. Neither the magnitude of the difference nor either function value is revealed.

The public inputs are $d$, $\beta$, $\Delta$, $\varepsilon$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=\|\nabla f(x)\|_2$ with tolerance $\varepsilon>0$. Any theorem for squared gradient norms must first be converted to this norm scale.

### Resource accounting

One point-pair comparison costs $1$ call. Every repeated comparison and every comparison in a line search is charged. The budget $T$ counts scalar comparison replies.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The error requirement is $\Pr(\ell(I,\widehat{x})\le \varepsilon)\ge2/3$.

Probability is over the algorithm's random seed only.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$\Delta$: Known upper bound on the initial objective gap **Domain:** $\Delta\ge0$.

$f(x_0)-\inf_{x\in\mathbb{R}^d}f(x)\le\Delta$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$K$: Dimensionless iteration scale for smooth stationarity **Domain:** $K\ge0$.

$K=\beta\Delta/\varepsilon^2$

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

$\nabla f,\nabla^2f,D^jf$: Gradient, Hessian, and higher Fréchet derivatives **Domain:** $\nabla f\in\mathbb{R}^d,\ \nabla^2f\in\mathbb{R}^{d\times d}$; $D^jf$ is a $j$-linear form.

Used only at derivative orders and on regions where the model guarantees its existence.

$\|\cdot\|_{\mathrm{op}}$: Euclidean induced matrix or tensor operator norm **Domain:** Take the supremum over Euclidean unit input vectors of the corresponding order.

$\|T\|_{\mathrm{op}}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|$

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

**Definition.** One binary comparison reply

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One binary comparison reply

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime O03.R1

**Region.** $K=\beta\Delta/\varepsilon^2$, $\varepsilon^2\le c\beta\Delta$ and $d\ge CK\log(2+K)$; the oracle provides exact comparisons throughout the ambient space.

**Quantity.** Q1

**Resource.** One binary comparison reply

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(d\beta\Delta/\varepsilon^2)
$$

**Upper bound.** B3

$$
O(d\beta\Delta/\varepsilon^2)
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Comparison-based gradient estimation or randomized three-point descent

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(d\beta\Delta\varepsilon^{-2}\log(2d))
$$

**Sources.** [3](https://arxiv.org/html/2405.11454v1)

**Conditions.** The expression on source PDF p. 10 is $O(L\Delta n\log n/\epsilon^2)$; each point-pair comparison costs one call.

**Source location.** [3](https://arxiv.org/html/2405.11454v1) theorem: Theorem 4

**Source location.** [3](https://arxiv.org/html/2405.11454v1) theorem: Theorem 4; pdf pages: 10; printed pages: 10

### B2 - Reduction of an exact-value nonconvex hard family to the comparison interface

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\beta\Delta/\varepsilon^2)
$$

**Sources.** [2](https://arxiv.org/html/2610.19652v1) [4](https://arxiv.org/html/2610.00345v1)

**Conditions.** Use the exact-value hard subclass in XY26 with additional Lipschitz bound $L^2\ge\beta\Delta$, under $\varepsilon^2\le c\beta\Delta$ and $d\ge C(\beta\Delta/\varepsilon^2)\log(2+\beta\Delta/\varepsilon^2)$. One comparison can be simulated by two exact values.

**Local argument.** A1

**Source location.** [2](https://arxiv.org/html/2610.19652v1) theorem: Theorem 10.5

**Source location.** [2](https://arxiv.org/html/2610.19652v1) theorem: Theorem 10.5; pdf pages: 24; printed pages: 24

### B3 - Randomized three-point descent

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
2\left\lceil54d\beta\Delta/\varepsilon^2\right\rceil
$$

**Sources.** [1](https://doi.org/10.1137/19M1244378)

**Conditions.** $\beta ,\Delta ,\varepsilon >0$; $\beta -smooth,global gap\le \Delta$. Exact comparisons are available throughout the ambient space, with a fixed query budget and per-instance guarantee $Pr(\|\nabla f(xhat)\|\le \varepsilon )\ge 2/3$.

**Local argument.** A2

**Source location.** [1](https://doi.org/10.1137/19M1244378) theorem: Algorithm 3.1; Lemma 3.5, equation (3.8), arXiv:1902.03591v3, PDF page 8; Theorem 4.2, page 11

**Source location.** [1](https://doi.org/10.1137/19M1244378) theorem: Algorithm 3.1; Lemma 3.5, equation (3.8), arXiv:1902.03591v3, PDF page 8; Theorem 4.2, page 11

## 5. Local arguments

### A1 - Exact-value lower bounds transferred to comparison feedback

**Scope.** The comparison oracle returns only the exact order of two function values. Query/output domains, model budgets, and guarantees are preserved.

Two exact scalar values simulate one comparison. Therefore a fixed-success exact-value lower bound $L$ gives a comparison lower bound $L/2$. Expected-error targets require a separate constant-factor accuracy conversion.

At each adaptive comparison request $(x,y)$, query both exact values and return their order, including the declared tie convention. The same seed and transcript generate the same next query and output, using at most twice the comparison budget. Hence a comparison algorithm contradicts a value lower theorem only when all source model and guarantee conditions match.

For smooth convex objectives, apply the dimension/accuracy branch of Dorn et al., Theorem 2.1, at $Q\ge32$, and its logarithmic strongly convex subclass at $Q\ge128^2$; maximize only on their common window. For a strongly convex model with initial gap $\Delta$, choose a hard-instance radius $R_h=\sqrt{2\Delta/\beta}$. Smoothness at the global minimizer gives the required initial gap. If the target guarantee is expected error $\varepsilon$, Markov supplies success $2/3$ at error $3\varepsilon$; then the source scale is $Q_h=2\Delta/(3\varepsilon)$ and must be at least 32. No new public radius is added to the target specification.

For nonconvex gradient stationarity, use the exact-value hard subclass with a proof-only Lipschitz budget satisfying $L^2\ge\beta\Delta$. The source cap $B=\min\{\beta\Delta,L^2\}$ becomes $\beta\Delta$. Retain its small-gradient window and dimension requirement $d\ge C(\beta\Delta/\varepsilon^2)\log(2+\beta\Delta/\varepsilon^2)$. The same two-value simulation then gives the registered comparison lower bound.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [4](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2610.19652v1)

### A2 - A fixed-budget stationarity guarantee using two comparisons per iteration

**Scope.** Global $\beta$-smoothness, initial gap at most $\Delta$, unrestricted exact comparisons, and an arbitrary returned point; no global Lipschitz or bounded-sublevel-set promise.

For $\Delta>0$, at most $2\lceil54\beta d\Delta/\varepsilon^2\rceil$ comparisons achieve $\Pr(\|\nabla f(\widehat x)\|\le\varepsilon)\ge2/3$.

Independently draw $u_t$ uniformly from the unit sphere. Using two comparisons, choose the best of $x_t,x_t+\alpha u_t,x_t-\alpha u_t$ and make it $x_{t+1}$. Set $\alpha=\varepsilon/(3\beta\sqrt{3d})$ and $T=\lceil54\beta d\Delta/\varepsilon^2\rceil$. Smoothness gives
$$f(x_{t+1})\le f(x_t)-\alpha|\langle\nabla f(x_t),u_t\rangle|+\beta\alpha^2/2.$$
For a fixed vector $g$, sphere moments satisfy $\mathbb E\langle g,u\rangle^2=\|g\|^2/d$ and $\mathbb E\langle g,u\rangle^4=3\|g\|^4/[d(d+2)]$. Holder interpolation yields $\mathbb E|\langle g,u\rangle|\ge\|g\|/\sqrt{3d}$. Conditional expectation and telescoping imply
$$\frac1T\sum_{t=0}^{T-1}\mathbb E\|\nabla f(x_t)\|\le\frac{9\beta d\Delta}{\varepsilon T}+\frac\varepsilon6\le\frac\varepsilon3.$$
Return a uniformly random iterate from these $T$ points, independently of the preceding randomness. Its expected gradient norm is at most $\varepsilon/3$, so Markov proves the guarantee. No unknown gradient is used to choose the output. If $\Delta=0$, the initial point is a global minimizer and no calls are needed.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://doi.org/10.1137/19M1244378)

## References

[1] El Houcine Bergou, Eduard Gorbunov, Peter Richtárik. Stochastic Three Points Method for Unconstrained Smooth Minimization. arXiv:1902.03591v3; Lemma3.5 and Theorem4.2 read on 2026-10-29.

https://doi.org/10.1137/19M1244378

[2] Xia and Yuan. On Global Joint Lower Bounds in Zeroth-Order Nonconvex Optimization. arXiv:2610.19652v1, 2026-10-14.

https://arxiv.org/html/2610.19652v1

[3] Zhang and Li. Comparisons Are All You Need for Optimizing Smooth Functions. arXiv:2405.11454v1, 2024; the specified early version.

https://arxiv.org/html/2405.11454v1

[4] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa; Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1
