# Goldstein Frank-Wolfe gap: joint sample-value and LMO budget

**Setting ID.** `SO_ZO_B05_rand_multi_resource`

Single-objective optimization

Find a feasible point in the known compact convex set $X$ with a sufficiently small Goldstein Frank-Wolfe gap.

**Status.** Bounds missing; Joint budget unresolved

**TASK tags.** formulation: So goldstein frank wolfe stationarity; solution concept: Goldstein frank wolfe stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; initialization: Constrained initial gap; stochastic model: Sample lipschitz second moment

**ORACLE tags.** access order: Zeroth-order interface; interface family: Reusable sample value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Goldstein frank wolfe stationarity

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find a feasible point in the known compact convex set $X$ with a sufficiently small Goldstein Frank-Wolfe gap.

### Admissible model

$f(x)=\mathbb{E}[F(x;Z)]$. The sample value at a reference point is integrable. Sample functions satisfy $|F(x;Z)-F(y;Z)|\le G(Z)\|x-y\|_2$ and $\mathbb{E}[G(Z)^2]\le L^2$ throughout $\mathbb{R}^d$; samplewise convexity is not required.

$X\subseteq\mathbb{R}^d$ is a known nonempty closed convex set. The given initial point $x_0\in X$ satisfies $f(x_0)-\inf_{x\in X}f(x)\le\Delta<\infty$.

$X$ is additionally compact with $\operatorname{diam}_2(X)\le D$, and the Goldstein neighborhood radius satisfies $0<\rho<D$.

### Oracle interface

A new sample handle corresponds to an independent draw of the hidden sample $Z$. Given its handle and $x\in \mathbb{R}^d$, the interface returns the exact sample value $F(x;Z)$. The algorithm observes only handles and numerical values, not the underlying sample data or the complete sample function.

Sample handles may be retained for arbitrarily many paid evaluations. Responses using the same handle come from the same function, and distinct handles are independent.

A linear-minimization interface is also available: input $g\in\mathbb{R}^d$ and receive some $v\in\operatorname{argmin}_{y\in X}\langle g,y\rangle$. If minimizers are nonunique, the interface may select any admissible one. Perturbed function queries may lie outside $X$.

The public inputs are $d$, $L$, $\Delta$, $\rho$, $D$, $\varepsilon$, $X$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in X$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

$\ell(I,x)=\min_{g\in\partial_\rho f(x)}\max_{y\in X}\langle g,x-y\rangle$. This gap is finite and nonnegative because $X$ is compact and $x\in X$. The target tolerance is $\varepsilon$.

$\partial_\rho f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\rho}\partial f(y)$, where $\partial f$ is the Clarke subdifferential of the function on the ambient space.

### Resource accounting

One scalar sample-function value costs $1$ call; two points with the same sample handle or Markov state cost $2$ calls. Batches, initialization and repeated visits are charged per value. An empty handle supplies no free instance information.

Retain the joint budget $(N_v,N_{\mathrm{LMO}})$ achieved by one algorithm, counting sample-value and linear-minimization calls separately. Both resources are charged. Without prescribed weights, do not add them or combine coordinates achieved by different algorithms.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. Require $\mathbb{E}[\ell(I,\widehat{x})]\le \varepsilon$, fixing the instance before averaging over algorithmic and feedback randomness.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$L$: Moment budget of the sample Lipschitz coefficient **Domain:** $L>0$.

$\mathbb{E}[G(Z)^2]\le L^2$

$\Delta$: Known upper bound on the initial objective gap **Domain:** $\Delta\ge0$.

$f(x_0)-\inf_{x\in X}f(x)\le\Delta$

$\rho$: Goldstein subdifferential neighborhood radius **Domain:** $\rho>0$.

It measures the neighborhood defining stationarity, not the radius of a query or feasible ball.

$D$: Upper bound on the Euclidean diameter of the compact convex domain **Domain:** $D>0$.

$\sup_{x,y\in X}\|x-y\|_2\le D$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$X$: Fully known feasible or search domain **Domain:** $X\subset\mathbb{R}^d$; nonempty, compact and convex, with $\operatorname{diam}_2(X)\le D$.

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

$f,f_*$: Population objective and its optimal value **Domain:** $f:\mathcal{X}_{\mathrm{fun}}\to\mathbb{R}$.

$f_*=\inf_{x\in X}f(x)$.

$\partial f(x)$: Clarke subdifferential **Domain:** A nonempty compact convex subset at $x$ for a locally Lipschitz function, contained in $\mathbb{R}^d$.

