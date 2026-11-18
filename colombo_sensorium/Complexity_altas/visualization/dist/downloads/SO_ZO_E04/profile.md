# Smooth strongly convex optimization with exact values

**Setting ID.** `SO_ZO_E04`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; smoothness: Lipschitz gradient; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

### Admissible model

$f:\mathbb{R}^d\to\mathbb{R}$ is differentiable and satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$ for every $x,y\in\mathbb{R}^d$.

Strong convexity is defined in the Euclidean norm: $f((1-t)x+ty)\le(1-t)f(x)+tf(y)-\frac{\mu}{2}t(1-t)\|x-y\|_2^2$ for $x,y$ and $t\in[0,1]$ in the domain.

A global minimizer $x_*\in B_2(0,R)$ exists; the localization ball does not restrict the function domain.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

The public inputs are $d$, $\beta$, $\mu$, $R$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

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

$\mu$: Public lower bound on the strong-convexity modulus **Domain:** $\mu>0$.

$R$: Localization radius for a global minimizer **Domain:** $R>0$.

$x_*\in B_2(0,R)$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$\kappa$: Ratio of the known smoothness and strong-convexity bounds **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu$

$Q$: Smoothness accuracy ratio **Domain:** $Q>0$.

$Q=\beta R^2/\varepsilon$

$\gamma$: Relative slack near the zero-call threshold **Domain:** $0<\gamma<1/2$ when $2<Q<4$.

$\gamma=1-2/Q$

$m$: Saturation scale in the strongly convex lower bound **Domain:** $m>0$.

$m=\min\{d,\sqrt\kappa,\sqrt Q\}$

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

### R1 - Parameter regime E04.R1

**Region.** $\kappa=1,\ Q\ge4$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B5, B19

$$
\Omega(d)
$$

**Upper bound.** B9, B23

$$
O(d)
$$

**Gap or comparison.** $O(1)$

### R2 - Parameter regime E04.R2

**Region.** $1<\kappa\le2,\ Q\ge128^2$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B4, B18

$$
\Omega(d[1+\log Q/\log((\kappa+1)/(\kappa-1))])
$$

**Upper bound.** B2, B16

$$
O(d[1+\log Q/\log((\kappa+1)/(\kappa-1))])
$$

**Gap or comparison.** $O(1)$

### R3 - Parameter regime E04.R3

**Region.** $\kappa>2,\ Q\ge128^2$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B8, B7

$$
\Omega\!\left(d\max\{\min(d,\sqrt\kappa,\sqrt Q),\log Q\}\right)
$$

**Upper bound.** B1

$$
O(d\min\{\sqrt Q,\sqrt\kappa[1+\log_+(Q/\kappa)],d\log Q\})
$$

**Gap or comparison.** $O(1+\log Q)$

### R4 - Parameter regime E04.NEW.zero_region

**Region.** $Q\le2$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B11, B25

$$
0
$$

**Upper bound.** B10, B24

$$
0
$$

### R5 - Parameter regime E04.NEW.endpoint

**Region.** $2<Q<4$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B13

$$
\Omega(d)
$$

**Upper bound.** B12

$$
O(d)
$$

**Gap or comparison.** $O(1)$

### R6 - Parameter regime E04.NEW.constant_bridge

**Region.** $4\le Q<128^2,\ \kappa>1$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B5, B19

$$
\Omega(d)
$$

**Upper bound.** B6, B20

$$
O(d)
$$

**Gap or comparison.** $O(1)$

### R7 - Parameter regime E04.R3

**Region.** $\kappa>2,\ Q\ge128^2$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B22, B21

$$
\Omega\!\left(d\max\{\min(d,\sqrt\kappa,\sqrt Q),\log Q\}\right)
$$

**Upper bound.** B15

$$
O(d\min\{\sqrt Q,\sqrt\kappa[1+\log_+(Q/\kappa)],d\log Q\})
$$

