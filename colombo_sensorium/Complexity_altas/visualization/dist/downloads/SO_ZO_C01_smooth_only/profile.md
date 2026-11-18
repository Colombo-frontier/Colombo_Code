# First-order stationarity of nonconvex functions with only gradient smoothness and exact values

**Setting ID.** `SO_ZO_C01_smooth_only`

Single-objective optimization

Find an approximate first-order stationary point of the population objective $f$: an output point with sufficiently small gradient norm. The mathematical object is $\nabla f$, and information is acquired through the zeroth-order interface specified below.

**Status.** Fully optimal

**TASK tags.** formulation: First order stationarity; solution concept: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; initialization: Global initial gap; smoothness: Lipschitz gradient

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: First order stationarity

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find an approximate first-order stationary point of the population objective $f$: an output point with sufficiently small gradient norm. The mathematical object is $\nabla f$, and information is acquired through the zeroth-order interface specified below.

### Admissible model

$f:\mathbb{R}^d\to\mathbb{R}$ is differentiable and satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$ for every $x,y\in\mathbb{R}^d$.

$f_*:=\inf_{x\in\mathbb{R}^d}f(x)>-\infty$, and the given initial point $x_0$ satisfies $f(x_0)-f_*\le\Delta$.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

The public inputs are $d$, $\beta$, $\Delta$, $\varepsilon$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=\|\nabla f(x)\|_2$ with tolerance $\varepsilon>0$. Any theorem for squared gradient norms must first be converted to this norm scale.

### Resource accounting

Each scalar function value or noisy observation costs $1$ call. Every location in a multipoint finite difference, every initialization query, and every reference observation is charged.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

#### Deterministic

Only deterministic strategies are allowed. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The requirement $\ell(I,\widehat{x})\le \varepsilon$ holds deterministically for each instance.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

#### Randomized

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The error requirement is $\Pr(\ell(I,\widehat{x})\le \varepsilon)\ge2/3$.

Probability is over the algorithm's random seed only.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

**Output qualification.** Random selection among previously queried points is permitted, subject to the declared success guarantee.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$\Delta$: Known upper bound on the initial objective gap **Domain:** $\Delta\ge0$.

$f(x_0)-\inf_{x\in\mathbb{R}^d}f(x)\le\Delta$

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

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime C01.R0

**Region.** Gradient-smoothness-only specification; $\varepsilon^2\le c\beta\Delta$ and $d\ge C(\beta\Delta/\varepsilon^2)\log(2+\beta\Delta/\varepsilon^2)$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** One scalar function value or observation

**Status.** Optimal

**Lower bound.** B2, B5

$$
\Omega(d\beta\Delta/\varepsilon^2)
$$

**Upper bound.** B1, B3, B4

$$
O(d\beta\Delta/\varepsilon^2)
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Finite-difference gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d(1+\beta\Delta/\varepsilon^2))
$$