Defined as the closed convex hull of gradient limits along differentiability points approaching $x$.

$\partial_\rho f(x)$: Goldstein neighborhood subdifferential **Domain:** $\rho>0$.

$\partial_\rho f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\rho}\partial f(y)$

$\operatorname{conv},\operatorname{dist}$: Convex hull and Euclidean distance **Domain:** Set operations.

$\operatorname{dist}(v,S)=\inf_{s\in S}\|v-s\|_2$

$N_v,N_{\mathrm{LMO}}$: Numbers of sample-value and linear-minimization calls **Domain:** $N_v,N_{\mathrm{LMO}}\in\mathbb{N}_0$.

Joint budgets count each resource coordinate along the same execution path.

$g,v$: Linear-minimization input and returned point **Domain:** $g\in\mathbb{R}^d,\ v\in X$.

$v\in\operatorname{argmin}_{y\in X}\langle g,y\rangle$

$Z,F(\cdot;Z)$: Hidden sample and its associated sample function **Domain:** Samples lie in an admissible probability space; each sample function is real-valued on the declared domain.

The population objective is the expectation under the sample distribution or stationary distribution.

$G(Z)$: Random sample Lipschitz coefficient **Domain:** $G(Z)\ge0$.

The model's difference inequality holds for each sample, with the moment budget fixed as specified here.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=X$ and $\mathcal{X}=X$; the function domain is the region on which the model imposes regularity.

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

**Definition.** Number of scalar sample-value calls; LMO calls are counted separately

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - achievable resource region

$$
\mathcal B_v(\varepsilon;\theta)=\{b\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_j(\mathcal A,I)\le b_j\ \forall j,I,\quad G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Joint resource vector

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Additional theorem window

**Region.** $X$ is nonempty, compact and convex, with $\operatorname{diam}_2(X)\le D$ and $0<\rho<D$. The available interfaces are the stated sample-value oracle and LMO.

**Quantity.** Q1

**Resource.** Number of scalar sample-value calls; LMO calls are counted separately

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(d\Delta D^3L^2/(\rho\varepsilon^3))
$$

### R2 - Additional theorem window

**Region.** $X$ is nonempty, compact and convex, with $\operatorname{diam}_2(X)\le D$ and $0<\rho<D$. The available interfaces are the stated sample-value oracle and LMO.

**Quantity.** Q2

**Resource.** Joint resource vector

**Status.** Joint budget unresolved

**Achievable budgets.** B2

**Necessary constraints.** No admitted claim in this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $X$ is known, compact and convex, with $\operatorname{diam}_2(X)\le D$ and $0<\rho<D$. The same algorithm uses sample-value and linear-minimization oracles. A joint budget cannot be obtained by combining coordinates achieved by different algorithms.

**Oracle mapping.** Preserve sample handles and their reuse limits. Each queried point returns one sample value; sample data and sample gradients are not available for free.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** One implementation simultaneously attains $N_v=O(d\Delta D^3L^2/(\rho\varepsilon^3))$ and $N_{\mathrm{LMO}}=O(\Delta D^5L^4d^2/(\rho\varepsilon^5))$; the value-query projection selects only the first coordinate.

### B1 - Two-point estimation and conditional-gradient subproblems

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(d\Delta D^3L^2/(\rho\varepsilon^3))
$$

**Sources.** [1](https://arxiv.org/abs/2610.13787v1)

**Source location.** [1](https://arxiv.org/abs/2610.13787v1) theorem: Theorem 6.2; Remark 6.3

**Source location.** [1](https://arxiv.org/abs/2610.13787v1) theorem: Theorem 6.2; Remark 6.3

### B2 - Two-point estimation and conditional-gradient subproblems

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Randomized witness

$$
\bigl(O(d\Delta D^3L^2/(\rho\varepsilon^3)),\ O(\Delta D^5L^4d^2/(\rho\varepsilon^5))\bigr)
$$

**Sources.** [1](https://arxiv.org/abs/2610.13787v1)

**Source location.** [1](https://arxiv.org/abs/2610.13787v1) theorem: Theorem 6.2; Remark 6.3

**Source location.** [1](https://arxiv.org/abs/2610.13787v1) theorem: Theorem 6.2; Remark 6.3

## References

[1] Gon Buzaglo and Guy Kornowski. Optimal Algorithms for Nonsmooth Nonconvex Stochastic Optimization with Constraints. arXiv:2610.13787v1, 2026-10-09.

https://arxiv.org/abs/2610.13787v1