**Gap or comparison.** $O(1+\log Q)$

### R8 - Parameter regime E04.NEW.endpoint

**Region.** $2<Q<4$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B28

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Upper bound.** B27

$$
O(\max\{1,d(1-2/Q)\})
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Coordinate-difference acceleration, strongly convex restarts or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(d\min\{\sqrt Q,\sqrt\kappa[1+\log_+(Q/\kappa)],d\log Q\}\right)
$$

**Sources.** [2](https://arxiv.org/pdf/2609.18728v2) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** The principal accuracy window is $Q\ge32$. The internal localization radius in WSC26 can be enlarged by a constant factor to match this regime.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [2](https://arxiv.org/pdf/2609.18728v2) theorem: WSC26 Theorem 3.4; D26 Appendix C.2; pdf pages: 7; printed pages: 7

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: WSC26 Theorem 3.4; D26 Appendix C.2; pdf pages: 29; printed pages: 29

### B2 - Coordinate-difference acceleration, strongly convex restarts or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(d\left[1+\frac{\log Q}{\log((\kappa+1)/(\kappa-1))}\right]\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Most useful for $1<\kappa\le2$; interpret the endpoint $\kappa=1$ as $O(d)$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5 / Appendix E.6

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5 / Appendix E.6; pdf pages: 4; printed pages: 4

### B3 - Random quadratics and multiscale hard families under curvature constraints

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(d\max\{\min(d,\sqrt\kappa,\sqrt Q),\log Q\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** The unified expression applies to $\kappa\ge2$ and sufficiently small accuracy; it does not extend to $\kappa\downarrow1$.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4 + Theorem E.5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4 + Theorem E.5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4 + Theorem E.5; pdf pages: 4; printed pages: 4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4 + Theorem E.5; pdf pages: 35; printed pages: 35

### B4 - Random quadratics and multiscale hard families under curvature constraints

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(d\left[1+\frac{\log Q}{\log((\kappa+1)/(\kappa-1))}\right]\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $1\le\kappa\le2,\varepsilon\le \beta R^2/128^2$, with the endpoints interpreted by continuity.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5; pdf pages: 4; printed pages: 4

### B5 - Random quadratics and multiscale hard families under curvature constraints

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

**Local argument.** A2

### B6 - Coordinate-difference acceleration, strongly convex restarts or localization

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

**Local argument.** A2

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; pdf pages: 29; printed pages: 29

### B7 - Multiscale hard family for accuracy dependence

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\kappa\ge2,\ Q\ge128^2$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A3

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5; pdf pages: 4; printed pages: 4

### B8 - Random quadratics and multiscale hard families under curvature constraints

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt\kappa,\sqrt Q\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $1\le\kappa,\ Q\ge32$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4; pdf pages: 4; printed pages: 4

### B9 - Coordinate-difference acceleration, strongly convex restarts or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
d+1
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\kappa=1,\varepsilon>0$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem2.5 endpoint; pdf pages: 4; printed pages: 4

### B10 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A6

### B11 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A6

### B12 - Deterministic finite-difference descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

### B13 - Deterministic hard family with indistinguishable directions

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega(d)
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

### B14 - Lower bound for estimation of a random spherical center

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

### B15 - Coordinate-difference acceleration, strongly convex restarts or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(d\min\{\sqrt Q,\sqrt\kappa[1+\log_+(Q/\kappa)],d\log Q\}\right)
$$

**Sources.** [2](https://arxiv.org/pdf/2609.18728v2) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** The principal accuracy window is $Q\ge32$. The internal localization radius in WSC26 can be enlarged by a constant factor to match this regime.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [2](https://arxiv.org/pdf/2609.18728v2) theorem: WSC26 Theorem 3.4; D26 Appendix C.2; pdf pages: 7; printed pages: 7

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: WSC26 Theorem 3.4; D26 Appendix C.2; pdf pages: 29; printed pages: 29

### B16 - Coordinate-difference acceleration, strongly convex restarts or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(d\left[1+\frac{\log Q}{\log((\kappa+1)/(\kappa-1))}\right]\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Most useful for $1<\kappa\le2$; interpret the endpoint $\kappa=1$ as $O(d)$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5 / Appendix E.6

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5 / Appendix E.6; pdf pages: 4; printed pages: 4

### B17 - Random quadratics and multiscale hard families under curvature constraints

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(d\max\{\min(d,\sqrt\kappa,\sqrt Q),\log Q\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** The unified expression applies to $\kappa\ge2$ and sufficiently small accuracy; it does not extend to $\kappa\downarrow1$.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4 + Theorem E.5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4 + Theorem E.5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4 + Theorem E.5; pdf pages: 4; printed pages: 4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4 + Theorem E.5; pdf pages: 35; printed pages: 35

### B18 - Random quadratics and multiscale hard families under curvature constraints

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(d\left[1+\frac{\log Q}{\log((\kappa+1)/(\kappa-1))}\right]\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $1\le\kappa\le2,\varepsilon\le \beta R^2/128^2$, with the endpoints interpreted by continuity.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5; pdf pages: 4; printed pages: 4

### B19 - Random quadratics and multiscale hard families under curvature constraints

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

**Local argument.** A2

### B20 - Coordinate-difference acceleration, strongly convex restarts or localization

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

**Local argument.** A2

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; pdf pages: 29; printed pages: 29

### B21 - Multiscale hard family for accuracy dependence

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\kappa\ge2,\ Q\ge128^2$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A3

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5; pdf pages: 4; printed pages: 4

### B22 - Random quadratics and multiscale hard families under curvature constraints

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt\kappa,\sqrt Q\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $1\le\kappa,\ Q\ge32$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4; pdf pages: 4; printed pages: 4

### B23 - Coordinate-difference acceleration, strongly convex restarts or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
d+1
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\kappa=1,\varepsilon>0$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem2.5 endpoint; pdf pages: 4; printed pages: 4

### B24 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A6

### B25 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A6

### B26 - Deterministic finite-difference descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

### B27 - Randomized projection descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

### B28 - Lower bound for estimation of a random spherical center

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

## 5. Local arguments

### A1 - Smooth exact-value complexity just below the zero-query threshold

**Scope.** Global convexity and $\beta$-smoothness; a global minimizer in $B_2(R)$; unrestricted exact scalar queries and output; fixed worst-case budget; $2<Q=\beta R^2/\varepsilon<4$.

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

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A2 - Extending the endpoint bound to fixed accuracy windows

**Scope.** All model budgets are fixed while accuracy varies; exact unrestricted value access.

The endpoint lower bound at $Q=3$ yields $\Omega(d)$ for every $Q\ge3$. The deterministic finite-difference accelerated bound is $O(d)$ on every fixed numerical interval $4\le Q\le128^2$.

Solving to a smaller error also solves to any larger error, so minimax complexity is nondecreasing as $\varepsilon$ decreases. At $Q=3$, the endpoint lemma gives $\gamma=1/3$ and hence a uniform $\Omega(d)$ randomized lower bound. The deterministic accelerated upper bound $O(d\sqrt Q)$ is at most $128$ times its universal constant on the stated interval. The same upper bound applies to randomized algorithms. The endpoint hard family is already quadratic, so the lower statement transfers unchanged to the quadratic subclass; the quadratic upper follows by restriction of the smooth algorithm.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

### A3 - Explicit logarithmic lower bounds and class restrictions

**Scope.** The source theorem retains its unrestricted query/output domain, fixed query cap, and stated accuracy window.

For the smooth class, $Q\ge128^2$ gives $\Omega(d\log Q)$. This also holds in a public strongly convex class with $\kappa\ge2$. For a ball-restricted Lipschitz class, $A=LR/\varepsilon\ge6\cdot128^2$ gives $\Omega(d\log A)$.

Dorn et al., Theorem 2.5, gives
$$\frac{3d}{4000}\left[1+\frac{\log(\beta_hR_h^2/\varepsilon)}{\log((\beta_h+\mu_h)/(\beta_h-\mu_h))}\right]$$
when $\mu_h/\beta_h\in[1/2,1]$ and $\beta_hR_h^2/\varepsilon\ge128^2$. Choose $\mu_h=\beta_h/2$, so the denominator is $\log3$. A convex $\beta$-smooth class contains this subclass with $\beta_h=\beta$, $R_h=R$. A public lower curvature budget $\mu\le\beta/2$ also contains it, uniformly in the public condition number.

For the ball-restricted Lipschitz class choose $R_h=R/2$, $\beta_h=2L/(3R)$, and $\mu_h=\beta_h/2$. On $B_2(R)$, $\|\nabla f(x)\|\le\beta_h(\|x\|+\|x_*\|)\le L$, and the global minimizer remains inside the feasible ball. One source value simulates one restricted value. The stronger source oracle permits all such algorithms, and $Q_h=A/6$. The explicit window makes $\log(A/6)$ and $\log A$ uniformly comparable.

For a selected-component finite sum with all components equal to the same hard function, one component query is one source query. This transfer has cost one, not $n$. A logarithmic and a dimension-dependent lower bound may be maximized only where both respective windows hold.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

### A4 - The smooth strongly convex dimension lower and its finite-sum embedding

**Scope.** The declared public curvature budgets are lower/upper bounds, not a promise that the best curvature moduli equal them.

For $Q=\beta R^2/\varepsilon\ge32$, the cited theorem gives
$$\Omega\!\left(d\min\{d,\sqrt\kappa,\sqrt Q\}\right),\qquad\kappa=\beta/\mu\ge1.$$
For the merely convex class omit the condition-number truncation.

Dorn et al., Corollary 2.4, directly covers global smoothness, global strong convexity, a global minimizer in the public radius, unrestricted exact-value queries/output, and adaptive randomized algorithms. Its explicit dimension baseline is retained, including at $\kappa=1$. A deterministic algorithm is included in that lower algorithm class. For selected-component access, set every component equal to the same source hard function; each requested component value is one source value. When combined with an independent $nd$ or precision-log lower bound, retain the source window of each term and maximize only valid terms. No extra factor of $n$ or $d$ follows from this embedding.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

### A5 - Exact recovery at equal smoothness and strong convexity

**Scope.** Global $\mu$-strong convexity and $\beta$-smoothness with $\mu=\beta$; exact scalar values and unrestricted finite queries.

The objective is $f(x)=\beta\|x\|^2/2-b^\top x+c$. Values at $0,e_1,\ldots,e_d$ recover a minimizer in $d+1$ calls.

Strong monotonicity, Cauchy--Schwarz, and Lipschitz continuity of the gradient imply
$$\beta\|x-y\|^2\le\langle\nabla f(x)-\nabla f(y),x-y\rangle\le\|\nabla f(x)-\nabla f(y)\|\,\|x-y\|\le\beta\|x-y\|^2.$$
Equality throughout forces $\nabla f(x)-\nabla f(y)=\beta(x-y)$. Therefore $b_j=\beta/2+f(0)-f(e_j)$ and $x_*=b/\beta$. For a finite-sum average, each of these $d+1$ average values costs $n$ component values, giving $n(d+1)$ calls. A one-component specialization has $n=1$. Restricted query domains require an admissible nonzero coordinate scale in place of unit vectors.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A6 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] Wendao Wu et al.. Near-Optimal Exact-Value Zeroth-Order Complexity for Smooth Strongly Convex Optimization. arXiv:2609.18728v2, 2026.

https://arxiv.org/pdf/2609.18728v2
