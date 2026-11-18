# Smooth convex optimization with exact values

**Setting ID.** `SO_ZO_E03`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Lipschitz gradient; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; query domain: Full space; operation: Function value; feedback quality: Exact

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic algorithms; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

### Admissible model

$f:\mathbb{R}^d\to\mathbb{R}$ is differentiable and satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$ for every $x,y\in\mathbb{R}^d$.

$f$ is convex throughout the ambient space.

A global minimizer $x_*\in B_2(0,R)$ exists; the localization ball does not restrict the function domain.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

The public inputs are $d$, $\beta$, $R$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in \mathbb{R}^d}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

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

$R$: Localization radius for a global minimizer **Domain:** $R>0$.

$x_*\in B_2(0,R)$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$Q$: Smoothness accuracy ratio **Domain:** $Q>0$.

$Q=\beta R^2/\varepsilon$

$\gamma$: Relative slack near the zero-call threshold **Domain:** $0<\gamma<1/2$ when $2<Q<4$.

$\gamma=1-2/Q$

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

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact scalar function value

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact scalar function value

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime E03.R1

**Region.** $32\le Q\le d^2$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B2, B13

$$
\Omega(d\sqrt Q)
$$

**Upper bound.** B1, B12

$$
O(d\sqrt Q)
$$

**Gap or comparison.** $O(1)$

### R2 - Parameter regime E03.R2

**Region.** $Q\ge32,\ Q>d^2$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B2, B6

$$
\begin{cases}\Omega(d^2),&Q<128^2,\\\Omega(\max\{d^2,d\log Q\}),&Q\ge128^2.\end{cases}
$$

**Upper bound.** B1

$$
O(\min\{d\sqrt Q,d^2\log Q\})
$$

**Gap or comparison.** $O(\log Q)$

### R3 - Parameter regime E03.R3

**Region.** $Q\le2$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B8, B19

$$
0
$$

**Upper bound.** B7, B18

$$
0
$$

### R4 - Parameter regime E03.R4.part1

**Region.** $2<Q<4$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B10

$$
\Omega(d)
$$

**Upper bound.** B9

$$
O(d)
$$

**Gap or comparison.** $O(1)$

### R5 - Parameter regime E03.R4.part3

**Region.** $4\le Q<32$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B4, B15

$$
\Omega(d)
$$

**Upper bound.** B5, B16

$$
O(d)
$$

**Gap or comparison.** $O(1)$

### R6 - Parameter regime E03.R2

**Region.** $Q\ge32,\ Q>d^2$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B13, B17

$$
\begin{cases}\Omega(d^2),&Q<128^2,\\\Omega(\max\{d^2,d\log Q\}),&Q\ge128^2.\end{cases}
$$

**Upper bound.** B12

$$
O(\min\{d\sqrt Q,d^2\log Q\})
$$

**Gap or comparison.** $O(\log Q)$

### R7 - Parameter regime E03.R4.part2

**Region.** $2<Q<4$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B22

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Upper bound.** B21