**Sources.** [2](https://arxiv.org/pdf/1309.5549)

**Conditions.** $\beta ,\Delta ,\varepsilon >0$; exact function values throughout the ambient space; $d\ge 1$.

**Local argument.** A1

### B2 - Randomly rotated chain and scalar-concealment hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\beta\Delta/\varepsilon^2)
$$

**Sources.** [1](https://arxiv.org/html/2610.19652v1) [3](https://arxiv.org/html/2609.00045v3) [4](https://arxiv.org/pdf/2610.00245v2) [5](https://arxiv.org/html/2610.17074v1)

**Conditions.** $\varepsilon ^2\le c\beta \Delta$ , $d\ge C(\beta \Delta /\varepsilon ^2)\log(2+\beta \Delta /\varepsilon ^2)$; $smooth_only$.

**Local argument.** A2

**Source location.** [1](https://arxiv.org/html/2610.19652v1) theorem: Smooth exact-value lower bound in XY26, restricted to the hard subclass with $L^2=\beta\Delta$

### B3 - Gradient method with random-direction smoothing

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(d\beta \Delta/\varepsilon^2)
$$

**Sources.** [2](https://arxiv.org/pdf/1309.5549)

**Conditions.** The population gradient is $\beta$-Lipschitz, and the initial objective gap is at most $\Delta$. Random-direction smoothing is used; with exact values, the finite-difference step may be any sufficiently small finite positive number.

**Local argument.** A1

**Source location.** [2](https://arxiv.org/pdf/1309.5549) theorem: Exact-oracle specialization of Section 3; direct coordinate-difference descent construction

### B4 - Finite-difference gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d(1+\beta\Delta/\varepsilon^2))
$$

**Sources.** [2](https://arxiv.org/pdf/1309.5549)

**Conditions.** $\beta ,\Delta ,\varepsilon >0$; exact function values throughout the ambient space; $d\ge 1$.

**Local argument.** A1

### B5 - Randomly rotated chain and scalar-concealment hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\beta\Delta/\varepsilon^2)
$$

**Sources.** [1](https://arxiv.org/html/2610.19652v1) [3](https://arxiv.org/html/2609.00045v3) [4](https://arxiv.org/pdf/2610.00245v2) [5](https://arxiv.org/html/2610.17074v1)

**Conditions.** $\varepsilon ^2\le c\beta \Delta$ , $d\ge C(\beta \Delta /\varepsilon ^2)\log(2+\beta \Delta /\varepsilon ^2)$; $smooth_only$.

**Local argument.** A2

**Source location.** [1](https://arxiv.org/html/2610.19652v1) theorem: Smooth exact-value lower bound in XY26, restricted to the hard subclass with $L^2=\beta\Delta$

## 5. Local arguments

### A1 - Deterministic central-difference descent with a fixed cap

**Scope.** Global $\beta$-smoothness and initial gap $\Delta$; exact all-space values; no global function-Lipschitz assumption.

The deterministic upper is $O(d(1+\beta\Delta/\varepsilon^2))$, and is therefore admissible in a view allowing randomization.

At a point $x$, take central differences in all coordinates with $h=\varepsilon/(2\beta\sqrt d)$. Integrating the gradient Lipschitz inequality over the segment gives coordinate error at most $\beta h/2$, so $\|g-\nabla f(x)\|\le\varepsilon/4$. If $\|g\|\le3\varepsilon/4$, return $x$. Otherwise, $\|\nabla f(x)\|>\varepsilon/2$. With $e=g-\nabla f(x)$, a step $x^+=x-g/\beta$ obeys
$$f(x^+)\le f(x)-\frac{\|\nabla f(x)\|^2-\|e\|^2}{2\beta}<f(x)-\frac{3\varepsilon^2}{32\beta}.$$
More than $32\beta\Delta/(3\varepsilon^2)$ nonterminating steps contradict the gap budget. Thus at most $\lceil32\beta\Delta/(3\varepsilon^2)\rceil+1$ approximate gradients suffice, each using $2d$ scalar values. The finite step and stopping test provide a worst-case cap.

The separately registered randomized directional upper is the exact-noise specialization of Ghadimi and Lan's Section 3. Its target expected squared gradient norm is expressed at the profile's norm scale by replacing the source tolerance with a constant multiple of $\varepsilon^2$; a finite positive smoothing radius controls its bias. That randomized witness is retained as such, rather than relabeled because a deterministic algorithm has the same leading rate.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [2](https://arxiv.org/pdf/1309.5549)

### A2 - Oracle and subclass transfers for nonconvex lower bounds

**Scope.** Each bound keeps the source's fixed cap, output convention, accuracy window, and lower-bound algorithm class. Dimension-free supremum statements remain distinct from fixed-dimension statements.

The registered lower bounds follow by exact simulation or class containment, with no added dimension factor.

For identical stochastic samples or identical finite-sum components, use the same exact-value hard function for every label. The oracle response is then exactly one source value, so the source's computational lower bound transfers one-for-one. When the target observes fresh additive Gaussian values, an exact-value algorithm can generate the independent Gaussian perturbations itself; an algorithm for that noisier interface would therefore contradict the stronger exact-value lower. The exact-value source cap $B=\min\{\beta\Delta,L^2\}$ and its high-dimensional window remain in force. A smooth-only class may choose the proof-only budget $L=\sqrt{\beta\Delta}$ inside the hard subclass; this does not add a public Lipschitz parameter.

The second-moment sample class is contained in each $r$-moment class for $1<r\le2$, by $(\mathbb EG^r)^{1/r}\le(\mathbb EG^2)^{1/2}$. Thus the source Goldstein statistical lower transfers to the larger heavy-tail class, but it does not establish a matching heavy-tail exponent. A composite class that includes $\psi=0$ contains the corresponding noncomposite hard family. With $X=\mathbb R^d$, the normal-cone residual is the unconstrained Goldstein residual. These embeddings support the registered composite and constrained-normal-cone lower bounds only where those model members are allowed; they do not automatically support a compact-set Frank--Wolfe-gap lower bound.

A value-and-gradient incremental oracle can simulate a selected-component value by discarding the gradient. Dense26 Theorem 3.1 consequently transfers its $\Omega(n+\sqrt n\,\beta\Delta/\varepsilon^2)$ lower, with $n\ge1024$ and the registered dimension window. The same stronger-oracle ordering transfers the Hessian-Lipschitz and higher-order-smooth first-order lower theorems to exact values. A second-order stationary output necessarily satisfies its first-order gradient requirement, so the first-order lower also limits that stronger task. If the theorem states that some sufficiently large finite dimension is hard, retain $\sup_{d\ge1}N^*(d,\varepsilon)$ or its explicit hard-dimension bound; do not present it as a result for every fixed $d$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.19652v1) [3](https://arxiv.org/html/2609.00045v3) [4](https://arxiv.org/pdf/2610.00245v2) [5](https://arxiv.org/html/2610.17074v1)

## References

[1] Xia and Yuan. On Global Joint Lower Bounds in Zeroth-Order Nonconvex Optimization. arXiv:2610.19652v1, 2026-10-14.

https://arxiv.org/html/2610.19652v1

[2] Ghadimi and Lan. Stochastic First- and Zeroth-Order Methods for Nonconvex Stochastic Programming. SIAM Journal on Optimization, 2013.

https://arxiv.org/pdf/1309.5549

[3] Peng, Tang and Jia. Dense Weak Hiding: Closing Complexity Gaps in Nonconvex and PL Finite-Sum Optimization under Individual Smoothness. arXiv:2609.00045v3, 2026-10-10.

https://arxiv.org/html/2609.00045v3

[4] Zhang et al.. Matching Lower Bounds for Randomized First-Order Methods in Hessian-Lipschitz Nonconvex Optimization. arXiv:2610.00245v2, 2026-10-19.

https://arxiv.org/pdf/2610.00245v2

[5] Zhang et al.. Matching Randomized First-Order Bounds for Higher-Order Smooth Nonconvex Optimization. arXiv:2610.17074v1, 2026.

https://arxiv.org/html/2610.17074v1
