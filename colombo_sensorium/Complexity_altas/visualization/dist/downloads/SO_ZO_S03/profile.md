# Nonconvex stationarity with low curvature trace and exact values

**Setting ID.** `SO_ZO_S03`

Single-objective optimization

Find an approximate first-order stationary point of the population objective $f$: an output point with sufficiently small gradient norm. The mathematical object is $\nabla f$, and information is acquired through the zeroth-order interface specified below.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Logarithmic gap

**TASK tags.** formulation: First order stationarity; solution concept: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; initialization: Global initial gap; smoothness: Lipschitz gradient; spectral structure: Unknown fixed hessian upper matrix; structure: Trace budget

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

There is a fixed unknown symmetric positive-semidefinite matrix $H$, with $\|H\|_{\mathrm{op}}\le\beta$, $\operatorname{tr}H\le\beta E$ and $1\le E\le d$. On the initial sublevel set $\{x:f(x)\le f(x_0)\}$, $\nabla^2f(x)\preceq H$ holds almost everywhere.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

The matrix $H$ is hidden; only the budgets $E$ and $\beta$ are public.

The public inputs are $d$, $\beta$, $\Delta$, $E$, $\varepsilon$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

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

$E$: Normalized trace budget of the unknown curvature upper-bound matrix **Domain:** $1\le E\le d$.

$\operatorname{tr}H\le\beta E$

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

$H$: Unknown fixed matrix bounding curvature from above **Domain:** $H=H^\top\succeq0$.

$\|H\|_{\mathrm{op}}\le\beta$, $\operatorname{tr}H\le\beta E$

$\operatorname{tr},\preceq$: Matrix trace and positive semidefinite order **Domain:** Real symmetric matrix.

$A\preceq B$ means that $v^\top(B-A)v\ge0$ for every $v$.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$I_d,\preceq$: Identity matrix and positive-semidefinite order **Domain:** $I_d\in\mathbb{R}^{d\times d}$; the order applies to real symmetric matrices of the same size.

$A\preceq B$ means that $v^\top(B-A)v\ge0$ for every $v\in\mathbb{R}^d$.

$x_0$: Public initial point **Domain:** $x_0\in\mathbb{R}^d$.

Belongs to the feasible domain required by the model.

$c_H$: Fixed constant in the intermediate low-curvature-trace lower-bound window **Domain:** $c_H>0$.

Used for the threshold $EK\le c_Hd^2/\log(ed)$; the source corollary fixes the same numerical value.

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

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime S03.R2

**Region.** Deterministic strategies; $1\le E\le d$, $K\ge1$, $EK\le d$, and $E<K\log(e+K)$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Logarithmic gap

**Lower bound.** B3

$$
\Omega(d\min\{K,\sqrt{EK/\log(e+K)}\})
$$

**Upper bound.** B1

$$
O(d\min\{K,\sqrt{EK}\})
$$

**Gap or comparison.** $O(\sqrt{\log(e+K)})$

### R2 - Parameter regime S03.R5

**Region.** Deterministic strategies; $K\ge1$ and $K\log(e+K)\le E\le d$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Optimal

**Lower bound.** B6

$$
\Omega(dK)
$$

**Upper bound.** B2

$$
O(dK)
$$

**Gap or comparison.** $O(1)$

### R3 - Parameter regime S03.R1

**Region.** Randomization is allowed; $1\le E\le d$, $K=\beta\Delta/\varepsilon^2\ge1$ and $EK\le d$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** One scalar function value or observation

**Status.** Optimal

**Lower bound.** B9

$$
\Omega(EK)
$$

**Upper bound.** B7

$$
O(EK)
$$

**Gap or comparison.** $O(1)$

### R4 - Parameter regime S03.R4

**Region.** Randomization is allowed; $1\le E\le d$, $K=\beta\Delta/\varepsilon^2\ge1$ and $d<EK\le c_Hd^2/\log(ed)$. The constant $c_H>0$ is fixed by the source corollary.

**Views.** Randomized

**Quantity.** Q3

**Resource.** One scalar function value or observation

**Status.** Optimal

**Lower bound.** B10

$$
\Omega(EK)
$$

**Upper bound.** B7

$$
O(EK)
$$

**Gap or comparison.** $O(1)$

### R5 - Parameter regime S03.R6

**Region.** Randomization is allowed; $1\le E\le d$, $K\ge1$, $EK>d$ and $EK>c_Hd^2/\log(ed)$. The constant $c_H$ is the same as in the preceding intermediate regime.

**Views.** Randomized

**Quantity.** Q3

**Resource.** One scalar function value or observation

**Status.** Polynomial gap

**Lower bound.** B11

$$
\Omega(d)
$$

**Upper bound.** B7

$$
O(EK)
$$

**Gap or comparison.** $O(EK/d)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Trace-adapted randomized descent or a deterministic directional method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d\min\{K,\sqrt{EK}\})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2)

**Conditions.** $1\le E\le d$, $K\ge1$ and $EK\le d$. The simplified deterministic bound applies only in this window.

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Theorems 3.1--3.2; pdf pages: 6; printed pages: 6

### B2 - Deterministic low-curvature trace method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
\mathrm{Det}:\ O(\min\{dK,\sqrt{dEK(d+K)}\})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2)