$$
O(\max\{1,d(1-2/Q)\})
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Coordinate-difference acceleration or cutting-plane localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\min\{d\sqrt Q,d^2\log Q\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** The principal accuracy window is $Q\ge32$. Use coordinate differences with error-tolerant acceleration, or localization by approximate cutting planes.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 29; printed pages: 29; theorem: Appendix C.2

### B2 - Random quadratics and multiscale accuracy hard families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max\{5d/16,(d/4096)\min(d,\sqrt Q)\}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $0<\varepsilon\le\beta R^2/32$. The hard family can be chosen to consist of positive-definite quadratics satisfying the same localization bound.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 3; printed pages: 3; theorem: Theorem 2.1

### B3 - Random quadratics and multiscale accuracy hard families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Sufficiently small absolute normalized accuracy; a nonquadratic multiscale hard family.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix E, Theorem E.5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 35; printed pages: 35; theorem: Appendix E, Theorem E.5

### B4 - Random quadratics and multiscale accuracy hard families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $Q\ge3$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_ENDPOINT_EXTENSION

### B5 - Coordinate-difference acceleration or cutting-plane localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $4\le Q\le128^2$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_ENDPOINT_EXTENSION

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 29; printed pages: 29; theorem: Appendix C.2

### B6 - Multiscale hard family for accuracy dependence

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $Q\ge128^2$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** ZO_PROOF_PRECISION_LOG

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 4; printed pages: 4; theorem: Theorem 2.5

### B7 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_ZERO

### B8 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_ZERO

### B9 - Deterministic finite-difference descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_SMOOTH_ENDPOINT

### B10 - Deterministic hard family with indistinguishable directions

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega(d)
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_SMOOTH_ENDPOINT

### B11 - Lower bound for estimation of a random spherical center

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_SMOOTH_ENDPOINT

### B12 - Coordinate-difference acceleration or cutting-plane localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\min\{d\sqrt Q,d^2\log Q\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** The principal accuracy window is $Q\ge32$. Use coordinate differences with error-tolerant acceleration, or localization by approximate cutting planes.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 29; printed pages: 29; theorem: Appendix C.2

### B13 - Random quadratics and multiscale accuracy hard families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max\{5d/16,(d/4096)\min(d,\sqrt Q)\}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $0<\varepsilon\le\beta R^2/32$. The hard family can be chosen to consist of positive-definite quadratics satisfying the same localization bound.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 3; printed pages: 3; theorem: Theorem 2.1

### B14 - Random quadratics and multiscale accuracy hard families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Sufficiently small absolute normalized accuracy; a nonquadratic multiscale hard family.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix E, Theorem E.5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 35; printed pages: 35; theorem: Appendix E, Theorem E.5

### B15 - Random quadratics and multiscale accuracy hard families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $Q\ge3$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_ENDPOINT_EXTENSION

### B16 - Coordinate-difference acceleration or cutting-plane localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $4\le Q\le128^2$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_ENDPOINT_EXTENSION

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 29; printed pages: 29; theorem: Appendix C.2

### B17 - Multiscale hard family for accuracy dependence

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $Q\ge128^2$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** ZO_PROOF_PRECISION_LOG

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 4; printed pages: 4; theorem: Theorem 2.5

### B18 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_ZERO

### B19 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_ZERO

### B20 - Deterministic finite-difference descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_SMOOTH_ENDPOINT

### B21 - Randomized projection descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_SMOOTH_ENDPOINT

### B22 - Lower bound for estimation of a random spherical center

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** ZO_PROOF_SMOOTH_ENDPOINT

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: d09e5c50edb6884ea171397ecd2546244d9ac9a5e5b4c8f828e1dfe706896404

### Native proof: ZO_PROOF_SMOOTH_ENDPOINT

Native pointer: /proofs/0; canonical SHA-256: 338937770d1ede37b427bdf58b7747803c6b72e0b7e1e12b5babd5cad5defdff

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: a5c82ebecf3e082953aacf639f4db3a9a8f3308adc30992dbe0443ce0608e13e

Writing $\gamma=1-2/Q\in(0,1/2)$,
$$T_{\mathrm{det}}=\Theta(d),\qquad T_{\mathrm{rand},2/3}=\Theta(\max\{1,d\gamma\}).$$
The constants are uniform in $d,Q$, and in every declared strong-convexity lower budget $0<\mu\le\beta$.

Let $g=\nabla f(0)$. The convex function $h(x)=f(x)-\langle g,x\rangle$ is minimized at zero. A $1/\beta$ descent step for $h$ from a minimizer $x_*$ of $f$ gives
$$f(0)-f_*\le R\|g\|-\|g\|^2/(2\beta).$$
For a rank-$k$ orthogonal projector $P$, central differences in an orthonormal basis of its range yield $\widehat g=Pg+e$ with $e\in\operatorname{range}(P)$ and $\|e\|\le\beta h\sqrt{k}/2$. At $\widehat x=-\widehat g/\beta$, cancellation of the cross term in the smoothness inequality gives
$$f(\widehat x)-f_*\le R\|g\|-\frac{\|g\|^2+\|Pg\|^2}{2\beta}+\frac{\|e\|^2}{2\beta}\le\frac{\beta R^2}{2(1+a)}+\frac{\|e\|^2}{2\beta},\quad a=\frac{\|Pg\|^2}{\|g\|^2}.$$
The zero-gradient case satisfies the same error estimate.

For a Haar-uniform subspace choose $k=\min\{d,\max\{24,\lceil4d\gamma\rceil\}\}$. If $k<d$, then $\mathbb E a=k/d$ and $\operatorname{Var}(a)=2k(d-k)/(d^2(d+2))\le2k/d^2$. Thus $\Pr(a<k/(2d))\le8/k\le1/3$, and $k/(2d)\ge2\gamma$. For $k=d$, $a=1\ge2\gamma$ deterministically. Set
$$m(\gamma)=(1-\gamma)-(1+2\gamma)^{-1}>0,\qquad h=R\sqrt{m(\gamma)/k}.$$
This finite positive step makes the displayed error strictly less than $\varepsilon$ on the good event. It uses $2k$ values. Taking $P=I$ gives the deterministic $O(d)$ upper bound.

For the randomized lower bound take $f_v(x)=\beta\|x-v\|^2/2$, with $v$ uniform on $R S^{d-1}$. A value reveals at most one linear projection of $v$. After at most $T<d$ adaptive projections, the unrevealed part remains conditionally uniform on the residual sphere; the revealed squared energy $S$ obeys $\mathbb E S\le TR^2/d$. If $S<\gamma R^2$, a success ball of radius $R\sqrt{1-\gamma}$ covers at most half that residual sphere. Consequently $p_{\rm success}\le1/2+T/(2d\gamma)$, forcing $T\ge d\gamma/3$. Zero calls are impossible because the success balls for $v=\pm Re_1$ are disjoint and cannot both receive probability $2/3$.

For a deterministic algorithm with $T<d$, answer $\beta(\|x\|^2+R^2)/2$. Choose a length-$R$ vector $v$ orthogonal to every queried vector. The objectives $f_v$ and $f_{-v}$ give the same adaptive transcript, but their average loss at the common output is at least $\beta R^2/2>\varepsilon$. Their Hessian is $\beta I$, so the lower family also belongs to every strongly convex budget $\mu\le\beta$ and to the unknown-quadratic class.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/0/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 7436d26015c807652a1ece7ac37bdb07635b36ddb888cbba0d3b71b99a22f702

Global convexity and $\beta$-smoothness; a global minimizer in $B_2(R)$; unrestricted exact scalar queries and output; fixed worst-case budget; $2<Q=\beta R^2/\varepsilon<4$.

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 7e55293b97d62d893730e65f0711e175b9330bbf57c1d98f79833699c2a8e885

Smooth exact-value complexity just below the zero-query threshold

### Native proof: ZO_PROOF_ENDPOINT_EXTENSION

Native pointer: /proofs/1; canonical SHA-256: 7b45cd9fdbb96071cbfd572f1f82843e1a824cf6c3c12058a9c10276f986b427

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: bd9a0c4e5638359ee1a13c852d259c8991d3ff9f277411c58d1efc3dfc306beb

The endpoint lower bound at $Q=3$ yields $\Omega(d)$ for every $Q\ge3$. The deterministic finite-difference accelerated bound is $O(d)$ on every fixed numerical interval $4\le Q\le128^2$.

Solving to a smaller error also solves to any larger error, so minimax complexity is nondecreasing as $\varepsilon$ decreases. At $Q=3$, the endpoint lemma gives $\gamma=1/3$ and hence a uniform $\Omega(d)$ randomized lower bound. The deterministic accelerated upper bound $O(d\sqrt Q)$ is at most $128$ times its universal constant on the stated interval. The same upper bound applies to randomized algorithms. The endpoint hard family is already quadratic, so the lower statement transfers unchanged to the quadratic subclass; the quadratic upper follows by restriction of the smooth algorithm.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/1/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: module_dependencies

Native pointer: /proofs/1/module_dependencies; canonical SHA-256: a7a3fc655588cd4b894c69b7420479caed78513f7dd6d4681562c51ab6fe8700

#### Native item 1

Native pointer: /proofs/1/module_dependencies/0; canonical SHA-256: 4f452d8ed97f47aa7c2654ceb7664669c9a18956dbc24e82de952de25319fbab

ZO_PROOF_SMOOTH_ENDPOINT

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: ed532264f16f32501db08bf6139fbbf5d892fc51c4d84a1cf486033b5c058dda

All model budgets are fixed while accuracy varies; exact unrestricted value access.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: ab23a528d7deb23726a446bfe5198e14f299c649577dc9c8aa9f42b6f8dac664

Extending the endpoint bound to fixed accuracy windows

### Native proof: ZO_PROOF_PRECISION_LOG

Native pointer: /proofs/2; canonical SHA-256: 3669c61a80d81bbe0aa60db6734f4240fa0120356dbe68abfd4212e4b9184177

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: 22a37def08b7d321ee101fa614c49bf15f038bb3f82579c82fc250f797c52cb7

For the smooth class, $Q\ge128^2$ gives $\Omega(d\log Q)$. This also holds in a public strongly convex class with $\kappa\ge2$. For a ball-restricted Lipschitz class, $A=LR/\varepsilon\ge6\cdot128^2$ gives $\Omega(d\log A)$.

Dorn et al., Theorem 2.5, gives
$$\frac{3d}{4000}\left[1+\frac{\log(\beta_hR_h^2/\varepsilon)}{\log((\beta_h+\mu_h)/(\beta_h-\mu_h))}\right]$$
when $\mu_h/\beta_h\in[1/2,1]$ and $\beta_hR_h^2/\varepsilon\ge128^2$. Choose $\mu_h=\beta_h/2$, so the denominator is $\log3$. A convex $\beta$-smooth class contains this subclass with $\beta_h=\beta$, $R_h=R$. A public lower curvature budget $\mu\le\beta/2$ also contains it, uniformly in the public condition number.

For the ball-restricted Lipschitz class choose $R_h=R/2$, $\beta_h=2L/(3R)$, and $\mu_h=\beta_h/2$. On $B_2(R)$, $\|\nabla f(x)\|\le\beta_h(\|x\|+\|x_*\|)\le L$, and the global minimizer remains inside the feasible ball. One source value simulates one restricted value. The stronger source oracle permits all such algorithms, and $Q_h=A/6$. The explicit window makes $\log(A/6)$ and $\log A$ uniformly comparable.

For a selected-component finite sum with all components equal to the same hard function, one component query is one source query. This transfer has cost one, not $n$. A logarithmic and a dimension-dependent lower bound may be maximized only where both respective windows hold.

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/2/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 33d1886dbfecb60ab07affb5a5b70ec72413f57bba3bcdaee7db562519fff3ce

The source theorem retains its unrestricted query/output domain, fixed query cap, and stated accuracy window.

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /proofs/2/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 7d6c3836ee73380d5185e810548c207da824c054e9f2dcfc9d6a1af7c006e12b

Explicit logarithmic lower bounds and class restrictions

### Native proof: ZO_PROOF_ZERO

Native pointer: /proofs/3; canonical SHA-256: 1d6580814630c8e2805d1bef988f17262747efcfe8580ea0d6eaace3086f220c

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: e337fe1bbdc7a8471c27bff8578ac9695fda39f5bd738324501658aee12cbc83

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/3/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: 1415baad26ae3bdb7a7f19af0ab941587cafa672fc7447677224c888ab47c12b

The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: a1c4db43e97db238b9e152f2d0f29dccb6ee901b91806fdf8840d239abdee28f

Zero-query certificates

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 4e73863730dc8d7d5d272beb1798c68e9e336d4d81b8aa197a0594b4b29b9fa4

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 1b291f50806bb85c139ba66b9624181fc224107039f795697a082f2c5127f715

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 91c457ef63c2d9e9f1e623569670f8729886ed893da7b795a314aaa709572684

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 1cd35066ec2547e32eb4793e9541456366e48e351ac3cd3f112ccd662ca73acf

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 760ad704afd94b23aed633aba6042aceee01397bf227ef8041e18ad5b605d152

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 997b1b1ae05457680ae56d22621b984b974bc53a841aba45f4c6f19c19c0e15d

32<=Q<=d^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 3e3d5c9ef16fcbef809b228ff790735cd08a3c6be91cb4102dcb371822ada0c8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 997b1b1ae05457680ae56d22621b984b974bc53a841aba45f4c6f19c19c0e15d

32<=Q<=d^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 4a7b518cadfbdccaf54a3f8a8118368859c96697e42ed7ef5de0b71f96ba0da6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 65d306254f6f3c7c98a2e9e2cfe05513cc29695f1dbe0cbc93309183f4ea784e

The retained b2 lower rate is at least order d throughout this cell.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: 3611d38dd0698cfff98d9caa90302ab35ccbd527a11ae05d81020ca9e3335ead

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 98d783f7498ce31c5ac32fb5837e941a7f57343dedad8c4de7b407f6ee2ac90b

On bounded-Q overlap, b1 is already O(d); no asymptotic gain.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: b4dd8d555760cd22cb7040129711851f3ae56b57f70dbbf87ef3617e7843c77c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: e98ec75fd745a38c5e51d94e3c3732b46c3b1a8afed2beef6f21088a97fbe3ce

On its overlap, log Q <= sqrt Q, so b2 already gives the stronger rate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/bound_uses/5; canonical SHA-256: c59aeef0e862539b732b3a7ec9f4fa77cacad0ee5ec78b23a6576b94ee3b42ac

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/bound_id; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/bound_uses/6; canonical SHA-256: e09a7a2c75ff30abe894877650347b4482b0a0a3b218f9abb93714b56a50fb68

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/bound_id; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 8

Native pointer: /joint_analysis/comparisons/0/bound_uses/7; canonical SHA-256: af653e3aef2d067e2015845e31a8c4145577a81e1cab3f45ae4c0d6af2908c7f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/bound_id; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native item 9

Native pointer: /joint_analysis/comparisons/0/bound_uses/8; canonical SHA-256: 082a69dc85941dbfcfe57b2bdd0d2db8a573dac1332c3b2c165a7aba5741fc91

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/bound_id; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 24f6eedae39d7bc1cd578681ef266e2ba588a57404686ab1ed8af20f8ae41766

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 1623f2c742d4506a89d709bea1c99f547d0a1f72ce0910d01982002b4714da24

Q=32 belongs here only when d^2>=32; otherwise it belongs to c2.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 94d3cef7608ccd50719b764b477f3c8adc318b36f9515ba4fc8fa0357e5bb260

Q=d^2 is included here; upper and lower rates are both order d^2.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: a40f0afbd348ce5c8ffd5b87ccd9181748aeb15e7921cf248ad81bef4589bf2b

The quadratic lower-family saturation is not a full-class reconstruction upper bound.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 76b79d0494fc995e4407609b1b0f32b3356a42d5e35bbe3dc1a2c819b259db85

SO_ZO_E03__deterministic__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: dc08fa72625a3de4530532a78dfeba8561551fd71c26aa66ab8c176109ae894a

$O(1)$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 56a7d83b93fc7928ef7ef6598f1c795e0edf185dd48bf150f50698d59adc0952

\Omega(d\sqrt Q)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: ac0c4bd84854139bfcd6cf4dcb3b7c1b434a006e5f496c897df44f2f339c96ed

None at the recorded rate level; conditional baseline retention.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 5d767db3473334bcb4eef62baf0dbb46f7365d15ba694299bc8cf82a0fcf0e79

O(d\sqrt Q)

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 2dc8653a6c9ae77332c6c6b2b533c24da9f4d05a22d2630d840edf215e38fa62

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 576415bee47a529f03b5a1e50c9aaa36054830fb5919de66640dc70848cecf07

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 4cdf2c67b73bff57962fb112018d4125e74d8b1893a734f5fbb03dd807ae7cab

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: c08a56e208d821372a97ac3b17f1ffb5b35a95407eba049b3d5507c9df5f3a1c

Q>=32,Q>d^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 0600d064ac696e871ffaa22db89da999f8cbb8347fa28d95aac4cee82df7098b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: c08a56e208d821372a97ac3b17f1ffb5b35a95407eba049b3d5507c9df5f3a1c

Q>=32,Q>d^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 4a7b518cadfbdccaf54a3f8a8118368859c96697e42ed7ef5de0b71f96ba0da6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 65d306254f6f3c7c98a2e9e2cfe05513cc29695f1dbe0cbc93309183f4ea784e

The retained b2 lower rate is at least order d throughout this cell.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: 3611d38dd0698cfff98d9caa90302ab35ccbd527a11ae05d81020ca9e3335ead

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 98d783f7498ce31c5ac32fb5837e941a7f57343dedad8c4de7b407f6ee2ac90b

On bounded-Q overlap, b1 is already O(d); no asymptotic gain.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: 64ba6bf2cebb861902c556a512b4da2ae42eb628b9697718de0396f2f989f6a5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: c00795bfc8d4d6c88352021f9347da732915145ebe63851c66536983750e9944

Q>=32,Q>d^2 AND Q>=128^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: c59aeef0e862539b732b3a7ec9f4fa77cacad0ee5ec78b23a6576b94ee3b42ac

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/bound_uses/6; canonical SHA-256: e09a7a2c75ff30abe894877650347b4482b0a0a3b218f9abb93714b56a50fb68

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/bound_id; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 8

Native pointer: /joint_analysis/comparisons/1/bound_uses/7; canonical SHA-256: af653e3aef2d067e2015845e31a8c4145577a81e1cab3f45ae4c0d6af2908c7f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/bound_id; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native item 9

Native pointer: /joint_analysis/comparisons/1/bound_uses/8; canonical SHA-256: 082a69dc85941dbfcfe57b2bdd0d2db8a573dac1332c3b2c165a7aba5741fc91

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/bound_id; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: c606163bf1662d3b5ceaae2a1290f9b51a24f5bef76feda822771c1e6b274d8b

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 720fad7b107d1892dfc9cc26cda6f230e320ecea1921ec4d5881852aed568665

Q>d^2 is strict; Q=d^2 belongs to c1.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 3a0bbc103ffbf44176db469eea9f8752b216633f26b95e6703d40e6fb4ddbd9c

Q=128^2 activates b6 exactly as its source guard; it is not an intrinsic phase transition.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: b5c6bbc54bfa7089948739a030c08a5a7d97f533fb322ce3bec8fddb3fd63481

The upper crossover sqrt Q ~ d log Q and lower crossover log Q ~ d are asymptotic comparisons of rate terms.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: 1034600bbb0acf73dc4bad9c4ea1d1422fdc86498fb9aed62e817f2979286d23

At d=1 and Q>=128^2, both retained sides are order log Q; the cell-wide gap label is not a pointwise lower bound on the gap.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 450ebec716e7f5c2c54f4251d6263ce8019c85a8378d1cce288b5349a45023b4

$O(\log Q)$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 693fa0e6b192b2fd4da5d79b552db044cffbbef6e3d1db6a49e75a033b3cb845

\begin{cases}\Omega(d^2),&Q<128^2,\\\Omega(\max\{d^2,d\log Q\}),&Q\ge128^2.\end{cases}

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 78a6f2c3909990beacd9d861039e56a16fb2ca0d23e44ad2941b59f141371010

The recorded joint upper/lower rates need not match throughout this cell; the label O(log Q) is an upper bound on their ratio, not a proof of an unavoidable gap.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: e20b158ebb1822b53881d2023dafd5ea3922f0a711fa14cef68c885baa9f35cf

O(\min\{d\sqrt Q,d^2\log Q\})

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 7e19de4a27e8c5953e124d341b2f7de857f2efed11cd40f61cc72899ab28cfe8

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 160066a365fc5a495b48b2465c1e5b664042530b7e43c157fad448db20a0ae01

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 997aadad94d7208b3990de54db5f301d220547e9266e7ccc19bc131c7f9d581f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 73387149c476db721bde894318593e4f6c388f359e3ae101e738fa1ac6f26273

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: 1ded3d1c81bcad12b0ee913c2ad4ce89484fa91f22cf9f9092dc7776a3cb422b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: 2dd905aa42af45eb89ef20bc3d477dede43a75255d2941861df615e5ab8453fa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: c5ad36477f7cae7f17ac802fd9d809d815086a40650f5bc3f7271c688f49d4bb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native item 6

Native pointer: /joint_analysis/comparisons/2/bound_uses/5; canonical SHA-256: 1369a21eb1b687c4e149d26a0c22105164eb508dd722c8f60c673477fcc00c55

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/adopted_region; canonical SHA-256: ede48c35230e73a8437a18dbfbc2f9b5b1f8114ea6b790aa6b0041df4242996a

Q<=2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/bound_id; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 7

Native pointer: /joint_analysis/comparisons/2/bound_uses/6; canonical SHA-256: 2bbff84a20e89de607d8b40521ee52cdc1fe56aabd6866078fc1745354f61e8d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/adopted_region; canonical SHA-256: ede48c35230e73a8437a18dbfbc2f9b5b1f8114ea6b790aa6b0041df4242996a

Q<=2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/bound_id; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 8

Native pointer: /joint_analysis/comparisons/2/bound_uses/7; canonical SHA-256: af653e3aef2d067e2015845e31a8c4145577a81e1cab3f45ae4c0d6af2908c7f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/bound_id; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native item 9

Native pointer: /joint_analysis/comparisons/2/bound_uses/8; canonical SHA-256: 082a69dc85941dbfcfe57b2bdd0d2db8a573dac1332c3b2c165a7aba5741fc91

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/bound_id; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 7ebefd8567ab7839b36e68101cadd8bc183737090b8cafc32b710b72abd3ff87

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: dafa7d50ebd337af49ab62e25ed56facd92d4ace29cc6b1d09abff7350308b38

Q=2 is included: output 0 has gap <= beta R^2/2 = epsilon.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: bebe3f6eda1b0b4eb129f8709f1aa4d7faeca8a239e0c405c8130f3d4ec844f7

Both exact costs are zero; no upper/lower ratio is defined.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/boundary_checks/2; canonical SHA-256: 48f7694247e8de9fc7ff6fb2a163bf86c138e08bf4e61924569369d22daaabf8

For every Q>2, disjoint translated-quadratic success balls rule out zero calls; this does not establish a main-rate improvement.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 12b19b3ea5bfdcb615f3032fad2378489f623f29b7ae19c968fd7011adf2c018

SO_ZO_E03__deterministic__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: e464cc3ae79f7a934bec979b9cd4699a72e094503fcfcc217c28b54f3a0e8491

Not applicable: exact cost 0.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: ac0c4bd84854139bfcd6cf4dcb3b7c1b434a006e5f496c897df44f2f339c96ed

None at the recorded rate level; conditional baseline retention.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 86f0e06eebf3b4b561dcea8332dd3d43b6c0e54f4b80654db7f8eab471dbcc49

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 381ba9620dcfd7493de2816997b5f179a9d7f4848412eabc23db7fcc612ec92b

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: 997aadad94d7208b3990de54db5f301d220547e9266e7ccc19bc131c7f9d581f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 73387149c476db721bde894318593e4f6c388f359e3ae101e738fa1ac6f26273

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 67721a8cf73ae69e9f16718f75effe36000a7295c700663e1785c8a887d20aa3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 0feb814fc9c3d035e2e1665b380122eb00da82b36ff58b44c5590e7878f9b122

On 3<=Q<4, native b10 already gives Omega(d).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 2dd905aa42af45eb89ef20bc3d477dede43a75255d2941861df615e5ab8453fa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: c5ad36477f7cae7f17ac802fd9d809d815086a40650f5bc3f7271c688f49d4bb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/bound_uses/5; canonical SHA-256: c59aeef0e862539b732b3a7ec9f4fa77cacad0ee5ec78b23a6576b94ee3b42ac

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/bound_id; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 7

Native pointer: /joint_analysis/comparisons/3/bound_uses/6; canonical SHA-256: e09a7a2c75ff30abe894877650347b4482b0a0a3b218f9abb93714b56a50fb68

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/bound_id; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 8

Native pointer: /joint_analysis/comparisons/3/bound_uses/7; canonical SHA-256: d867675ec6c6cebffda1e04a08cf146e8090141a9d1952b8c4fbbde2fd363791

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/adopted_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/bound_id; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native item 9

Native pointer: /joint_analysis/comparisons/3/bound_uses/8; canonical SHA-256: 37c78412246ce8fac746ba6e6bd1d0c559c47112e82577735b632cfbdeffacfa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/adopted_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/bound_id; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: 6cabfbcb35d09fdd7ce90f015a2f794a08c53ac8e439d6167ae09e92d2af9512

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: a085a3a48ec995939f79ddb474b73fc29e403e5035fba8336c08615a29cb4a91

Both Q=2 and Q=4 are excluded.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: 5868e181713a2738c208e1d6d75e4087b5f071612d28d548febbd28f6506700b

gamma=1-2/Q varies jointly; it is not an allowed hidden-constant dependency.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/boundary_checks/2; canonical SHA-256: e7cf4518fb308f67fe421f5d59c3e2495cc08d85fb0e41e804136e1d724fdd5e

The deterministic retained rate remains Theta(d), even as Q decreases to 2.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/boundary_checks/3; canonical SHA-256: d4e42e914f9bf45e4656c49192653321938963237094a907ee653fc2caba18e5

The endpoint proof uses finite positive differences only on the open interval; Q=4 is handled by c5.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 227d1d31afdd2a12fe37a590fed81e64f6f52546880671e1e4a386ec04c5e6b3

SO_ZO_E03__deterministic__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: dc08fa72625a3de4530532a78dfeba8561551fd71c26aa66ab8c176109ae894a

$O(1)$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 2c3270cd326857cb83ddaf05fc93e833998ac4db0784515c3d2791b08b50a98d

\Omega(d)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: ac0c4bd84854139bfcd6cf4dcb3b7c1b434a006e5f496c897df44f2f339c96ed

None at the recorded rate level; conditional baseline retention.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: 53c161ebcd5437ab4f1131346ff84094e563b8e4c49eeda8799494631a05aaef

O(d)

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: ec7b080f61cac681f7cc9789eef93f053a7122290b39aec2c43924fe79cca5c9

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: 93a607a5b9eabb8ea27daec098a55873fc0d65527fb8d320d1c21e22c6a792bd

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: 997aadad94d7208b3990de54db5f301d220547e9266e7ccc19bc131c7f9d581f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: 73387149c476db721bde894318593e4f6c388f359e3ae101e738fa1ac6f26273

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: d373f08a61349423eec1c51f94d20521ce9b6ccca5fe56cdf5d3d9828568ceda

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: c7aa6ee7623a43dc97006f0be860940b9f6551118e4ba82cd04556a70415819a

4<=Q<32

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/bound_uses/3; canonical SHA-256: ae2c802476c46808d298366f172f09e322566165c98980e35324bb4d4b41e303

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/adopted_region; canonical SHA-256: c7aa6ee7623a43dc97006f0be860940b9f6551118e4ba82cd04556a70415819a

4<=Q<32

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/bound_id; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/validity_region; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/bound_uses/4; canonical SHA-256: c5ad36477f7cae7f17ac802fd9d809d815086a40650f5bc3f7271c688f49d4bb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/bound_id; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/validity_region; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native item 6

Native pointer: /joint_analysis/comparisons/4/bound_uses/5; canonical SHA-256: c59aeef0e862539b732b3a7ec9f4fa77cacad0ee5ec78b23a6576b94ee3b42ac

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/bound_id; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 7

Native pointer: /joint_analysis/comparisons/4/bound_uses/6; canonical SHA-256: e09a7a2c75ff30abe894877650347b4482b0a0a3b218f9abb93714b56a50fb68

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/bound_id; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 8

Native pointer: /joint_analysis/comparisons/4/bound_uses/7; canonical SHA-256: af653e3aef2d067e2015845e31a8c4145577a81e1cab3f45ae4c0d6af2908c7f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/bound_id; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native item 9

Native pointer: /joint_analysis/comparisons/4/bound_uses/8; canonical SHA-256: 082a69dc85941dbfcfe57b2bdd0d2db8a573dac1332c3b2c165a7aba5741fc91

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/bound_id; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: 31bbbcd0280f83480b17af8b5f9d198c1e87e2437e2f158e8ea92193cd7b4f85

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: a96733f29f580dba2d1b436987a3bede5651479c8a18239861f342aff054267b

Q=4 is included; the open endpoint proof is not used there.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/boundary_checks/1; canonical SHA-256: 4468ef51ed7b77143116eb5d62ae0cc6bd8d50b45b843dc54cf9a635436d94d9

Q=32 is excluded and goes to c1 or c2.

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/boundary_checks/2; canonical SHA-256: 5ecb6d6e7b8815009062b7013d26f7d782482f481aca6eb1591b04ae3249082f

This is a fixed numerical window, not a slice with a hidden Q-dependent constant.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: 86afe548392f2a0adbd98399d9e7405f732fef457ca3bafd924a84e549dc6c85

SO_ZO_E03__deterministic__c5

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: dc08fa72625a3de4530532a78dfeba8561551fd71c26aa66ab8c176109ae894a

$O(1)$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: 2c3270cd326857cb83ddaf05fc93e833998ac4db0784515c3d2791b08b50a98d

\Omega(d)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: ac0c4bd84854139bfcd6cf4dcb3b7c1b434a006e5f496c897df44f2f339c96ed

None at the recorded rate level; conditional baseline retention.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: 53c161ebcd5437ab4f1131346ff84094e563b8e4c49eeda8799494631a05aaef

O(d)

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: c9d619fc0f849a1869ab6cd76b2d18e63438680243b9271a8dfa474a68245a34

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: b1a43868f2fe1eed0c301506e20366e9ccc13dec84c514aef390db71cd9d9fc0

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: 95f1d2db5ea8dcaa103023096a79acdee81e9ffa721049f8d8063ca5498c51c6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: 997b1b1ae05457680ae56d22621b984b974bc53a841aba45f4c6f19c19c0e15d

32<=Q<=d^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: fd6f66da199a713e37185cc63962e4c180b953a7e343ff4d65da5a000fcb9187

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: 997b1b1ae05457680ae56d22621b984b974bc53a841aba45f4c6f19c19c0e15d

32<=Q<=d^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: 3ce5b5d1bdb26324cadabc6c67b055fa89d6bbf61febfe4ba1c78f3431177498

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: 65d306254f6f3c7c98a2e9e2cfe05513cc29695f1dbe0cbc93309183f4ea784e

The retained b2 lower rate is at least order d throughout this cell.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/bound_uses/3; canonical SHA-256: a032820616f4cfb6fa90213ad8fcaeb01feb785ee88d728b0c4a6b9d9419256a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/bound_id; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/reason; canonical SHA-256: 98d783f7498ce31c5ac32fb5837e941a7f57343dedad8c4de7b407f6ee2ac90b

On bounded-Q overlap, b1 is already O(d); no asymptotic gain.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/validity_region; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/5/bound_uses/4; canonical SHA-256: 31940ddf1924b98efecfa61b20ac31634c8437fee77e72d46a76aeb68733d5ee

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/bound_id; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/reason; canonical SHA-256: e98ec75fd745a38c5e51d94e3c3732b46c3b1a8afed2beef6f21088a97fbe3ce

On its overlap, log Q <= sqrt Q, so b2 already gives the stronger rate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/validity_region; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native item 6

Native pointer: /joint_analysis/comparisons/5/bound_uses/5; canonical SHA-256: 9032fa6cde935066c5c82ef7d2956a8a86025b4a95f4b5def32ce832260cbb90

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/bound_id; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 7

Native pointer: /joint_analysis/comparisons/5/bound_uses/6; canonical SHA-256: 01d29e344521ffe8a44dbb7d4b5d8c78e2886718ef3754d71e37ef6629f0cfe7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/bound_id; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 8

Native pointer: /joint_analysis/comparisons/5/bound_uses/7; canonical SHA-256: 991389b3066ff506f39c7d6868950b7a375aa5d24ab9f291381b70edc5643c40

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/bound_id; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native item 9

Native pointer: /joint_analysis/comparisons/5/bound_uses/8; canonical SHA-256: 818503a97c5abda1cc95e5cc5d377c76e689253e2f03e6149469f3717607662a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/bound_id; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: 24f6eedae39d7bc1cd578681ef266e2ba588a57404686ab1ed8af20f8ae41766

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: 1623f2c742d4506a89d709bea1c99f547d0a1f72ce0910d01982002b4714da24

Q=32 belongs here only when d^2>=32; otherwise it belongs to c2.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/boundary_checks/1; canonical SHA-256: 94d3cef7608ccd50719b764b477f3c8adc318b36f9515ba4fc8fa0357e5bb260

Q=d^2 is included here; upper and lower rates are both order d^2.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/boundary_checks/2; canonical SHA-256: a40f0afbd348ce5c8ffd5b87ccd9181748aeb15e7921cf248ad81bef4589bf2b

The quadratic lower-family saturation is not a full-class reconstruction upper bound.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: 700e3e7f14852da0d2d74c023842061de90daeed23df99c1191130feab77b6dc

SO_ZO_E03__randomized__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: dc08fa72625a3de4530532a78dfeba8561551fd71c26aa66ab8c176109ae894a

$O(1)$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: 56a7d83b93fc7928ef7ef6598f1c795e0edf185dd48bf150f50698d59adc0952

\Omega(d\sqrt Q)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: ac0c4bd84854139bfcd6cf4dcb3b7c1b434a006e5f496c897df44f2f339c96ed

None at the recorded rate level; conditional baseline retention.

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: 5d767db3473334bcb4eef62baf0dbb46f7365d15ba694299bc8cf82a0fcf0e79

O(d\sqrt Q)

#### Native item 7

Native pointer: /joint_analysis/comparisons/6; canonical SHA-256: 20c7b889b8149e1a7cc61e2471f2b4ed1d1c2a2c40aa0a5389d8b63ebd3616ec

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/6/bound_uses; canonical SHA-256: b574428f0ee813419c7940410d8f2f39997306c15512e2f97fff32bc5d4e7623

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0; canonical SHA-256: 90424ee9c8c5ac9cf1251fb2a352714bb1883b69172e55feee1a12735f24c77a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/adopted_region; canonical SHA-256: c08a56e208d821372a97ac3b17f1ffb5b35a95407eba049b3d5507c9df5f3a1c

Q>=32,Q>d^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/bound_id; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/1; canonical SHA-256: 2cf2fc10e7862605ad2456f6f40c2d231c149659f34baa2e6aa8500ef67225e6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/adopted_region; canonical SHA-256: c08a56e208d821372a97ac3b17f1ffb5b35a95407eba049b3d5507c9df5f3a1c

Q>=32,Q>d^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/bound_id; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/bound_uses/2; canonical SHA-256: 3ce5b5d1bdb26324cadabc6c67b055fa89d6bbf61febfe4ba1c78f3431177498

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/bound_id; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/reason; canonical SHA-256: 65d306254f6f3c7c98a2e9e2cfe05513cc29695f1dbe0cbc93309183f4ea784e

The retained b2 lower rate is at least order d throughout this cell.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/validity_region; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/bound_uses/3; canonical SHA-256: a032820616f4cfb6fa90213ad8fcaeb01feb785ee88d728b0c4a6b9d9419256a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/bound_id; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/reason; canonical SHA-256: 98d783f7498ce31c5ac32fb5837e941a7f57343dedad8c4de7b407f6ee2ac90b

On bounded-Q overlap, b1 is already O(d); no asymptotic gain.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/validity_region; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/6/bound_uses/4; canonical SHA-256: fa8fb5778e1191000b84066e518daf6a5eb77b473c6c86eb71e3dc54c68796b2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/adopted_region; canonical SHA-256: c00795bfc8d4d6c88352021f9347da732915145ebe63851c66536983750e9944

Q>=32,Q>d^2 AND Q>=128^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/bound_id; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/validity_region; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native item 6

Native pointer: /joint_analysis/comparisons/6/bound_uses/5; canonical SHA-256: 9032fa6cde935066c5c82ef7d2956a8a86025b4a95f4b5def32ce832260cbb90

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/bound_id; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 7

Native pointer: /joint_analysis/comparisons/6/bound_uses/6; canonical SHA-256: 01d29e344521ffe8a44dbb7d4b5d8c78e2886718ef3754d71e37ef6629f0cfe7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/bound_id; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 8

Native pointer: /joint_analysis/comparisons/6/bound_uses/7; canonical SHA-256: 991389b3066ff506f39c7d6868950b7a375aa5d24ab9f291381b70edc5643c40

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/bound_id; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native item 9

Native pointer: /joint_analysis/comparisons/6/bound_uses/8; canonical SHA-256: 818503a97c5abda1cc95e5cc5d377c76e689253e2f03e6149469f3717607662a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/bound_id; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/6/boundary_checks; canonical SHA-256: c606163bf1662d3b5ceaae2a1290f9b51a24f5bef76feda822771c1e6b274d8b

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/boundary_checks/0; canonical SHA-256: 720fad7b107d1892dfc9cc26cda6f230e320ecea1921ec4d5881852aed568665

Q>d^2 is strict; Q=d^2 belongs to c1.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/boundary_checks/1; canonical SHA-256: 3a0bbc103ffbf44176db469eea9f8752b216633f26b95e6703d40e6fb4ddbd9c

Q=128^2 activates b6 exactly as its source guard; it is not an intrinsic phase transition.

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/boundary_checks/2; canonical SHA-256: b5c6bbc54bfa7089948739a030c08a5a7d97f533fb322ce3bec8fddb3fd63481

The upper crossover sqrt Q ~ d log Q and lower crossover log Q ~ d are asymptotic comparisons of rate terms.

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/boundary_checks/3; canonical SHA-256: 1034600bbb0acf73dc4bad9c4ea1d1422fdc86498fb9aed62e817f2979286d23

At d=1 and Q>=128^2, both retained sides are order log Q; the cell-wide gap label is not a pointwise lower bound on the gap.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/6/comparison_id; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/6/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/6/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/6/gap; canonical SHA-256: 450ebec716e7f5c2c54f4251d6263ce8019c85a8378d1cce288b5349a45023b4

$O(\log Q)$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/6/lower_envelope; canonical SHA-256: 693fa0e6b192b2fd4da5d79b552db044cffbbef6e3d1db6a49e75a033b3cb845

\begin{cases}\Omega(d^2),&Q<128^2,\\\Omega(\max\{d^2,d\log Q\}),&Q\ge128^2.\end{cases}

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/6/remaining_gap; canonical SHA-256: 78a6f2c3909990beacd9d861039e56a16fb2ca0d23e44ad2941b59f141371010

The recorded joint upper/lower rates need not match throughout this cell; the label O(log Q) is an upper bound on their ratio, not a proof of an unavoidable gap.

#### Native field: role

Native pointer: /joint_analysis/comparisons/6/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/6/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/6/upper_envelope; canonical SHA-256: e20b158ebb1822b53881d2023dafd5ea3922f0a711fa14cef68c885baa9f35cf

O(\min\{d\sqrt Q,d^2\log Q\})

#### Native item 8

Native pointer: /joint_analysis/comparisons/7; canonical SHA-256: d1c0ca517225e0c73d23d17bbbe9337dbd456d58a4b48717ab531028bcb743a9

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/7/bound_uses; canonical SHA-256: 484d8a259780690c8dce37cd61916c2e6744ce1e27f068c9ec13ddf854e93010

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/0; canonical SHA-256: 066de35c2161c445bce1476b10514db53be13e89b39a92219080495c94eeb117

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/bound_id; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/bound_uses/1; canonical SHA-256: ae2e28032392ef3326d360f66f6a801af95495387f7950902235a2852ac5cb77

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/bound_id; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/bound_uses/2; canonical SHA-256: dd06025a632112a9f6c6ce41950935ae45604af65be6ea39e004b99f9dccddb1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/bound_id; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/validity_region; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native item 4

Native pointer: /joint_analysis/comparisons/7/bound_uses/3; canonical SHA-256: 004b5029b68586bea65102b9c3c950aa2612a5ca1ebca162783536eb255c1bad

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/bound_id; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/validity_region; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/7/bound_uses/4; canonical SHA-256: 5d4c93a2a6fc194d9eb4ea884ca904ebd819cba0c2aad5f6a4d52a8062972dac

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/bound_id; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/validity_region; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native item 6

Native pointer: /joint_analysis/comparisons/7/bound_uses/5; canonical SHA-256: ead86ef0274ea9493f3617760f5367b9e243e323b256c839c6dc93ff0ce79e62

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/adopted_region; canonical SHA-256: ede48c35230e73a8437a18dbfbc2f9b5b1f8114ea6b790aa6b0041df4242996a

Q<=2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/bound_id; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 7

Native pointer: /joint_analysis/comparisons/7/bound_uses/6; canonical SHA-256: 9873de62330dd9f61a8b0d357c6841d91fe6c252d050ac84494eb3219b761672

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/adopted_region; canonical SHA-256: ede48c35230e73a8437a18dbfbc2f9b5b1f8114ea6b790aa6b0041df4242996a

Q<=2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/bound_id; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 8

Native pointer: /joint_analysis/comparisons/7/bound_uses/7; canonical SHA-256: 991389b3066ff506f39c7d6868950b7a375aa5d24ab9f291381b70edc5643c40

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/bound_id; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native item 9

Native pointer: /joint_analysis/comparisons/7/bound_uses/8; canonical SHA-256: 818503a97c5abda1cc95e5cc5d377c76e689253e2f03e6149469f3717607662a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/bound_id; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/7/boundary_checks; canonical SHA-256: 7ebefd8567ab7839b36e68101cadd8bc183737090b8cafc32b710b72abd3ff87

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/boundary_checks/0; canonical SHA-256: dafa7d50ebd337af49ab62e25ed56facd92d4ace29cc6b1d09abff7350308b38

Q=2 is included: output 0 has gap <= beta R^2/2 = epsilon.

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/boundary_checks/1; canonical SHA-256: bebe3f6eda1b0b4eb129f8709f1aa4d7faeca8a239e0c405c8130f3d4ec844f7

Both exact costs are zero; no upper/lower ratio is defined.

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/boundary_checks/2; canonical SHA-256: 48f7694247e8de9fc7ff6fb2a163bf86c138e08bf4e61924569369d22daaabf8

For every Q>2, disjoint translated-quadratic success balls rule out zero calls; this does not establish a main-rate improvement.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/7/comparison_id; canonical SHA-256: 3fdb6ec272a97b5caf48ac717a76436c472ecf6ea23dac40e6b71a0f4e40bc2a

SO_ZO_E03__randomized__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/7/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/7/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/7/gap; canonical SHA-256: e464cc3ae79f7a934bec979b9cd4699a72e094503fcfcc217c28b54f3a0e8491

Not applicable: exact cost 0.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/7/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/7/remaining_gap; canonical SHA-256: ac0c4bd84854139bfcd6cf4dcb3b7c1b434a006e5f496c897df44f2f339c96ed

None at the recorded rate level; conditional baseline retention.

#### Native field: role

Native pointer: /joint_analysis/comparisons/7/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/7/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/7/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native item 9

Native pointer: /joint_analysis/comparisons/8; canonical SHA-256: 85ca92c6ff19b4fa7e6647e150e8bdd48e157e4eedc54ee01a8c058c5475ccaf

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/8/bound_uses; canonical SHA-256: 36dba77a529f6aacb0602d6c51a9c7ab17d681fdef04f55374360fd3815086c2

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/0; canonical SHA-256: 066de35c2161c445bce1476b10514db53be13e89b39a92219080495c94eeb117

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/bound_id; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 2

Native pointer: /joint_analysis/comparisons/8/bound_uses/1; canonical SHA-256: ae2e28032392ef3326d360f66f6a801af95495387f7950902235a2852ac5cb77

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/bound_id; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 3

Native pointer: /joint_analysis/comparisons/8/bound_uses/2; canonical SHA-256: f5c6048c4c0b63166197f62c64abb5e21ea28082fa4bf16cc1adcf239bb01ecc

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/bound_id; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/reason; canonical SHA-256: 073b5f05f2bd3e6a27c41f69eeab27455993fcb1846df4ae38049c742dbbd923

On 3<=Q<4, gamma>=1/3 and native b11 already gives Omega(d).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/validity_region; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native item 4

Native pointer: /joint_analysis/comparisons/8/bound_uses/3; canonical SHA-256: 004b5029b68586bea65102b9c3c950aa2612a5ca1ebca162783536eb255c1bad

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/bound_id; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/validity_region; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/8/bound_uses/4; canonical SHA-256: 5d4c93a2a6fc194d9eb4ea884ca904ebd819cba0c2aad5f6a4d52a8062972dac

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/bound_id; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/validity_region; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native item 6

Native pointer: /joint_analysis/comparisons/8/bound_uses/5; canonical SHA-256: 9032fa6cde935066c5c82ef7d2956a8a86025b4a95f4b5def32ce832260cbb90

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/bound_id; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 7

Native pointer: /joint_analysis/comparisons/8/bound_uses/6; canonical SHA-256: 01d29e344521ffe8a44dbb7d4b5d8c78e2886718ef3754d71e37ef6629f0cfe7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/6/bound_id; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/6/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/6/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 8

Native pointer: /joint_analysis/comparisons/8/bound_uses/7; canonical SHA-256: 1e2f3ae29a5381e9c1f89ee713a79fdad023114574718d74eb455862410250f6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/7/adopted_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/7/bound_id; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/7/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/7/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/7/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native item 9

Native pointer: /joint_analysis/comparisons/8/bound_uses/8; canonical SHA-256: 39270d1f08e35dd886337a806526d33e5558456948925c64f6e9dcaf4ca97a57

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/8/adopted_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/8/bound_id; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/8/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/8/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/8/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/8/boundary_checks; canonical SHA-256: cc4e5ad89d815e7242710d10eca6b69f8792ea3679a47d442afe2ecec8d22a40

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/boundary_checks/0; canonical SHA-256: a085a3a48ec995939f79ddb474b73fc29e403e5035fba8336c08615a29cb4a91

Both Q=2 and Q=4 are excluded.

#### Native item 2

Native pointer: /joint_analysis/comparisons/8/boundary_checks/1; canonical SHA-256: 5868e181713a2738c208e1d6d75e4087b5f071612d28d548febbd28f6506700b

gamma=1-2/Q varies jointly; it is not an allowed hidden-constant dependency.

#### Native item 3

Native pointer: /joint_analysis/comparisons/8/boundary_checks/2; canonical SHA-256: d6a31aa44d915ff612dc57b559056eded44883039ed87b950ca34c0783ff3caa

If d gamma is bounded, the retained rate is Theta(1); if d gamma grows, it is Theta(d gamma).

#### Native item 4

Native pointer: /joint_analysis/comparisons/8/boundary_checks/3; canonical SHA-256: d4e42e914f9bf45e4656c49192653321938963237094a907ee653fc2caba18e5

The endpoint proof uses finite positive differences only on the open interval; Q=4 is handled by c5.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/8/comparison_id; canonical SHA-256: 2a04790fa2df16ccf10b9c03083b5c13ac10139b14919c22ab3c30a68ff3f432

SO_ZO_E03__randomized__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/8/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/8/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/8/gap; canonical SHA-256: dc08fa72625a3de4530532a78dfeba8561551fd71c26aa66ab8c176109ae894a

$O(1)$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/8/lower_envelope; canonical SHA-256: 319737cc93f6f0c6678d8159dcf433333c6ea70f33ada83a14783b9cfe780e21

\Omega(\max\{1,d(1-2/Q)\})

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/8/remaining_gap; canonical SHA-256: ac0c4bd84854139bfcd6cf4dcb3b7c1b434a006e5f496c897df44f2f339c96ed

None at the recorded rate level; conditional baseline retention.

#### Native field: role

Native pointer: /joint_analysis/comparisons/8/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/8/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/8/upper_envelope; canonical SHA-256: 3ad4dce61597e4f965da5f951691804238cab9f055883f2f5ea5fb26033c0819

O(\max\{1,d(1-2/Q)\})

#### Native item 10

Native pointer: /joint_analysis/comparisons/9; canonical SHA-256: 63967dcd329125af3bfa4cb925c4e5232e7a20ff93a500ecd292ef39483f8117

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/9/bound_uses; canonical SHA-256: 1bcd4590f641358f33372beefd5b587cebe74113c046cac61de366f6ed388293

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/0; canonical SHA-256: 066de35c2161c445bce1476b10514db53be13e89b39a92219080495c94eeb117

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/bound_id; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 2

Native pointer: /joint_analysis/comparisons/9/bound_uses/1; canonical SHA-256: ae2e28032392ef3326d360f66f6a801af95495387f7950902235a2852ac5cb77

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/bound_id; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/validity_region; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native item 3

Native pointer: /joint_analysis/comparisons/9/bound_uses/2; canonical SHA-256: 52a0e437c2e892f3db6a6576beaa4025f0dbf9491ab6d72ef8ba802bba9bf5dc

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/adopted_region; canonical SHA-256: c7aa6ee7623a43dc97006f0be860940b9f6551118e4ba82cd04556a70415819a

4<=Q<32

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/bound_id; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/validity_region; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native item 4

Native pointer: /joint_analysis/comparisons/9/bound_uses/3; canonical SHA-256: 295828fdb10ae1b215f81351f36979f18c9e9a33fa9171e8392976d1a63fb162

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/adopted_region; canonical SHA-256: c7aa6ee7623a43dc97006f0be860940b9f6551118e4ba82cd04556a70415819a

4<=Q<32

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/bound_id; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/reason; canonical SHA-256: d904161d23c1c32fa04412920f182045ec745f02ced1da83b2ae99292aa48657

Conditional retention of native active claim.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/validity_region; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/9/bound_uses/4; canonical SHA-256: 5d4c93a2a6fc194d9eb4ea884ca904ebd819cba0c2aad5f6a4d52a8062972dac

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/bound_id; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/validity_region; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native item 6

Native pointer: /joint_analysis/comparisons/9/bound_uses/5; canonical SHA-256: 9032fa6cde935066c5c82ef7d2956a8a86025b4a95f4b5def32ce832260cbb90

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/bound_id; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 7

Native pointer: /joint_analysis/comparisons/9/bound_uses/6; canonical SHA-256: 01d29e344521ffe8a44dbb7d4b5d8c78e2886718ef3754d71e37ef6629f0cfe7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/6/bound_id; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/6/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/6/validity_region; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native item 8

Native pointer: /joint_analysis/comparisons/9/bound_uses/7; canonical SHA-256: 991389b3066ff506f39c7d6868950b7a375aa5d24ab9f291381b70edc5643c40

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/7/bound_id; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/7/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/7/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native item 9

Native pointer: /joint_analysis/comparisons/9/bound_uses/8; canonical SHA-256: 818503a97c5abda1cc95e5cc5d377c76e689253e2f03e6149469f3717607662a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/8/bound_id; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/8/reason; canonical SHA-256: 619c98638417972c809099227adac8c76a794fa47866bf3394c7391381c8b139

Disjoint validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/8/validity_region; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/9/boundary_checks; canonical SHA-256: 31bbbcd0280f83480b17af8b5f9d198c1e87e2437e2f158e8ea92193cd7b4f85

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/boundary_checks/0; canonical SHA-256: a96733f29f580dba2d1b436987a3bede5651479c8a18239861f342aff054267b

Q=4 is included; the open endpoint proof is not used there.

#### Native item 2

Native pointer: /joint_analysis/comparisons/9/boundary_checks/1; canonical SHA-256: 4468ef51ed7b77143116eb5d62ae0cc6bd8d50b45b843dc54cf9a635436d94d9

Q=32 is excluded and goes to c1 or c2.

#### Native item 3

Native pointer: /joint_analysis/comparisons/9/boundary_checks/2; canonical SHA-256: 5ecb6d6e7b8815009062b7013d26f7d782482f481aca6eb1591b04ae3249082f

This is a fixed numerical window, not a slice with a hidden Q-dependent constant.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/9/comparison_id; canonical SHA-256: 041f5b5649f4314047eec02f84b36191fe9a6c71fc2ffd98e0933aca3d2e1008

SO_ZO_E03__randomized__c5

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/9/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/9/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/9/gap; canonical SHA-256: dc08fa72625a3de4530532a78dfeba8561551fd71c26aa66ab8c176109ae894a

$O(1)$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/9/lower_envelope; canonical SHA-256: 2c3270cd326857cb83ddaf05fc93e833998ac4db0784515c3d2791b08b50a98d

\Omega(d)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/9/remaining_gap; canonical SHA-256: ac0c4bd84854139bfcd6cf4dcb3b7c1b434a006e5f496c897df44f2f339c96ed

None at the recorded rate level; conditional baseline retention.

#### Native field: role

Native pointer: /joint_analysis/comparisons/9/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/9/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/9/upper_envelope; canonical SHA-256: 53c161ebcd5437ab4f1131346ff84094e563b8e4c49eeda8799494631a05aaef

O(d)

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 3b14675595d4479bfb6b702721f6a5ae50670b50c03b743f0adfbb85a28c2bc0

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 9d1b48d97f22f1deeaaa33d1d9efa155486f21074945339647507e5d070c9caf

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 385c105dea8bb942906401e41248a631d2c3e980b43c580831b20971aa77c361

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: b7ce3f814d0e14e74eb1dc742ad4a2c7a798413fb9771560f107cad87ef46402

zero

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: d4944c4f22238cfa78a780911be3a22a0121d2b4d1ead3b8c0eeaaa97225557a

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 12b19b3ea5bfdcb615f3032fad2378489f623f29b7ae19c968fd7011adf2c018

SO_ZO_E03__deterministic__c3

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: 3fdb6ec272a97b5caf48ac717a76436c472ecf6ea23dac40e6b71a0f4e40bc2a

SO_ZO_E03__randomized__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: a9e59d020f424e9cc2b2782624b7971a3a345b4456e69896c3b8cd45b96c0376

Exact zero cost in both views; no ratio.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: fb5709b7ada1d39d59dff7200c2fc51267a798eb1c39a857c4fe5227848cbf46

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: a2883e3744bce5f6e5da05fb2ac7600586ea31c1d4a8e38c5bd4388b3679e825

endpoint

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: a7a3fc655588cd4b894c69b7420479caed78513f7dd6d4681562c51ab6fe8700

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/0; canonical SHA-256: 4f452d8ed97f47aa7c2654ceb7664669c9a18956dbc24e82de952de25319fbab

ZO_PROOF_SMOOTH_ENDPOINT

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: fc74556868b0d9882b1299b408f6fa32fec40d5f95f4679f6796b0d973a61414

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 227d1d31afdd2a12fe37a590fed81e64f6f52546880671e1e4a386ec04c5e6b3

SO_ZO_E03__deterministic__c4

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: 2a04790fa2df16ccf10b9c03083b5c13ac10139b14919c22ab3c30a68ff3f432

SO_ZO_E03__randomized__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 67cba61450206dac8d851d8853ec503893e79b064fc273d910be32f7772daaee

Deterministic Theta(d); randomized Theta(max{1,d(1-2/Q)}), uniformly.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 717d762c058a692911c0859eecec457a4bfa5b4ca973eb00a0f94706999f4093

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 6fb87a60fe6605ee1203c9cde8253a82bdcbb1fd33f829346a7c4cbb3a8ccc61

constant_accuracy

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: cf1d752dc93674714e736ee1b8f78c46284d25600955f3d01c964f6b708da39e

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs/0; canonical SHA-256: 3a2ef0aeaa4f47239ccb28dd8a94f200e515fe07535c686da41e9872e8cb594e

ZO_PROOF_ENDPOINT_EXTENSION

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 25f740d30d8c993f579eb2b56f8010a5bd285a05b144555cbdad43d7e2b9eded

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 86afe548392f2a0adbd98399d9e7405f732fef457ca3bafd924a84e549dc6c85

SO_ZO_E03__deterministic__c5

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/1; canonical SHA-256: 041f5b5649f4314047eec02f84b36191fe9a6c71fc2ffd98e0933aca3d2e1008

SO_ZO_E03__randomized__c5

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 9eaea9555a7a10a8798d9e549c3383df83cbcc97e3c71f1f2fbda3cc8d89787f

Both views retain Theta(d) on this fixed numerical interval.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: c7aa6ee7623a43dc97006f0be860940b9f6551118e4ba82cd04556a70415819a

4<=Q<32

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: ec6016d169e546ea6331870d109c970e259b6bde6fb3c871bbe6c516d382ab8f

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: c6345cb20b5762d48d6a25fe26cbf888644bf3510ee83a73ae191fb59315d1d3

moderate_accuracy

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: bac9c9797cb31bace1f4e2e240a90689066eaa877e2d69a04effd9c323419059

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: 76b79d0494fc995e4407609b1b0f32b3356a42d5e35bbe3dc1a2c819b259db85

SO_ZO_E03__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/1; canonical SHA-256: 700e3e7f14852da0d2d74c023842061de90daeed23df99c1191130feab77b6dc

SO_ZO_E03__randomized__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: f46fbc042e9794297ca67dad4dd4517e374e41e91adcab9cd5adb7dec81286db

Both views retain matching order d sqrt Q. Existing optimal comparison states are conditionally retained; this metadata migration issues no new native-proof closure certificate for historical source-only records.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 997b1b1ae05457680ae56d22621b984b974bc53a841aba45f4c6f19c19c0e15d

32<=Q<=d^2

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: fa30a61df467c137ea98df408b8ccb905df13af2b86d384d814379b58d2f58b1

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: cb510d625c8e21766aa14c700790484e0222e915b42fa3bdb02876da0d97f939

high_accuracy

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 5499062830cf6a7334adf503b236780b8cd922529428638c175a168d6cacc476

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/1; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: fa4260eb03d99b613a8216e490f072cdf3cb4fe15646359fa1f3502158ed80d4

Both guarded sides are recorded; the joint gap need not be closed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: e5a94f97f53a5d7ecebca48703e9e8d651dfc03111bcd85b050996797ef7969e

Q>=32 AND Q>d^2

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: fd19eef5d3eceea2b6ef95cf889e74f32374b5b09707bff6d6a1aa5020239dcc

For Q>0, exactly one of Q<=2, 2<Q<4, 4<=Q<32, or Q>=32 holds. In the last branch exactly one of Q<=d^2 and Q>d^2 holds. Empty moderate cells at small d create no hole. Each cell has one comparison per view. Coverage records conditional baseline brackets, not global optimality.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: d95820fe870dd46e76c1a6ebf496f2a73054214af0148966ce40c22f30af7f1f

empty as a domain partition; literature beyond the finite exact-paper check is unassessed.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: b0d0cbcf597e136660bbf51f852fbea6204f97e33d408a9236c776a77c10a608

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 7dc6a4875754b9ad6d24f7c05e075f190a92579767eef927e1c6ec663e364710

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 3cb7ebb611965a5b3d1fa680e40b5cf336e47d7599bfb52832f59c6e3b4ac654

First joint annotation only. It exposes parameter roles, conditional provenance, candidate dispositions and endpoint conventions without changing scientific rows. The c2 label is a ratio upper bound; it does not claim a matching lower bound on that ratio. The four separate q2 rows are audited in the finding, not merged into q1.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: a719ebda0f7dfc209ddda61cd44a8910d0443575a9b6c7ddffe8d34840b96666

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 76b79d0494fc995e4407609b1b0f32b3356a42d5e35bbe3dc1a2c819b259db85

SO_ZO_E03__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/0/comparison_ids/2; canonical SHA-256: 12b19b3ea5bfdcb615f3032fad2378489f623f29b7ae19c968fd7011adf2c018

SO_ZO_E03__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/impact/0/comparison_ids/3; canonical SHA-256: 227d1d31afdd2a12fe37a590fed81e64f6f52546880671e1e4a386ec04c5e6b3

SO_ZO_E03__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/impact/0/comparison_ids/4; canonical SHA-256: 86afe548392f2a0adbd98399d9e7405f732fef457ca3bafd924a84e549dc6c85

SO_ZO_E03__deterministic__c5

#### Native item 6

Native pointer: /joint_analysis/impact/0/comparison_ids/5; canonical SHA-256: 700e3e7f14852da0d2d74c023842061de90daeed23df99c1191130feab77b6dc

SO_ZO_E03__randomized__c1

#### Native item 7

Native pointer: /joint_analysis/impact/0/comparison_ids/6; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native item 8

Native pointer: /joint_analysis/impact/0/comparison_ids/7; canonical SHA-256: 3fdb6ec272a97b5caf48ac717a76436c472ecf6ea23dac40e6b71a0f4e40bc2a

SO_ZO_E03__randomized__c3

#### Native item 9

Native pointer: /joint_analysis/impact/0/comparison_ids/8; canonical SHA-256: 2a04790fa2df16ccf10b9c03083b5c13ac10139b14919c22ab3c30a68ff3f432

SO_ZO_E03__randomized__c4

#### Native item 10

Native pointer: /joint_analysis/impact/0/comparison_ids/9; canonical SHA-256: 041f5b5649f4314047eec02f84b36191fe9a6c71fc2ffd98e0933aca3d2e1008

SO_ZO_E03__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 431459ca18eabae162d7865007f7f593f9d74b90aae179b2e1f7b981d33db800

SO_ZO_E03_joint_annotation_v1

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: d2ea7b81829da844a3fc61ea8efe90d673ec4abd092cded8f54f038a002a132f

Exactly the same ten native guarded brackets, organized over the full joint domain.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: fd0882d0269c1b1aacc6bb247c890eba7be6a8efcdcbec86c0a4c039fb1a84f5

The ten native guarded brackets; no joint_analysis was present.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: b88e3c8a06084bc726f0d52754d53b838d017592cf119f23f4d9a7716ab99c07

Entire target domain; every bound, guard, envelope and status is preserved.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 7518b4164396b077b03edc8888425e1f30f3a39dbfd79226af8c436e4c890173

d>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>0.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 9938a0e3f4674514de15a838b6765139c0ef5d54a7497dcd2fa4c2d996fae541

The five disjoint domain cells cover Q>0 for both registered views.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 5c75ab42d599c8df42e6d04a6c5098553e8efa8428db4909d9473dc18b902b42

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 8d5b4ec351e965550a5c0b89afc058627d7a8f2a660b53ad4a4483b0b5252c5d

The freshly read source matches the existing scalar-value model, unrestricted adaptive randomized algorithms, arbitrary output and fixed pathwise cap. Its lower-bound subclass is contained in the target; deterministic algorithms are covered. These results are already active.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 91b7349adf0b79247361a30738b58cfcaf2c50ac0f0998a9380fb5f2e3fd142b

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 76b79d0494fc995e4407609b1b0f32b3356a42d5e35bbe3dc1a2c819b259db85

SO_ZO_E03__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: 700e3e7f14852da0d2d74c023842061de90daeed23df99c1191130feab77b6dc

SO_ZO_E03__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/impact/1/comparison_ids/3; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: c16f0118173b68e02c0cf333e3e153e7b5bab6948caa348658d1e17353d87a42

SO_ZO_E03_dorn_v1_rate_screen

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 0dbf423ed81d3c08700e2a54fe80535df5b273547dfd542192c5f4f72e1830a5

Unchanged.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 93ab9fdf00b60028986af7fa59389c6a80221c3d2706ba19a6f965598e6b37db

U=O(min{d sqrt Q,d^2 log Q}); L=Omega(d min{d,sqrt Q}), augmented by Omega(d log Q) only for Q>=128^2.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 132b76ea16729093259e1f2a8f4591e9346b44a3ccf57277026ce3828deae4f3

All registered principal-accuracy cells.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: f5a969f9fcc9adeea2e2c8c49dcb011a740ffbe9fd33031debfb4f8cf9503b52

Theorem 2.1: Q>=32; Theorem 2.5 transfer at mu=L/2: Q>=128^2.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 580631287faf9f3f09f2ed9539ec69b4c417bacc082076d23f19ce493ac14449

The source expressions coincide with active b1,b2,b6 in each view.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: fecd4ab7441787991866e3e316b42558746cb4b945f97b98e7c625909aee16cc

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 20209e27554b20a3a265f291b9b2f3670deb0217d9ff685237747b8a4b39f462

A subclass upper bound cannot be transferred upward to the full class. Theorem 2.5 likewise supplies an upper bound only under its strong-convexity assumption; that assumption is absent here.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 5499062830cf6a7334adf503b236780b8cd922529428638c175a168d6cacc476

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 9358f87a468fe4329d11a8b40f99dee725fc56683f71a55d465f9e82f23cd96f

SO_ZO_E03_quadratic_upper_screen

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 0dbf423ed81d3c08700e2a54fe80535df5b273547dfd542192c5f4f72e1830a5

Unchanged.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 95a3bad26987d8539cf75bf040ffa00680ebed7ae6240ea08ea254702f5d22b3

Full-class U=O(min{d sqrt Q,d^2 log Q}).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 37a31a96711109d28c436984d600a5bba453a29b25173cc0892850dfc69c550c

Entire fixed target.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 85945c38c3fbff75314d24615e2ad24f8874795999e0bcf31cbdcfeef8262ead

Corollary 2.2 requires a quadratic objective; the target permits all globally smooth convex objectives.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 5cc1b3b48e207f20b7586fca89602c41b5d9d99a9d847910bddd6dcbad1f76d2

Finite coefficient recovery identifies a quadratic, not an arbitrary smooth convex function.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 5b19ccced0984414c2ef620b78e79059471cc5801e63ab79d5f0466a68887f6d

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: b6807a4e38c811454c15d83d5d34d54e720d8ad16b5dc950adf50f1d6e6e6590

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration. Fresh revision addresses the preserved actual independent reviewer metadata issues with exact typed pending resource opportunities and honest closed/open publication bookkeeping. Unproved mappings remain pending, distinct IDs remain distinct, and no source guard or native inequality is broadened.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: a719ebda0f7dfc209ddda61cd44a8910d0443575a9b6c7ddffe8d34840b96666

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 76b79d0494fc995e4407609b1b0f32b3356a42d5e35bbe3dc1a2c819b259db85

SO_ZO_E03__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: 12b19b3ea5bfdcb615f3032fad2378489f623f29b7ae19c968fd7011adf2c018

SO_ZO_E03__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: 227d1d31afdd2a12fe37a590fed81e64f6f52546880671e1e4a386ec04c5e6b3

SO_ZO_E03__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/impact/3/comparison_ids/4; canonical SHA-256: 86afe548392f2a0adbd98399d9e7405f732fef457ca3bafd924a84e549dc6c85

SO_ZO_E03__deterministic__c5

#### Native item 6

Native pointer: /joint_analysis/impact/3/comparison_ids/5; canonical SHA-256: 700e3e7f14852da0d2d74c023842061de90daeed23df99c1191130feab77b6dc

SO_ZO_E03__randomized__c1

#### Native item 7

Native pointer: /joint_analysis/impact/3/comparison_ids/6; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native item 8

Native pointer: /joint_analysis/impact/3/comparison_ids/7; canonical SHA-256: 3fdb6ec272a97b5caf48ac717a76436c472ecf6ea23dac40e6b71a0f4e40bc2a

SO_ZO_E03__randomized__c3

#### Native item 9

Native pointer: /joint_analysis/impact/3/comparison_ids/8; canonical SHA-256: 2a04790fa2df16ccf10b9c03083b5c13ac10139b14919c22ab3c30a68ff3f432

SO_ZO_E03__randomized__c4

#### Native item 10

Native pointer: /joint_analysis/impact/3/comparison_ids/9; canonical SHA-256: 041f5b5649f4314047eec02f84b36191fe9a6c71fc2ffd98e0933aca3d2e1008

SO_ZO_E03__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 4d09b4c55f39fcfb74d4f3c63f9ada6184e70f957b20b151a5403aa8b6ac6b1a

curated_feedback_SO_ZO_E03_20261116_32450a04eb

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 0793dbdc8682f8e079d0d0fa71e97806343c26bbc8d7b8d3e24c673347862b40

d is an integer >=1; beta>0, R>0, epsilon>0; Q=beta R^2/epsilon>0. The separate deterministic and randomized g1 minimax quantities count exact scalar values under fixed worst-case budgets, with global convex beta-smooth objectives, a minimizer in B_2(0,R), and unrestricted ambient queries/output. All four independent native parameters vary; rescaling expresses their dependence through d,Q.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 64e80c2619100aecaf4c6cac46f36c8ac4a010398191c58e44532ee99f19dd0f

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 1041c48675eddf33b1cef6b3f0fdeab15223560134a9a48bc761f9b29aaf6d90

Assess the guarded deterministic q2 b3 to q1 c2 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 57d6a6917647c4a0bd9c79d6041628295dcf96035a1d5fff5bb44188e027e05e

Assess the guarded deterministic q2 b11 to q1 c4 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: c11fd1eff34091f02efdf7a38db5e5e82ca2ea29d573086b9e3d9cadac17b9b0

Assess the guarded randomized q2 b3 to q1 c2 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 917f50159faab02132a4bc759969d10b38569d9451fd561b68cb88aa7752dd64

Assess the guarded randomized q2 b9 to q1 c4 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 64e62c121834676415408235ac307441939d36a50104b13e3dba21c22a288125

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: e37d4a58045c843cb02e62a1ff2424479989a36be6a946015c473b2a0912321e

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: d5788d3e4b274df07a842900dc1ced593125fa89de56bcd6814a995345d9c0b1

Frozen baseline /bounds/0

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: f35fc1eef51fd1a12c4633256565a3296e639b1fa547aed8e32c477ccb6883a7

(32<=Q<=d^2) OR (Q>=32,Q>d^2)

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: b493b7be0702dfdb157b627d947776b437795d416d204a46f71cfd51535ae71e

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 3445f36961c203c3b3a063da16f6a6552203d4c4807786913e7787cb1d34f1db

Frozen baseline /bounds/1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: f35fc1eef51fd1a12c4633256565a3296e639b1fa547aed8e32c477ccb6883a7

(32<=Q<=d^2) OR (Q>=32,Q>d^2)

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: c99c36d95cf385ac91a1cab988e11fa151f634ed332328f83b5c384406a52cdc

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: cf1d752dc93674714e736ee1b8f78c46284d25600955f3d01c964f6b708da39e

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 3a2ef0aeaa4f47239ccb28dd8a94f200e515fe07535c686da41e9872e8cb594e

ZO_PROOF_ENDPOINT_EXTENSION

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: ff24070aa2e0b027ccc78d3253833ca15a8e29b201813da6458749217388051b

Frozen baseline /bounds/3

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 88ab4d5cf8b55d9dfd9f4a1c0f18fc929f583d3a76bed57bfd2edf4aa8483862

(4<=Q<32)

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: e8bbc06c8d546e84e000b80f9457df41251414cde6b62a11ad526f5ce3b3ce45

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: cf1d752dc93674714e736ee1b8f78c46284d25600955f3d01c964f6b708da39e

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: 3a2ef0aeaa4f47239ccb28dd8a94f200e515fe07535c686da41e9872e8cb594e

ZO_PROOF_ENDPOINT_EXTENSION

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 673bd4f36c8762405633c052ced116befc48f5c7060b568e27cf94b3be6fd72d

Frozen baseline /bounds/4

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/3/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 88ab4d5cf8b55d9dfd9f4a1c0f18fc929f583d3a76bed57bfd2edf4aa8483862

(4<=Q<32)

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 1548d78ed4c939f7c99920562dfcd23bcf9ea5a657b63eaac8161b2eba928252

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: e6fec3f7796e10d8ba70af3b1071bff78a3b8434f5317fb6e3fb2df5c9ef8f6d

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: e30a144145cb8fed16a0c5ffe3378c144c420bcb95d991d80d22b9669950b9b5

Frozen baseline /bounds/5

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/4/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 2913205f04674b69177abbf6d06b8750aa6c6f59e40e06541825d40c679fd5aa

(Q>=32,Q>d^2 AND Q>=128^2)

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: da0d2cbb3614e63866933e1f5cb3319be97a7769e7fdf056915595dfe59f2a22

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: 30adff92f80941ad5172aad12f005642cb34f9b7781fc3f700ecce8d67e790a8

Frozen baseline /bounds/6

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 0617de4b4eccd0abddb890c50e1e57ebe927c07f3f633dbb4a2961568b62cbdb

(Q<=2)

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: 8079015076abc2fa607f5463d37501393f4f21d9a56986ecca989ecdc53d40aa

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: 6ee00f1cc613ab2fd13f8590c4e34f8a934dcf759cd1deb1157125366fa470ff

Frozen baseline /bounds/7

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 0617de4b4eccd0abddb890c50e1e57ebe927c07f3f633dbb4a2961568b62cbdb

(Q<=2)

#### Native item 8

Native pointer: /joint_analysis/provenance/7; canonical SHA-256: 63fd1ac882807d00d49d717ad6918bebd3c700e309fd98b8c103e319cce464ac

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/7/bound_id; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: mapping

Native pointer: /joint_analysis/provenance/7/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/7/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/7/proof_refs; canonical SHA-256: a7a3fc655588cd4b894c69b7420479caed78513f7dd6d4681562c51ab6fe8700

#### Native item 1

Native pointer: /joint_analysis/provenance/7/proof_refs/0; canonical SHA-256: 4f452d8ed97f47aa7c2654ceb7664669c9a18956dbc24e82de952de25319fbab

ZO_PROOF_SMOOTH_ENDPOINT

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/7/source_domain; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/7/source_locator; canonical SHA-256: 32aec6c25ba11e523e32b5eb9090df44be01114fc9e0a4b37cbc25b6ba4b29bc

Frozen baseline /bounds/8

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/7/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/7/target_domain; canonical SHA-256: 824fb7a8c0c7e02d6b4b8ebbd99d474a3898feecaeb7174933b84ab714987686

(2<Q<4)

#### Native item 9

Native pointer: /joint_analysis/provenance/8; canonical SHA-256: e2e92861fab2f8fa290f461d9c21bfc8e1d0fa6cf57ef1ace8e539f9089d4993

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/8/bound_id; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native field: mapping

Native pointer: /joint_analysis/provenance/8/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/8/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/8/proof_refs; canonical SHA-256: a7a3fc655588cd4b894c69b7420479caed78513f7dd6d4681562c51ab6fe8700

#### Native item 1

Native pointer: /joint_analysis/provenance/8/proof_refs/0; canonical SHA-256: 4f452d8ed97f47aa7c2654ceb7664669c9a18956dbc24e82de952de25319fbab

ZO_PROOF_SMOOTH_ENDPOINT

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/8/source_domain; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/8/source_locator; canonical SHA-256: b0436e4e6aad21111b8da5f4a00cbc0917ccb3bfd0e61da9669d1b51e004a182

Frozen baseline /bounds/9

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/8/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/8/target_domain; canonical SHA-256: 824fb7a8c0c7e02d6b4b8ebbd99d474a3898feecaeb7174933b84ab714987686

(2<Q<4)

#### Native item 10

Native pointer: /joint_analysis/provenance/9; canonical SHA-256: 0b2aa887e7ffc19f750345599e62cf2662b36f54a0eeba53c40b5efc449f1ed2

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/9/bound_id; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/9/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/9/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/9/source_domain; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/9/source_locator; canonical SHA-256: dcc83f0d773e7ff56dee228cca6d4bed24da8597141dabcd93c7b4629af8a69b

Frozen baseline /bounds/11

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/9/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/9/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/9/target_domain; canonical SHA-256: f35fc1eef51fd1a12c4633256565a3296e639b1fa547aed8e32c477ccb6883a7

(32<=Q<=d^2) OR (Q>=32,Q>d^2)

#### Native item 11

Native pointer: /joint_analysis/provenance/10; canonical SHA-256: 9987e953eb6a81d1548af024480dc6f4262c0c9405cfdd05928d97dfa13d0d17

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/10/bound_id; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/10/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/10/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/10/source_domain; canonical SHA-256: 2a27ea1ec94f4adbac03fcff9615a10bdc6fedec38c847a626ad13d7f911fe43

Q>=32

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/10/source_locator; canonical SHA-256: 5e6c6b892879d0db04e6541380b0f04b26c44450344650115954c7ffa11ae90d

Frozen baseline /bounds/12

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/10/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/10/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/10/target_domain; canonical SHA-256: f35fc1eef51fd1a12c4633256565a3296e639b1fa547aed8e32c477ccb6883a7

(32<=Q<=d^2) OR (Q>=32,Q>d^2)

#### Native item 12

Native pointer: /joint_analysis/provenance/11; canonical SHA-256: 14b64ed03de03498dab6739459bba2f1a50bbc00d6667fa2633286ce58863977

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/11/bound_id; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/11/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/11/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/11/proof_refs; canonical SHA-256: cf1d752dc93674714e736ee1b8f78c46284d25600955f3d01c964f6b708da39e

#### Native item 1

Native pointer: /joint_analysis/provenance/11/proof_refs/0; canonical SHA-256: 3a2ef0aeaa4f47239ccb28dd8a94f200e515fe07535c686da41e9872e8cb594e

ZO_PROOF_ENDPOINT_EXTENSION

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/11/source_domain; canonical SHA-256: 338097d56601b868712606be6f2cb51a653dee7869cd7b871b35952a5019c10a

Q>=3

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/11/source_locator; canonical SHA-256: 43d3e33816f37018e5dc34bf7d9629dc8adb83c4e8333b6276e3f38ff05bd7ed

Frozen baseline /bounds/14

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/11/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/11/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/11/target_domain; canonical SHA-256: 88ab4d5cf8b55d9dfd9f4a1c0f18fc929f583d3a76bed57bfd2edf4aa8483862

(4<=Q<32)

#### Native item 13

Native pointer: /joint_analysis/provenance/12; canonical SHA-256: 64258826818f5a1e9e91d5221a31eeba7e11b0686b7f78c705956148a9503eb2

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/12/bound_id; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/12/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/12/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/12/proof_refs; canonical SHA-256: cf1d752dc93674714e736ee1b8f78c46284d25600955f3d01c964f6b708da39e

#### Native item 1

Native pointer: /joint_analysis/provenance/12/proof_refs/0; canonical SHA-256: 3a2ef0aeaa4f47239ccb28dd8a94f200e515fe07535c686da41e9872e8cb594e

ZO_PROOF_ENDPOINT_EXTENSION

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/12/source_domain; canonical SHA-256: 8ce59571c6302c7279bda5c159b395a5de84926c8c1dd8a03fe1b14d49c02bb1

4<=Q<=128^2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/12/source_locator; canonical SHA-256: c5676162a2a5b26020029dc6f7741f5d508654d62a3432455788845f366bc6d2

Frozen baseline /bounds/15

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/12/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/12/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/12/target_domain; canonical SHA-256: 88ab4d5cf8b55d9dfd9f4a1c0f18fc929f583d3a76bed57bfd2edf4aa8483862

(4<=Q<32)

#### Native item 14

Native pointer: /joint_analysis/provenance/13; canonical SHA-256: abec08d908fe0453679f48b0c5feae24feeea204471c1fa93542a58240dbbeb9

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/13/bound_id; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/13/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/13/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/13/proof_refs; canonical SHA-256: e6fec3f7796e10d8ba70af3b1071bff78a3b8434f5317fb6e3fb2df5c9ef8f6d

#### Native item 1

Native pointer: /joint_analysis/provenance/13/proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/13/source_domain; canonical SHA-256: f9832528018cda478402dd08379ebf01f0d4717411417ff1637aa2adef11448c

Q>=128^2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/13/source_locator; canonical SHA-256: 7b9fab05f60d8978ebd1560f10c0601cdf9db79b43a4bd7f03af12d928abd31b

Frozen baseline /bounds/16

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/13/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/13/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/13/target_domain; canonical SHA-256: 2913205f04674b69177abbf6d06b8750aa6c6f59e40e06541825d40c679fd5aa

(Q>=32,Q>d^2 AND Q>=128^2)

#### Native item 15

Native pointer: /joint_analysis/provenance/14; canonical SHA-256: f9cc8db47d6cf1d38837f54904351543fd7e96ab6c91fa63f0e3443a8fa9e605

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/14/bound_id; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/14/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/14/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/14/proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/provenance/14/proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/14/source_domain; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/14/source_locator; canonical SHA-256: 85a50955051979ad49f14b7849f10575f758cea59277e892c932f4f938babc14

Frozen baseline /bounds/17

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/14/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/14/target_domain; canonical SHA-256: 0617de4b4eccd0abddb890c50e1e57ebe927c07f3f633dbb4a2961568b62cbdb

(Q<=2)

#### Native item 16

Native pointer: /joint_analysis/provenance/15; canonical SHA-256: ea7d18ae37bc787481caa798e479f8c23b2dd3b162bda796f7c4fbb4c239561b

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/15/bound_id; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: mapping

Native pointer: /joint_analysis/provenance/15/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/15/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/15/proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/provenance/15/proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/15/source_domain; canonical SHA-256: edc2515c5f87c2b837559112dc53e1021c3df9a4687c583abd3eb5194fa79157

0<Q<=2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/15/source_locator; canonical SHA-256: 5856a16152ddf133b008ba16cc8a7f3556a5de410650eb191c217f5660ed3d2c

Frozen baseline /bounds/18

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/15/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/15/target_domain; canonical SHA-256: 0617de4b4eccd0abddb890c50e1e57ebe927c07f3f633dbb4a2961568b62cbdb

(Q<=2)

#### Native item 17

Native pointer: /joint_analysis/provenance/16; canonical SHA-256: 33ea48d3cdd406b70f9526f2341d099ad3deb44d84ae7d31284cbc47f5c3b990

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/16/bound_id; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native field: mapping

Native pointer: /joint_analysis/provenance/16/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/16/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/16/proof_refs; canonical SHA-256: a7a3fc655588cd4b894c69b7420479caed78513f7dd6d4681562c51ab6fe8700

#### Native item 1

Native pointer: /joint_analysis/provenance/16/proof_refs/0; canonical SHA-256: 4f452d8ed97f47aa7c2654ceb7664669c9a18956dbc24e82de952de25319fbab

ZO_PROOF_SMOOTH_ENDPOINT

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/16/source_domain; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/16/source_locator; canonical SHA-256: 18c41e97fc14d545620c57a3da809669b28138868109fe2b7082851b297a9142

Frozen baseline /bounds/20

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/16/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/16/target_domain; canonical SHA-256: 824fb7a8c0c7e02d6b4b8ebbd99d474a3898feecaeb7174933b84ab714987686

(2<Q<4)

#### Native item 18

Native pointer: /joint_analysis/provenance/17; canonical SHA-256: 516f104e81cbee538c3037a64df850066d257be7ac0dbd5f05b4a8149d31f254

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/17/bound_id; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native field: mapping

Native pointer: /joint_analysis/provenance/17/mapping; canonical SHA-256: 4e4ce0d9dd6860ac6d6ef0e0338ad004c59f01f5b78ef9e1626e0248585ac887

Conditional identity retention; native evidence and applicability remain binding. No new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/17/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/17/proof_refs; canonical SHA-256: a7a3fc655588cd4b894c69b7420479caed78513f7dd6d4681562c51ab6fe8700

#### Native item 1

Native pointer: /joint_analysis/provenance/17/proof_refs/0; canonical SHA-256: 4f452d8ed97f47aa7c2654ceb7664669c9a18956dbc24e82de952de25319fbab

ZO_PROOF_SMOOTH_ENDPOINT

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/17/source_domain; canonical SHA-256: e89e96ef157750fe0677117d02d53bbf4e7f52c0194064e68310424ba6707474

2<Q<4

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/17/source_locator; canonical SHA-256: 7feaaeb20cceafe32b4e1cd6509066ece5805499285014277328b052db097331

Frozen baseline /bounds/21

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/17/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/17/target_domain; canonical SHA-256: 824fb7a8c0c7e02d6b4b8ebbd99d474a3898feecaeb7174933b84ab714987686

(2<Q<4)

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: f22cef252911eb07c13a8773b6fac2ee4dac047305b823e04cd9fea4711448da

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: a719ebda0f7dfc209ddda61cd44a8910d0443575a9b6c7ddffe8d34840b96666

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 76b79d0494fc995e4407609b1b0f32b3356a42d5e35bbe3dc1a2c819b259db85

SO_ZO_E03__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 12b19b3ea5bfdcb615f3032fad2378489f623f29b7ae19c968fd7011adf2c018

SO_ZO_E03__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 227d1d31afdd2a12fe37a590fed81e64f6f52546880671e1e4a386ec04c5e6b3

SO_ZO_E03__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: 86afe548392f2a0adbd98399d9e7405f732fef457ca3bafd924a84e549dc6c85

SO_ZO_E03__deterministic__c5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: 700e3e7f14852da0d2d74c023842061de90daeed23df99c1191130feab77b6dc

SO_ZO_E03__randomized__c1

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/6; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/7; canonical SHA-256: 3fdb6ec272a97b5caf48ac717a76436c472ecf6ea23dac40e6b71a0f4e40bc2a

SO_ZO_E03__randomized__c3

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/8; canonical SHA-256: 2a04790fa2df16ccf10b9c03083b5c13ac10139b14919c22ab3c30a68ff3f432

SO_ZO_E03__randomized__c4

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/9; canonical SHA-256: 041f5b5649f4314047eec02f84b36191fe9a6c71fc2ffd98e0933aca3d2e1008

SO_ZO_E03__randomized__c5

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: d4d3066227543deefb2bd165a10a4f8922532486377109007e37e62d29936c86

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: f44902418633a6a927c42d0e451b78fdca596b9167d496f6305c3031528c835c

No new blind literature search in this migration. Conditional retention of the exact preceding accepted analysis and its finite historical scope; all stated pending work remains pending.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 180bdb652bace3bcfb7fdf4b7941d1d77f74360543ebe2e7b01b72dcde8f8e0f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: fb606bb6746daef6e0cb800c3f9a48de439fbaddef092bfcfa236ba6ac0c8b38

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 83bf3226946ce72850b3e9a6687dfca5f96c72c1b9fcb7b1ec4c2b9279b9e333

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/4; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/5; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/6; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/7; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/8; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 15776aaab62394ec678be0f298832e9408d46655d78d6248b96d3758751e2f6b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 76b79d0494fc995e4407609b1b0f32b3356a42d5e35bbe3dc1a2c819b259db85

SO_ZO_E03__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: cbd717faae83a18dcd0984f69326879d0fe1418a4573e90441638e7d8eb23ec6

synthesis-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 70c3b3ec255caadf4b49839f8863d062db1547a2b4b3bb73ae34633ba3528025

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 83bf3226946ce72850b3e9a6687dfca5f96c72c1b9fcb7b1ec4c2b9279b9e333

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/4; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/5; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/6; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/7; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/8; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 9bf3f8e150c0abe48d28626ae40988428b05463a4a5a66ce177e19ead5aa40b8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: ebcba919e62a1ab3932a5511960ae541204ef3e4e612a3e2b58eaa7aea342c2d

synthesis-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 7aa4470c2ba8fd97f5a08c0f0fb8be54085849ad592f1eb173d67ff43d9e905a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 83bf3226946ce72850b3e9a6687dfca5f96c72c1b9fcb7b1ec4c2b9279b9e333

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/5; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/6; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/7; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/8; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 403552b0d6af73b23ab9bc6a3603f34c6e9879aaf3077b6154462991a8a68bc8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 12b19b3ea5bfdcb615f3032fad2378489f623f29b7ae19c968fd7011adf2c018

SO_ZO_E03__deterministic__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 94ebdcb021bcbc6fc94fa708c1e7a7f9d1afd6248b96e70935fa7df176e425ff

synthesis-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: a20a5ab4b859005edfa640e8848315a4ad1e809790b5813d0cd50aed2be6f702

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 83bf3226946ce72850b3e9a6687dfca5f96c72c1b9fcb7b1ec4c2b9279b9e333

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/3; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/4; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/5; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/6; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/7; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/8; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 7bbcd82dd95f444c9c486c8487b21d27111412a0edc3253a5c4e35092d205fe2

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 227d1d31afdd2a12fe37a590fed81e64f6f52546880671e1e4a386ec04c5e6b3

SO_ZO_E03__deterministic__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 7f1a6540bd14dbb3bcfdfdfac9a64bfde09607556bb3c904bfc43adedf6ede22

synthesis-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 845e7d9a51f323644d504f171f6d77dcaff5cd3ccd6a211e737e5b128578499b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 83bf3226946ce72850b3e9a6687dfca5f96c72c1b9fcb7b1ec4c2b9279b9e333

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: c72869c774f4e39844b69c16e03bb7ea046e408ddb0f6fcf6077d2dd8bca6e2f

SO_ZO_E03__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: 7738d094b1280da576643ca3286600d8d8e51eab65bc31226756ce5bff70139a

SO_ZO_E03__deterministic__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: 193525ef95fb99c47b9041265d61d52c0b5c0980fcc3bbd903895ab8aa9dcb0d

SO_ZO_E03__deterministic__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/3; canonical SHA-256: 85ece774969860e2da6d65916b3b1a5550f3f3f4a2d00599986a0babd63c3f17

SO_ZO_E03__deterministic__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/4; canonical SHA-256: 69dcd82ea0d647f723601ad8a176457232093cbb37108964bd560af015baf6e5

SO_ZO_E03__deterministic__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/5; canonical SHA-256: 153aa7ee6ac9e75fa9a2ccf051224ec53f1133a1ce448706afe8570d41481fab

SO_ZO_E03__deterministic__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/6; canonical SHA-256: aac4ed6446b1f75308b7861bf563e3053a6d604f67fe50b8390e0cd823ddba0f

SO_ZO_E03__deterministic__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/7; canonical SHA-256: 99886926a42663c1e195f5f4e921a4f262e5ea46a5973640592cc5144e51db54

SO_ZO_E03__deterministic__b8

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/8; canonical SHA-256: a739e67d21af1e4fa7a0808eb861b127d580f2e2b821e4eebf573f1f486043f1

SO_ZO_E03__deterministic__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: e6f9376e91f6a811281593720fd6b70da0483e9fff721e8352c58a0817d955f1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 86afe548392f2a0adbd98399d9e7405f732fef457ca3bafd924a84e549dc6c85

SO_ZO_E03__deterministic__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: ca0bbdf769e92b6ee0fc04da5960cb413f34af9e8cc0d5eca08f2ac29f71ac8f

synthesis-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: a23cd3c8ab007c01816804ca9ca07fb6b6a36ceed9ddce5931d535aaeb757bd3

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 61eb4d64f8325c9db29b5dc28cb1e065df8355e3e8034bcc1f911cabda1068e4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/0; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/1; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/2; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/3; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/4; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/5; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/6; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/7; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/8; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 83c8302746ca26440e99b6f11d7b7db4deba0d45f5c7deed2402e0b80e91242d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 700e3e7f14852da0d2d74c023842061de90daeed23df99c1191130feab77b6dc

SO_ZO_E03__randomized__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 8cedb7c54fb7a3ff1b2d98263a56263d1a8afbb4fdabf8cee435054dc16d1ea3

synthesis-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: ca36f14750f0e71120a775f5ec356cbb7f8191e88d7e74bd6728874289a8c435

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 61eb4d64f8325c9db29b5dc28cb1e065df8355e3e8034bcc1f911cabda1068e4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/0; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/1; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/2; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/3; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/4; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/5; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/6; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/7; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/8; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: cc69c66d9116458ab3b2fa9327ac44fec2fa33977903e170633d5f45a6f5d469

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 5fa33983f32a4c1027a92106c478a51fb23e76f63df8884a2a111e3319f68669

synthesis-6

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 4f8dada84fff6e7bf1a463921e452f4ff6a6e8153f4c8805f9e734670e1f7c81

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 61eb4d64f8325c9db29b5dc28cb1e065df8355e3e8034bcc1f911cabda1068e4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/0; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/1; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/2; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/3; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/4; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/5; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/6; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/7; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/8; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: d99b5964d476bda83e82f0fbfcf09694c03037c9c7c9f7e3dc7504f599af0e8a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 3fdb6ec272a97b5caf48ac717a76436c472ecf6ea23dac40e6b71a0f4e40bc2a

SO_ZO_E03__randomized__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: f1d7c1b829959acf5fd8b22ab6c75fdbf1b3810e2c3ef78a394693a9a0260546

synthesis-7

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: bdd10f567d1007c7984a049f406376c7ab63c447aedbf83068baf00880e5ca8f

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 61eb4d64f8325c9db29b5dc28cb1e065df8355e3e8034bcc1f911cabda1068e4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/0; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/1; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/2; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/3; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/4; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/5; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/6; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/7; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/8; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 354b14c3d533395364bb71fdd02bd2e5c9bbf6d4679742b05ab62382cd892efc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 2a04790fa2df16ccf10b9c03083b5c13ac10139b14919c22ab3c30a68ff3f432

SO_ZO_E03__randomized__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 705e1af290021b0ee8b6cac71ead9597d036f83961af1c252c90f4ed8047130f

synthesis-8

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 10e2e403046950eed676d1ceacb17d36ffd3d14e2566f2bd75b1341046e39555

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 61eb4d64f8325c9db29b5dc28cb1e065df8355e3e8034bcc1f911cabda1068e4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/0; canonical SHA-256: 03c5da3cccbf07c3b5aa8f60f8fdb2e775e1e11b96f79822e52da0484a9fae22

SO_ZO_E03__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/1; canonical SHA-256: 11a38f344fb6814954aae1108a35b8cb9ec54e3085f31c99b809738424c73979

SO_ZO_E03__randomized__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/2; canonical SHA-256: 149eadd7015e3f7886fb48661ab70fa7f9fc5631cf8a65cb2e5f8ab7e4d9484e

SO_ZO_E03__randomized__b11

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/3; canonical SHA-256: 88e7bb3e9cbd6bdec49eea7964187a7709d4b33de0382e66256e736952e1d8e2

SO_ZO_E03__randomized__b2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/4; canonical SHA-256: ec30eb7f6758a2f7e4d6a606770465d61ace3a3e466838c9f4dac1df2ec5b76d

SO_ZO_E03__randomized__b4

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/5; canonical SHA-256: 9ab746fe42383ea9d4260614622f47f848167be686995b9fae1139ab49ec5db3

SO_ZO_E03__randomized__b5

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/6; canonical SHA-256: 19e12fe3ddf416debf150b5452e6dff90840ebcad8dfc53141d0a5a48c75000c

SO_ZO_E03__randomized__b6

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/7; canonical SHA-256: f049653134479b59b06920269b136d0e1031a446296f57fe03275f9eafb392d9

SO_ZO_E03__randomized__b7

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/8; canonical SHA-256: c7254a975d4330a39ccb5bde0894d6a087d781945eadfee9a7b0f3d5ce93fefe

SO_ZO_E03__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: aa89db430b3575edb3e7b81d28ea6a076e2fdef8fea3c0c09f24a65d90244641

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 041f5b5649f4314047eec02f84b36191fe9a6c71fc2ffd98e0933aca3d2e1008

SO_ZO_E03__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: cefa876d80b27bbc26ecd952c430927d231047df60d2c399f9959d4307ecfd70

synthesis-9

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: 6e3c1cfd001f08f6337e1a9be0f6488ffdb7b432c972eee1f94535f8011185a3

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: da2d956ddfb8bdb380faae64361444b37bd61b1c18436d0e30adc4f96998362b

Typed native opportunity: source SO_ZO_E03__deterministic__b3 and target SO_ZO_E03__deterministic__c2. Preserve exact bound validity (Sufficiently small absolute normalized accuracy; a nonquadratic multiscale hard family.). The displayed dlogQ lower is source-small-normalized-accuracy/nonquadratic-multiscale only. The numeric activation threshold and every original source/query/output/success restriction must be resolved before it could enter high-accuracyc2; do not treat the printed asymptotic formula as globally valid. Compare any legal consequence with all currently adoptedq1 lowers, including their guard-dependent maximum. Fixed worst-path budgets, exact scalar-values at permitted ambient points and arbitrary-output semantics remain to be checked against the separate target ID. No unproved transfer is activated in a bracket, and no newprimarypaper research or theoremcertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: 9b273aefc5cbf94faaa62c78e282ecb337c8bf243d6885ce35c87403d8d1e766

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/0; canonical SHA-256: e0c57e0031fc1dd6017abfd3ed55ec94d32ffb1dfcd5f1add6fcd644f58a0b81

SO_ZO_E03__deterministic__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 86bb9a36f5dd20da983125973bc2cb723bb58f37b6d8680d91787a3a5960e285

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids/0; canonical SHA-256: cb510d625c8e21766aa14c700790484e0222e915b42fa3bdb02876da0d97f939

high_accuracy

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 9bf3f8e150c0abe48d28626ae40988428b05463a4a5a66ce177e19ead5aa40b8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 6a697feda8ba9c9d2fa42e01a43c895c5927b1d34f69282f00bdc445d01440d1

q2-deterministic-b3-to-c2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 1041c48675eddf33b1cef6b3f0fdeab15223560134a9a48bc761f9b29aaf6d90

Assess the guarded deterministic q2 b3 to q1 c2 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: f087a613013c100c7d1113d733d6ea2af252c9a3e0fb0506f3f3b8627c9e3e41

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: da2d956ddfb8bdb380faae64361444b37bd61b1c18436d0e30adc4f96998362b

Typed native opportunity: source SO_ZO_E03__deterministic__b3 and target SO_ZO_E03__deterministic__c2. Preserve exact bound validity (Sufficiently small absolute normalized accuracy; a nonquadratic multiscale hard family.). The displayed dlogQ lower is source-small-normalized-accuracy/nonquadratic-multiscale only. The numeric activation threshold and every original source/query/output/success restriction must be resolved before it could enter high-accuracyc2; do not treat the printed asymptotic formula as globally valid. Compare any legal consequence with all currently adoptedq1 lowers, including their guard-dependent maximum. Fixed worst-path budgets, exact scalar-values at permitted ambient points and arbitrary-output semantics remain to be checked against the separate target ID. No unproved transfer is activated in a bracket, and no newprimarypaper research or theoremcertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: 9b273aefc5cbf94faaa62c78e282ecb337c8bf243d6885ce35c87403d8d1e766

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs/0; canonical SHA-256: e0c57e0031fc1dd6017abfd3ed55ec94d32ffb1dfcd5f1add6fcd644f58a0b81

SO_ZO_E03__deterministic__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 86bb9a36f5dd20da983125973bc2cb723bb58f37b6d8680d91787a3a5960e285

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids/0; canonical SHA-256: cb510d625c8e21766aa14c700790484e0222e915b42fa3bdb02876da0d97f939

high_accuracy

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: 9bf3f8e150c0abe48d28626ae40988428b05463a4a5a66ce177e19ead5aa40b8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: 147e23182bee82fe98f77051656d64e7e91e4b9d4e4dfc1c46fed17803d4aa32

q2-deterministic-b3-to-c2-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: 1041c48675eddf33b1cef6b3f0fdeab15223560134a9a48bc761f9b29aaf6d90

Assess the guarded deterministic q2 b3 to q1 c2 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/obligations/12; canonical SHA-256: 1324e16be3cd68e5e682f65196734c6eca231a315c7b3931c19253bdb183b433

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/argument; canonical SHA-256: 63f0c68ede6938cacf4935d6af5e895fbce144db3f4a1eda25e59dccb86471c8

Typed native opportunity: source SO_ZO_E03__deterministic__b11 and target SO_ZO_E03__deterministic__c4. Preserve exact bound validity ($2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.). The source window is exactly2<Q<4, gamma=1-2/Q. The printed lower max{1,dgamma} is at most orderd there; the already-recordedq1 deterministic endpoint isThetad, so a legal transfer of that displayed order need not strengthen it. This order observation does not certify the missing q2/q1 map, source interpretation, or hidden-constant comparison; keep the route pending. Fixed worst-path budgets, exact scalar-values at permitted ambient points and arbitrary-output semantics remain to be checked against the separate target ID. No unproved transfer is activated in a bracket, and no newprimarypaper research or theoremcertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs; canonical SHA-256: 2836a9b7a84dfb480c76a528985ad1e3e3f01b6b2624ac82925f3b9cb8377739

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs/0; canonical SHA-256: 5f61fdd351cac6497f9fe5a532d9eb1451459c774b78d45f2e0ad9b07e4d600d

SO_ZO_E03__deterministic__b11

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids; canonical SHA-256: 4460884b08df0d3df026fcf51397d652c88a93f222363872fc24b17aeb43f419

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids/0; canonical SHA-256: a2883e3744bce5f6e5da05fb2ac7600586ea31c1d4a8e38c5bd4388b3679e825

endpoint

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids; canonical SHA-256: 7bbcd82dd95f444c9c486c8487b21d27111412a0edc3253a5c4e35092d205fe2

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/0; canonical SHA-256: 227d1d31afdd2a12fe37a590fed81e64f6f52546880671e1e4a386ec04c5e6b3

SO_ZO_E03__deterministic__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/id; canonical SHA-256: f2ab8f4191552af3aad8f4002e68a56377765aac3f91d56bc14cdb12c97c019a

q2-deterministic-b11-to-c4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/lead; canonical SHA-256: 57d6a6917647c4a0bd9c79d6041628295dcf96035a1d5fff5bb44188e027e05e

Assess the guarded deterministic q2 b11 to q1 c4 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 14

Native pointer: /joint_analysis/synthesis_coverage/obligations/13; canonical SHA-256: a8c2583ec9362b08e085540bcd5b6216299bf9c287807ac5e93ddeebb9d17479

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/argument; canonical SHA-256: 63f0c68ede6938cacf4935d6af5e895fbce144db3f4a1eda25e59dccb86471c8

Typed native opportunity: source SO_ZO_E03__deterministic__b11 and target SO_ZO_E03__deterministic__c4. Preserve exact bound validity ($2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.). The source window is exactly2<Q<4, gamma=1-2/Q. The printed lower max{1,dgamma} is at most orderd there; the already-recordedq1 deterministic endpoint isThetad, so a legal transfer of that displayed order need not strengthen it. This order observation does not certify the missing q2/q1 map, source interpretation, or hidden-constant comparison; keep the route pending. Fixed worst-path budgets, exact scalar-values at permitted ambient points and arbitrary-output semantics remain to be checked against the separate target ID. No unproved transfer is activated in a bracket, and no newprimarypaper research or theoremcertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs; canonical SHA-256: 2836a9b7a84dfb480c76a528985ad1e3e3f01b6b2624ac82925f3b9cb8377739

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/0; canonical SHA-256: 5f61fdd351cac6497f9fe5a532d9eb1451459c774b78d45f2e0ad9b07e4d600d

SO_ZO_E03__deterministic__b11

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids; canonical SHA-256: 4460884b08df0d3df026fcf51397d652c88a93f222363872fc24b17aeb43f419

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids/0; canonical SHA-256: a2883e3744bce5f6e5da05fb2ac7600586ea31c1d4a8e38c5bd4388b3679e825

endpoint

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids; canonical SHA-256: 7bbcd82dd95f444c9c486c8487b21d27111412a0edc3253a5c4e35092d205fe2

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/0; canonical SHA-256: 227d1d31afdd2a12fe37a590fed81e64f6f52546880671e1e4a386ec04c5e6b3

SO_ZO_E03__deterministic__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/id; canonical SHA-256: 611bd03f3e120e44c8154b9892c354fa54ebb0c307ab71b0c7f252a106bc0b7c

q2-deterministic-b11-to-c4-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/lead; canonical SHA-256: 57d6a6917647c4a0bd9c79d6041628295dcf96035a1d5fff5bb44188e027e05e

Assess the guarded deterministic q2 b11 to q1 c4 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 15

Native pointer: /joint_analysis/synthesis_coverage/obligations/14; canonical SHA-256: aaa2a7db23b12eea66db706d0f657d4317ac67ffca4f95ad0988684d5159d001

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/argument; canonical SHA-256: b37f36df68f39bf752bbf352498a5a999e89aa0eee3097e44b30b9cd85af5aa6

Typed native opportunity: source SO_ZO_E03__randomized__b3 and target SO_ZO_E03__randomized__c2. Preserve exact bound validity (Sufficiently small absolute normalized accuracy; a nonquadratic multiscale hard family.). The displayed dlogQ lower is source-small-normalized-accuracy/nonquadratic-multiscale only. The numeric activation threshold and every original source/query/output/success restriction must be resolved before it could enter high-accuracyc2; do not treat the printed asymptotic formula as globally valid. Compare any legal consequence with all currently adoptedq1 lowers, including their guard-dependent maximum. Fixed worst-path budgets, exact scalar-values at permitted ambient points and arbitrary-output semantics remain to be checked against the separate target ID. No unproved transfer is activated in a bracket, and no newprimarypaper research or theoremcertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs; canonical SHA-256: 1548ada6b515c79b93eecaeea1f7fda3edeea51c5ab0e872927c21b8472319ed

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs/0; canonical SHA-256: b84b613ad3c03b505e8e31509bbc57144d342bd584c07aa7faa8bcf0a3c51c94

SO_ZO_E03__randomized__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids; canonical SHA-256: 86bb9a36f5dd20da983125973bc2cb723bb58f37b6d8680d91787a3a5960e285

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids/0; canonical SHA-256: cb510d625c8e21766aa14c700790484e0222e915b42fa3bdb02876da0d97f939

high_accuracy

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids; canonical SHA-256: cc69c66d9116458ab3b2fa9327ac44fec2fa33977903e170633d5f45a6f5d469

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/0; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/id; canonical SHA-256: 1508973ebea1da8870776dce2fce859bef3cad96eb3974c20204765e3e5d5341

q2-randomized-b3-to-c2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/lead; canonical SHA-256: c11fd1eff34091f02efdf7a38db5e5e82ca2ea29d573086b9e3d9cadac17b9b0

Assess the guarded randomized q2 b3 to q1 c2 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 16

Native pointer: /joint_analysis/synthesis_coverage/obligations/15; canonical SHA-256: d45a4a888140c2b40d740c5e323889996284d3469702320a83fb3e2cf46651a8

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/argument; canonical SHA-256: b37f36df68f39bf752bbf352498a5a999e89aa0eee3097e44b30b9cd85af5aa6

Typed native opportunity: source SO_ZO_E03__randomized__b3 and target SO_ZO_E03__randomized__c2. Preserve exact bound validity (Sufficiently small absolute normalized accuracy; a nonquadratic multiscale hard family.). The displayed dlogQ lower is source-small-normalized-accuracy/nonquadratic-multiscale only. The numeric activation threshold and every original source/query/output/success restriction must be resolved before it could enter high-accuracyc2; do not treat the printed asymptotic formula as globally valid. Compare any legal consequence with all currently adoptedq1 lowers, including their guard-dependent maximum. Fixed worst-path budgets, exact scalar-values at permitted ambient points and arbitrary-output semantics remain to be checked against the separate target ID. No unproved transfer is activated in a bracket, and no newprimarypaper research or theoremcertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs; canonical SHA-256: 1548ada6b515c79b93eecaeea1f7fda3edeea51c5ab0e872927c21b8472319ed

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs/0; canonical SHA-256: b84b613ad3c03b505e8e31509bbc57144d342bd584c07aa7faa8bcf0a3c51c94

SO_ZO_E03__randomized__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids; canonical SHA-256: 86bb9a36f5dd20da983125973bc2cb723bb58f37b6d8680d91787a3a5960e285

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids/0; canonical SHA-256: cb510d625c8e21766aa14c700790484e0222e915b42fa3bdb02876da0d97f939

high_accuracy

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids; canonical SHA-256: cc69c66d9116458ab3b2fa9327ac44fec2fa33977903e170633d5f45a6f5d469

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/0; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/id; canonical SHA-256: 33a8eb3d5008ff361b6bc0aa0fafc08935066e3adc42caa147235f9f65ccbfa0

q2-randomized-b3-to-c2-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/lead; canonical SHA-256: c11fd1eff34091f02efdf7a38db5e5e82ca2ea29d573086b9e3d9cadac17b9b0

Assess the guarded randomized q2 b3 to q1 c2 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 17

Native pointer: /joint_analysis/synthesis_coverage/obligations/16; canonical SHA-256: 7a937e883ceac1f63b9761e636e5145243ee45ce201782e93737f9f35112dca6

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/argument; canonical SHA-256: dd13504079294cad63388d6d213b55d7e5a411c39e8d675a8c65cc2c2617bb7e

Typed native opportunity: source SO_ZO_E03__randomized__b9 and target SO_ZO_E03__randomized__c4. Preserve exact bound validity ($2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.). The source window is exactly2<Q<4. Its O(d) upper has to be mapped to the q1 randomized guarantee/resource before adoption; it cannot be silently identified with q1. The currently recordedq1 endpoint upper O(max{1,d(1-2/Q)}) is no larger in order on this window, so the displayed O(d) source row by itself establishes no stronger q1order. This is not a completed transfer proof. Fixed worst-path budgets, exact scalar-values at permitted ambient points and arbitrary-output semantics remain to be checked against the separate target ID. No unproved transfer is activated in a bracket, and no newprimarypaper research or theoremcertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs; canonical SHA-256: 9d2794b1a12ae3d4175bae8a6c07e24a8584ee975bd61a58550770e7301fc4e0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/0; canonical SHA-256: 8fca862a2a0727edfafbf86f742a9e7a47d5dc01e9a03c2866c847d61c03d600

SO_ZO_E03__randomized__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids; canonical SHA-256: 4460884b08df0d3df026fcf51397d652c88a93f222363872fc24b17aeb43f419

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids/0; canonical SHA-256: a2883e3744bce5f6e5da05fb2ac7600586ea31c1d4a8e38c5bd4388b3679e825

endpoint

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids; canonical SHA-256: 354b14c3d533395364bb71fdd02bd2e5c9bbf6d4679742b05ab62382cd892efc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/0; canonical SHA-256: 2a04790fa2df16ccf10b9c03083b5c13ac10139b14919c22ab3c30a68ff3f432

SO_ZO_E03__randomized__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/id; canonical SHA-256: e28a567366d05b7f9bf9519d5e8c36d7891662fd5ed849c4e9853bfc31359208

q2-randomized-b9-to-c4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/lead; canonical SHA-256: 917f50159faab02132a4bc759969d10b38569d9451fd561b68cb88aa7752dd64

Assess the guarded randomized q2 b9 to q1 c4 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 18

Native pointer: /joint_analysis/synthesis_coverage/obligations/17; canonical SHA-256: 33e7f7ec029c1d94df15d2afb367591ab2ef40cdad4fd98535528acc16c6b9a6

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/argument; canonical SHA-256: dd13504079294cad63388d6d213b55d7e5a411c39e8d675a8c65cc2c2617bb7e

Typed native opportunity: source SO_ZO_E03__randomized__b9 and target SO_ZO_E03__randomized__c4. Preserve exact bound validity ($2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.). The source window is exactly2<Q<4. Its O(d) upper has to be mapped to the q1 randomized guarantee/resource before adoption; it cannot be silently identified with q1. The currently recordedq1 endpoint upper O(max{1,d(1-2/Q)}) is no larger in order on this window, so the displayed O(d) source row by itself establishes no stronger q1order. This is not a completed transfer proof. Fixed worst-path budgets, exact scalar-values at permitted ambient points and arbitrary-output semantics remain to be checked against the separate target ID. No unproved transfer is activated in a bracket, and no newprimarypaper research or theoremcertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs; canonical SHA-256: 9d2794b1a12ae3d4175bae8a6c07e24a8584ee975bd61a58550770e7301fc4e0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/0; canonical SHA-256: 8fca862a2a0727edfafbf86f742a9e7a47d5dc01e9a03c2866c847d61c03d600

SO_ZO_E03__randomized__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/cell_ids; canonical SHA-256: 4460884b08df0d3df026fcf51397d652c88a93f222363872fc24b17aeb43f419

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/cell_ids/0; canonical SHA-256: a2883e3744bce5f6e5da05fb2ac7600586ea31c1d4a8e38c5bd4388b3679e825

endpoint

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids; canonical SHA-256: 354b14c3d533395364bb71fdd02bd2e5c9bbf6d4679742b05ab62382cd892efc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/0; canonical SHA-256: 2a04790fa2df16ccf10b9c03083b5c13ac10139b14919c22ab3c30a68ff3f432

SO_ZO_E03__randomized__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/id; canonical SHA-256: 09eb6116295e4e50859d41f3e69fa6ec4e745eb1d049ff02671f0d09ef270d43

q2-randomized-b9-to-c4-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/lead; canonical SHA-256: 917f50159faab02132a4bc759969d10b38569d9451fd561b68cb88aa7752dd64

Assess the guarded randomized q2 b9 to q1 c4 transfer/dominance before any adoption; no native quantity identity is assumed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 19

Native pointer: /joint_analysis/synthesis_coverage/obligations/18; canonical SHA-256: 731b77da13c6faa4dcfb5f98e34f814764ff0c087850c2e451dee4c32d397763

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids; canonical SHA-256: a719ebda0f7dfc209ddda61cd44a8910d0443575a9b6c7ddffe8d34840b96666

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/0; canonical SHA-256: 76b79d0494fc995e4407609b1b0f32b3356a42d5e35bbe3dc1a2c819b259db85

SO_ZO_E03__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/1; canonical SHA-256: f251ab43babd47c74c9dac4eb24ad62a2c6341ff166d99127c61616146fe212c

SO_ZO_E03__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/2; canonical SHA-256: 12b19b3ea5bfdcb615f3032fad2378489f623f29b7ae19c968fd7011adf2c018

SO_ZO_E03__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/3; canonical SHA-256: 227d1d31afdd2a12fe37a590fed81e64f6f52546880671e1e4a386ec04c5e6b3

SO_ZO_E03__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/4; canonical SHA-256: 86afe548392f2a0adbd98399d9e7405f732fef457ca3bafd924a84e549dc6c85

SO_ZO_E03__deterministic__c5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/5; canonical SHA-256: 700e3e7f14852da0d2d74c023842061de90daeed23df99c1191130feab77b6dc

SO_ZO_E03__randomized__c1

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/6; canonical SHA-256: dac29e720f253eae1b20717542c930eb81179e2759165c9a83ecde9830343198

SO_ZO_E03__randomized__c2

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/7; canonical SHA-256: 3fdb6ec272a97b5caf48ac717a76436c472ecf6ea23dac40e6b71a0f4e40bc2a

SO_ZO_E03__randomized__c3

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/8; canonical SHA-256: 2a04790fa2df16ccf10b9c03083b5c13ac10139b14919c22ab3c30a68ff3f432

SO_ZO_E03__randomized__c4

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/9; canonical SHA-256: 041f5b5649f4314047eec02f84b36191fe9a6c71fc2ffd98e0933aca3d2e1008

SO_ZO_E03__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/id; canonical SHA-256: 207dd0a5f023c1f5888c7ae4a7cdc7aad0c6377bba1f5662bc0f70f81b005b5a

curated-scope-limit-32450a04eb

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 77a376907adc478c3dbf436412d3dda86b120ae7df438c9f8152c61c021f64e7

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: d84419e2c49b554448ee9a1f2df3cdbaeaa46b29f6e3bdca005f96d33a20b57c

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 4b81cab280b1e31c2ea7afa9a416577b7c9c22795698d5d642e0394c36a90edd

/quantities/2

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 0793dbdc8682f8e079d0d0fa71e97806343c26bbc8d7b8d3e24c673347862b40

d is an integer >=1; beta>0, R>0, epsilon>0; Q=beta R^2/epsilon>0. The separate deterministic and randomized g1 minimax quantities count exact scalar values under fixed worst-case budgets, with global convex beta-smooth objectives, a minimizer in B_2(0,R), and unrestricted ambient queries/output. All four independent native parameters vary; rescaling expresses their dependence through d,Q.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 12b00fa64ad0c86430449fafb2af8442f51e2356339bc95e3ba910d57114d38a

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: a277390c82c95f6d279de1d41120192e77a6dc831821bacd4a5821773eeaaa3f

SO_ZO_E03_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 79aba9ce873a068ca379cddcaf2a9b05fff900dcaf56c207de8b9f362e4c8bfd

SO_ZO_E03_p_1c5476f952

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 3384f3fa67818e34ece42defbfd747d6f1f2d0ee7ca0bd376100764c7c4fa4b1

SO_ZO_E03_p_c5d2137706

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 0a057a1bbb192a566cf71424703e301bc3789cd001b6bd1ed1ebeeeb1ddd541b

SO_ZO_E03_p_5c322c6737

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 82974d7b69771b3096bbb9a033b354ad3c97d0f7ba7d0a601ea0765dd0af1144

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 0e452ae0abc2f263f36b992eb5f37fed68cb0c00197b1e1feb98b73032e2f8ff

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: cef91d19c1bc1b4f4bffbc662cef82031ea0fa93f1a4a4049ec8cfd287b8094f

Q=beta R^2/epsilon (native SO_ZO_E03_p_582414083f). The bijection x=R y, F(y)=f(R y)/(beta R^2) preserves scalar-value query counts, convexity, guarantees and global output/query domains, reduces smoothness and localization to 1, and gives tolerance 1/Q. Thus d and Q determine the primary joint rate.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: d8df699a4518be7d9e0ec1fd6c27bef15b78af181b7acc4bc458dbb10670e61e

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 79aba9ce873a068ca379cddcaf2a9b05fff900dcaf56c207de8b9f362e4c8bfd

SO_ZO_E03_p_1c5476f952

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 3384f3fa67818e34ece42defbfd747d6f1f2d0ee7ca0bd376100764c7c4fa4b1

SO_ZO_E03_p_c5d2137706

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/2; canonical SHA-256: 0a057a1bbb192a566cf71424703e301bc3789cd001b6bd1ed1ebeeeb1ddd541b

SO_ZO_E03_p_5c322c6737

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: da53dc5001ef1e872bd575bd38d9fafe75b9a13e995acdefe8bbd13f40e12829

Q

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1; canonical SHA-256: 4df8bdd6d64a959b5ebb639aa1167c728889bbd6710523e018c1da1ad0be354b

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/1/expression; canonical SHA-256: 575497546f8daa98e741d1a929076334bd7fa47ece77cf4c610ba1470c4211bd

gamma=1-2/Q (native SO_ZO_E03_p_c1d5aac69e); 0<gamma<1/2 on 2<Q<4.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs; canonical SHA-256: a39f13498a3b88a80a663d23168c05268319560007b89237a8c4b97957f2c2e1

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/0; canonical SHA-256: 5bb3f6c0db53ac228d53427bd890c731a30b0f3adc8b7d466527fe7eb2d092d0

SO_ZO_E03_p_582414083f

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/1/symbol; canonical SHA-256: ca44c452eb826c7bfd518fa436b4f73082548bd50cc5eb370e5acb75afb84554

gamma

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 68471940186fb8ec8af227a7f4feb4476a6c7d9739e54ab310f729e218829ab4

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: a277390c82c95f6d279de1d41120192e77a6dc831821bacd4a5821773eeaaa3f

SO_ZO_E03_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 79aba9ce873a068ca379cddcaf2a9b05fff900dcaf56c207de8b9f362e4c8bfd

SO_ZO_E03_p_1c5476f952

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 3384f3fa67818e34ece42defbfd747d6f1f2d0ee7ca0bd376100764c7c4fa4b1

SO_ZO_E03_p_c5d2137706

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 0a057a1bbb192a566cf71424703e301bc3789cd001b6bd1ed1ebeeeb1ddd541b

SO_ZO_E03_p_5c322c6737

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 5bb3f6c0db53ac228d53427bd890c731a30b0f3adc8b7d466527fe7eb2d092d0

SO_ZO_E03_p_582414083f

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: 73f1bb05459f181b122c5badea1bdde16ff6b6c9e73d78a56283bea2d28a0cd0

SO_ZO_E03_p_c1d5aac69e

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1
