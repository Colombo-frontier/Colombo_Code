# Power-law compressible gradients: first-order stationarity from exact values

**Setting ID.** `SO_ZO_S01_rand_native`

Single-objective optimization

Find an approximate first-order stationary point of the population objective $f$: an output point with sufficiently small gradient norm. The mathematical object is $\nabla f$, and information is acquired through the zeroth-order interface specified below.

**Status.** Bounds missing

**TASK tags.** formulation: First order stationarity; solution concept: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; initialization: Global initial gap; smoothness: Lipschitz gradient; structure: Compressible gradients

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; query domain: Full space

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

Fix $p\in(0,1)$. For all $x\in\mathbb{R}^d$ and $j=1,\ldots,d$, the $j$th largest absolute gradient coordinate satisfies $|\nabla f(x)|_{(j)}\le\|\nabla f(x)\|_2j^{-1/p}$. The support may vary with $x$; this is a relative compressibility assumption.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

The public inputs are $d$, $\beta$, $\Delta$, $\varepsilon$, $p$, $\vartheta$, $s$, $s_0$, $\sigma_0$, $b$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=\|\nabla f(x)\|_2$ with tolerance $\varepsilon>0$. Any theorem for squared gradient norms must first be converted to this norm scale.

### Resource accounting

Each scalar function value or noisy observation costs $1$ call. Every location in a multipoint finite difference, every initialization query, and every reference observation is charged.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. Require $\Pr(\|\nabla f(\widehat{x})\|_2\le\varepsilon)\ge1-2\exp(-c_{\mathrm{RIP}}m_{j_*})$. The quantities $c_{\mathrm{RIP}}>0$ and $m_{j_*}$ are defined in the symbol table; probability is over the random measurement matrices.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$\Delta$: Known upper bound on the initial objective gap **Domain:** $\Delta\ge0$.

$f(x_0)-\inf_{x\in\mathbb{R}^d}f(x)\le\Delta$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$p$: Power-law compressibility exponent of the gradient **Domain:** $0<p<1$.

$|\nabla f(x)|_{(j)}\le\|\nabla f(x)\|_2j^{-1/p}$, $j=1,\ldots,d$.

$\vartheta$: Relative error parameter for the compressed gradient approximation **Domain:** $0<\vartheta<1/2$.

$s$: Effective sparsity implied by compressibility and relative error **Domain:** $1\le s\le d$.

$s=\left[\frac4\vartheta\left(\frac{13.2}{\sqrt{2/p-1}}+\frac{11}{1/p-1}\right)\right]^{2p/(2-p)}$

$s_0$: Initial sparsity estimate used by the algorithm **Domain:** $s_0\in\mathbb{N}$.

$\lceil bs_0\log d\rceil\le d/4$

$\sigma_0$: Initial curvature scale used by the algorithm **Domain:** $\sigma_0>0$.

It is a public algorithmic parameter, not observation noise.

$b$: Oversampling parameter of the random measurement matrix **Domain:** $b>0$.

Must satisfy $b>c_1(\delta_{\mathrm{RIP}})$ as defined in this profile.

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

$|v|_{(j)}$: Rank of an absolute coordinate in nonincreasing order **Domain:** $j\in\{1,\ldots,d\}$.

Coordinates are ordered by nonincreasing absolute value.

$A_\vartheta$: Curvature amplification factor for relative error **Domain:** $A_\vartheta>0$.

$A_\vartheta=(1+\vartheta)^2/(1-2\vartheta)$

$j_*$: First resolution level providing a sufficiently accurate compressed estimate **Domain:** $j_*\in\mathbb{N}$.

$j_*=\lceil\max\{1,\log_2(s/s_0),\log_2(A_\vartheta\beta/\sigma_0)\}\rceil$

$S_*$: Sparsity scale used in the upper bound **Domain:** $S_*>0$.

$S_*=\max\{2s_0,2s,2A_\vartheta\beta s_0/\sigma_0\}$

$M_*$: Curvature scale used in the upper bound **Domain:** $M_*>0$.

$M_*=\max\{2\sigma_0,2s\sigma_0/s_0,2A_\vartheta\beta\}$

$s_j,m_j,J$: Sparsity levels, measurement dimension, and the full-dimensional fallback level **Domain:** $j\in\mathbb{N}_0$.

$s_j=2^js_0$, $m_j=\lceil bs_j\log d\rceil$ and $J=\min\{j:m_j\ge d\}$. The bound requires $j_*<J-1$.

$\delta_{\mathrm{RIP}}$: Fixed target restricted-isometry constant of the random matrix **Domain:** $\delta_{\mathrm{RIP}}=0.22664$.

Positive constant used only to specify the success probability.

$c_0^{\mathrm{RIP}}(a)$: Tail-bound function for Rademacher measurements **Domain:** $a\in\mathbb{R}$.

$c_0^{\mathrm{RIP}}(a)=a^2/4-a^3/6$

$c_1(\delta)$: Sufficient oversampling threshold **Domain:** $0<\delta<1,\ 4s_{j_*}<d$.

$c_1(\delta)=\frac{4}{c_0^{\mathrm{RIP}}(\delta/2)}\left[1+\frac{1+\log(12/\delta)}{\log(d/(4s_{j_*}))}\right]$

$c_{\mathrm{RIP}}$: Positive constant in the success-probability exponent **Domain:** $c_{\mathrm{RIP}}>0$.

$c_{\mathrm{RIP}}=c_0^{\mathrm{RIP}}(\delta_{\mathrm{RIP}}/2)-\frac4b\left[1+\frac{1+\log(12/\delta_{\mathrm{RIP}})}{\log(d/(4s_{j_*}))}\right]$; choose $b>c_1(\delta_{\mathrm{RIP}})$.

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

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Additional theorem window

**Region.** $0<\vartheta<1/2$. The public initialization satisfies $\lceil bs_0\log d\rceil\le d/4$ and $j_*<J-1$, with $b>c_1(0.22664)$. Retain dependence on $s/s_0$, $\beta/\sigma_0$ and $\Delta$. The success probability is over the random matrices specified in this profile.

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
4b(1+j_*)S_*M_*\Delta\log(d)\varepsilon^{-2}
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $0<\vartheta<1/2$. The public initialization satisfies $\lceil bs_0\log d\rceil\le d/4$ and $j_*<J-1$, with $b>c_1(0.22664)$. Retain dependence on $s/s_0$, $\beta/\sigma_0$ and $\Delta$. The success probability is over the random matrices specified in this profile.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee mapping.** The success probability is the explicit probability for the random compression matrix. Truncating execution at a known upper bound preserves a fixed call cap; conversion to the prescribed constant success probability is valid only when the stated probability threshold is met.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Compressible-gradient estimation with ZORO-FA

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
4b(1+j_*)S_*M_*\Delta\log(d)\varepsilon^{-2}
$$

**Sources.** [1](https://arxiv.org/html/2501.11616v3)

**Source location.** [1](https://arxiv.org/html/2501.11616v3) theorem: Corollaries 3--4, equations (44)--(47)

**Source location.** [1](https://arxiv.org/html/2501.11616v3) theorem: Corollaries 3--4, equations (44)--(47)

**Source location.** [1](https://arxiv.org/html/2501.11616v3) theorem: Corollaries 3--4, equations (44)--(47); pdf pages: 14

## References

[1] Grapiglia and McKenzie. Fully Adaptive Zeroth-Order Method for Minimizing Functions with Compressible Gradients. JOTA 208, 2026; checked version arXiv:2501.11616v3.

https://arxiv.org/html/2501.11616v3