**Conditions.** $1\le E\le d$ and $K\ge1$. This deterministic upper bound holds throughout the stated parameter range.

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Theorem B.1 / Corollary G.10; pdf pages: 18; printed pages: 18

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Theorem B.1 / Corollary G.10; pdf pages: 52; printed pages: 52

### B3 - Deterministic and randomized hard families under a low curvature-trace bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega(d\min\{K,\sqrt{EK/\log(e+K)}\})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2)

**Conditions.** $1\le E\le d$, $K\ge1$, $EK\le d$.

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Theorems 3.1--3.2; pdf pages: 6; printed pages: 6

### B4 - Deterministic and randomized hard families under a low curvature-trace bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(EK)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2) [2](https://arxiv.org/html/2610.19652v1)

**Conditions.** $1\le E\le d$, $K\ge1$ and $EK\le c_Hd^2/\log(ed)$, where $c_H>0$ is the universal constant fixed in the source corollary.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Trace26, Corollary H.3, with $\beta^\prime=\beta E/d$; pdf pages: 56; printed pages: 56

**Source location.** [2](https://arxiv.org/html/2610.19652v1) theorem: Trace26, Corollary H.3, with $\beta^\prime=\beta E/d$

### B5 - Deterministic and randomized hard families under a low curvature-trace bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega(d)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2)

**Conditions.** $1\le E\le d$, $K\ge1$.

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Corollary F.4; Lemma E.2; pdf pages: 43; printed pages: 43

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Corollary F.4; Lemma E.2

### B6 - Deterministic and randomized hard families under a low curvature-trace bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
dK/18432
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2)

**Conditions.** $1\le E\le d$, $K\ge1$, $K\log(e+K)\le E$.

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Corollary G.10; pdf pages: 52

### B7 - Trace-adapted randomized descent or a deterministic directional method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(EK)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2)

**Conditions.** $1\le E\le d$ and $K\ge1$. The randomized upper bound $O(EK)$ holds throughout this parameter range.

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Theorems 3.1--3.2; pdf pages: 6; printed pages: 6

### B8 - Deterministic low-curvature trace method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
\mathrm{Det}:\ O(\min\{dK,\sqrt{dEK(d+K)}\})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2)

**Conditions.** $1\le E\le d$ and $K\ge1$. This deterministic upper bound holds throughout the stated parameter range.

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Theorem B.1 / Corollary G.10; pdf pages: 18; printed pages: 18

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Theorem B.1 / Corollary G.10; pdf pages: 52; printed pages: 52

### B9 - Deterministic and randomized hard families under a low curvature-trace bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(EK)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2)

**Conditions.** $1\le E\le d$, $K\ge1$, $EK\le d$.

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Theorems 3.1--3.2; pdf pages: 6; printed pages: 6

### B10 - Deterministic and randomized hard families under a low curvature-trace bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(EK)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2) [2](https://arxiv.org/html/2610.19652v1)

**Conditions.** $1\le E\le d$, $K\ge1$ and $EK\le c_Hd^2/\log(ed)$, where $c_H>0$ is the universal constant fixed in the source corollary.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Trace26, Corollary H.3, with $\beta^\prime=\beta E/d$; pdf pages: 56; printed pages: 56

**Source location.** [2](https://arxiv.org/html/2610.19652v1) theorem: Trace26, Corollary H.3, with $\beta^\prime=\beta E/d$

### B11 - Deterministic and randomized hard families under a low curvature-trace bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\min\{d,EK\})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2)

**Conditions.** $1\le E\le d$, $K\ge1$.

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Corollary F.4; Lemma E.2; pdf pages: 43; printed pages: 43

**Source location.** [1](https://arxiv.org/pdf/2610.27550v2) theorem: Corollary F.4; Lemma E.2

## 5. Local arguments

### A1 - Scaling an isotropic curvature budget to a trace-constrained lower bound

**Scope.** The profile-defined effective curvature budget $E$, smoothness budget $\beta$, and $K=\beta\Delta/\varepsilon^2$; the registered high-dimensional window is retained.

Under $EK\le c d^2/\log(ed)$, the isotropic subclass gives $\Omega(EK)$.

Choose the public curvature certificate $H=\beta'I$ with $\beta'=\beta E/d$. This obeys the profile's trace budget and the spectral budget whenever its stated admissible range for $E$ holds. Apply the isotropic source lower at smoothness $\beta'$. Its factor $d\beta'\Delta/\varepsilon^2$ is exactly $EK$, and its dimension condition becomes the displayed one. This is a parameter scaling of Corollary H.3, not multiplication of separate dimension and trace lower bounds. Scalar values and other projected oracles remain distinct resources.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/pdf/2610.27550v2)

## References

[1] Peng, Tang and Jia. Lower Bounds for Smooth Nonconvex Zeroth-Order Optimization: The Price of Determinism under Low Curvature Trace. arXiv:2610.27550v2, 2026-10-21.

https://arxiv.org/pdf/2610.27550v2

[2] Xia and Yuan. On Global Joint Lower Bounds in Zeroth-Order Nonconvex Optimization. arXiv:2610.19652v1, 2026-10-14.

https://arxiv.org/html/2610.19652v1
