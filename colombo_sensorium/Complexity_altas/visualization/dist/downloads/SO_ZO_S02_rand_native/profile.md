# High-dimensional sparse convex objectives with independent noisy values

**Setting ID.** `SO_ZO_S02_rand_native`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Coordinate l1 gradient bound; smoothness: Entrywise l1 hessian bound; structure: Fixed unknown coordinate support

**ORACLE tags.** access order: Zeroth-order interface; interface family: Independent noisy value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

### Admissible model

$f:\mathbb{R}^d\to\mathbb{R}$ is convex and twice differentiable, and has a global minimizer $x_*$ satisfying $\|x_*\|_1\le B$.

For every $x$, $\|\nabla f(x)\|_0\le s$, $\|\nabla f(x)\|_1\le H$, and $\sum_{i,j=1}^d|\partial_{ij}f(x)|\le H$ hold. There is a fixed unknown set $S\subseteq\{1,\ldots,d\}$ with $|S|\le s$ such that $f(x)=f_S(x_S)$.

### Oracle interface

A query at $x_t\in \mathbb{R}^d$ returns one scalar $Y_t=f(x_t)+\xi_t$.

$\xi_t$ is drawn i.i.d. from $N(0,\sigma_v^2)$, independently of the algorithmic seed and preceding observations.

Every observation is charged independently. No same-sample coupling, sample handle, or noiseless function value is supplied.

The global support $S$ is hidden.

The public inputs are $d$, $s$, $H$, $B$, $\sigma_v$, $\varepsilon$, $T$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

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

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The error requirement is $\Pr(\ell(I,\widehat{x})\le \varepsilon)\ge2/3$.

Probability is over both the algorithm's seed and all feedback randomness, after fixing the instance and admissible environment law.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$s$: Upper bound on the size of the unknown global support **Domain:** $s\in\{1,\ldots,d\}$.

$|S|\le s$

$H$: Joint budget for coordinatewise gradient and Hessian regularity **Domain:** $H>0$.

$\|\nabla f(x)\|_1\le H$ and $\sum_{i,j}|\partial_{ij}f(x)|\le H$.

$B$: Known one-norm localization radius for a global minimizer **Domain:** $B>0$.

$\|x_*\|_1\le B$

$\sigma_v$: Standard deviation of independent Gaussian value noise **Domain:** $\sigma_v\ge0$.

$\xi\sim N(0,\sigma_v^2)$

$T$: Known query budget or argument of the risk curve **Domain:** $T\in\mathbb{N}_0$.

Use $N\le T$ in the fixed-budget specification and $\mathbb{E}[N]\le T$ in the expected-budget specification.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

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

$r_T$: Error scale of the final recommendation under the budget **Domain:** $T\in\mathbb{N}_0$.

Under an expectation guarantee, the quantity is $\inf_{\mathcal{A}:N\le T}\sup_I\mathbb{E}[f(\widehat{x})-f_*]$. Under a fixed-success-probability guarantee, it is the $2/3$ quantile threshold with the same quantifier order.

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

$S,x_S,f_S$: Unknown global support, coordinate subvector, and lower-dimensional objective **Domain:** $S\subseteq\{1,\ldots,d\},\ |S|\le s$.

$f(x)=f_S(x_S)$

$\|v\|_0,\|v\|_1$: Number of nonzero coordinates and the one-norm **Domain:** $v\in\mathbb{R}^d$.

$\|v\|_0=|\{i:v_i\ne0\}|$, $\|v\|_1=\sum_i|v_i|$

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

## 3. Complexity bracket

### Compared quantities

#### Q1 - fixed budget error quantile

$$
q^\star_{v,\pi}(B,\delta;\theta)=\inf\{\varepsilon:\exists\mathcal A\in\mathfrak A_v,\ C_\pi\le B,\ \Pr(\ell(I,\mathcal A)\le\varepsilon)\ge1-\delta\ \forall I\}
$$

**Definition.** Error quantile at a fixed budget and success probability

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Additional theorem window

**Region.** $Cs^3\log d\le T\le d$. The noise is independent and Gaussian, the support is fixed, and all remaining coordinate bounds are as stated in the model.

**Quantity.** Q1

**Resource.** Error quantile at a fixed budget and success probability

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
B(\sigma_v^2H^2s\log d/T)^{1/4}+\widetilde{O}_{s,\sigma_v,H,B}(T^{-1/3})
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The global support is fixed. Both the gradient one-norm and the sum of absolute Hessian entries satisfy the model bounds; $Cs^3\log d\le T\le d$. The risk remainder retains polynomial dependence on $s,\sigma_v,H,B$.

**Oracle mapping.** Scalar observations follow the independent-noise, conditional-noise, or mixed-error law specified here; every repeated observation is charged separately.

**Guarantee mapping.** The displayed risk is a simple-regret quantile scale at a fixed success probability; it is not labeled as expected risk.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Sparse gradient estimation and convex optimization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
r_T\lesssim B(\sigma_v^2H^2s\log d/T)^{1/4}+\widetilde{O}(T^{-1/3})
$$

**Sources.** [1](https://proceedings.mlr.press/v84/wang18e/wang18e.pdf)

**Source location.** [1](https://proceedings.mlr.press/v84/wang18e/wang18e.pdf) theorem: Theorem 1; pdf pages: 5

## References

[1] Wang, Du, Balakrishnan and Singh. Stochastic Zeroth-order Optimization in High Dimensions. AISTATS 2018, PMLR 84.

https://proceedings.mlr.press/v84/wang18e/wang18e.pdf
