# Smooth convex optimization with exact values

**Setting ID.** `SO_ZO_E03`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap. A separate deterministic regime keeps all queries and the output inside $B_2(0,R)$ and promises a unique minimizer in $B_2(0,R/2)$; its current bracket combines the 2609.18230 bounded upper with explicitly justified compatible lower and localization transfers.

**Status.** Logarithmic gap present

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Unique global minimizer in half radius ball; smoothness: Lipschitz gradient; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

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

#### Deterministic — queries and output in the ball

Deterministic total Borel adaptive query and output maps are allowed. Every query and terminal output must lie in $B_2(0,R)$. No linear-span, zero-respecting, finite-precision or computational-complexity restriction is imposed.

Exact-real arithmetic, storage, projection onto public balls and computation of centroids of known convex localization bodies are unpriced. Finite-difference steps are positive and finite. Every actual oracle response, including initialization and perturbations, is charged.

One deterministic algorithm, chosen from the public inputs $d,\beta,R,\varepsilon$, must return $\widehat x\in B_2(0,R)$ with $f(\widehat x)-f(x_*)\le\varepsilon$ for every function in the view-specific class.

The charged scalar-value count has a fixed worst-case cap on every history. Early stopping may be padded by queries at zero.

All queries and the output lie in B_2(0,R); the unique global minimizer lies in the closed half-radius ball B_2(0,R/2).

This is a separate regime of SO_ZO_E03. It does not change the unrestricted deterministic or randomized views.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$R$: Localization radius for a global minimizer **Domain:** $R>0$.

$x_*\in B_2(0,R)$; in bounded_query_deterministic, $R$ is the query/output radius and the unique minimizer satisfies $\|x_*\|_2\le R/2$.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$Q$: Smoothness accuracy ratio **Domain:** $Q>0$.

$Q=\beta R^2/\varepsilon$

$\gamma$: Relative slack near the zero-call threshold **Domain:** $0<\gamma<1/2$ when $2<Q<4$.

$\gamma=1-2/Q$

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $\mathbb R^d$ in the original full-space views; $B_2(0,R)$ in bounded_query_deterministic.

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

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity. These equalities describe the original full-space views. In bounded_query_deterministic the function/global-optimization domains remain $\mathbb R^d$, while queries and output are restricted to $B_2(0,R)$.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

$d_{0,\mathrm{W26}}$: Universal dimension threshold in Wu et al. Theorems 3.4–3.5 **Domain:** $d_{0,\mathrm{W26}}\in\mathbb N$.

An unspecified absolute proof constant; not a public model parameter.

$c_{\varepsilon,\mathrm{W26}}$: Universal accuracy-window constant for the retained source lower bound **Domain:** $0<c_{\varepsilon,\mathrm{W26}}\le1/128$.

Theorem 3.5 gives an unspecified positive universal constant. For comparisons here choose its minimum with $1/128$, a permissible restriction of the source window, not an asserted numerical value of the original constant.

$c_{\mathrm{W26}}$: Positive universal multiplicative constant in the source lower bound **Domain:** $c_{\mathrm{W26}}>0$.

Unspecified universal constant of Theorem 3.5.

$Q_{\mathrm{W26}}(d)$: Branch cutoff of the source lower bound, not the current envelope cutoff **Domain:** $Q_{\mathrm{W26}}(d)>0$.

$Q_{\mathrm{W26}}(d)=(d/\log(ed))^{2/3}$; equality belongs to both source branch statements, whose formulas coincide.

$Q_{\mathrm{src}}$: Normalized accuracy after setting the source localization radius to R/2 **Domain:** $Q_{\mathrm{src}}>0$.

$Q_{\mathrm{src}}=\beta(R/2)^2/\varepsilon=Q/4$.



$$
\begin{aligned}&N_{\mathrm{bq}}^*\end{aligned}
$$

: Deterministic bounded-query minimax value complexity **Domain:** 

$$
\begin{aligned}&N_{\mathrm{bq}}^*\in\mathbb N_0\cup\{+\infty\}\end{aligned}
$$

.

The quantity for view bounded_query_deterministic only: queries/output in $B_2(0,R)$, unique minimizer in $B_2(0,R/2)$.

$X_{\mathrm{bq}},C_{\mathrm{bq}}$: Allowed ball and inner working ball in the bounded-query view **Domain:** $C_{\mathrm{bq}}\subset X_{\mathrm{bq}}\subset\mathbb R^d$.

$X_{\mathrm{bq}}=B_2(0,R)$ and $C_{\mathrm{bq}}=B_2(0,R/2)$.

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

#### Q5 - target accuracy cost

**View.** Deterministic — queries and output in the ball

$$
\begin{aligned}&N_{\mathrm{bq}}^*(d,\beta,R,\varepsilon)=\inf\{T\in\mathbb N_0:\\[3pt]&\exists\mathcal A\text{ admissible in bounded\_query\_deterministic},\\[3pt]&\sup_{f\in\mathcal F_{\beta}(d,R)}[f(\widehat x)-f(x_*)]\le\varepsilon\}\end{aligned}
$$

**Definition.** one exact scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Only the new bounded-query deterministic contract is used. T is a fixed pathwise scalar-value cap; the function is global, but all queries and the output are in B_2(0,R), with a unique global minimizer in B_2(0,R/2). No identification with the two existing full-space quantities is implicit.

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

### R8 - Ball-restricted queries/output: zero calls

**Region.** $0<Q\le8$.

**Views.** Deterministic — queries and output in the ball

**Quantity.** Q5

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B29

$$
0
$$

**Upper bound.** B28

$$
0
$$

### R9 - Ball-restricted queries/output: fixed coarse accuracy

**Region.** $8<Q<128$.

**Views.** Deterministic — queries and output in the ball

**Quantity.** Q5

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B30

$$
\Omega(d)
$$

**Upper bound.** B23

$$
O(d)
$$

**Gap or comparison.** $O(1)$

### R10 - Ball-restricted queries/output: current matching square-root regime

**Region.** $128\le Q\le4d^2$.

**Views.** Deterministic — queries and output in the ball

**Quantity.** Q5

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B25, B30

$$
\Omega(d\sqrt Q)
$$

**Upper bound.** B23

$$
O(d\sqrt Q)
$$

**Gap or comparison.** $O(1)$

### R11 - Ball-restricted queries/output: finite transition window

**Region.** $128\le Q<65536$ and $Q>4d^2$.

**Views.** Deterministic — queries and output in the ball

**Quantity.** Q5

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B25, B30

$$
\Omega(d^2)
$$

**Upper bound.** B23, B27

$$
O(d^2)
$$

**Gap or comparison.** $O(1)$; here $\log Q<\log65536$ is universally bounded.

### R12 - Ball-restricted queries/output: current high-accuracy envelope

**Region.** $Q\ge65536$ and $Q>4d^2$.

**Views.** Deterministic — queries and output in the ball

**Quantity.** Q5

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B25, B26, B30

$$
\Omega\!\left(d\max\{d,\log Q\}\right)
$$

**Upper bound.** B23, B27

$$
O\!\left(d\min\{\sqrt Q,d\log Q\}\right)
$$

**Gap or comparison.** $O\!\left(\dfrac{\min\{\sqrt Q,d\log Q\}}{\max\{d,\log Q\}}\right)\le O(\log Q)$; an upper bound on the remaining joint gap, not a lower bound on its size.

## 4. Bounds and supporting evidence

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A2

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A2

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A3

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A4

### B8 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $Q\le2$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A4

### B9 - Deterministic finite-difference descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A1

### B10 - Deterministic hard family with indistinguishable directions

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega(d)
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A1

### B11 - Lower bound for estimation of a random spherical center

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A1

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A2

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A2

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A3

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A4

### B19 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $Q\le2$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A4

### B20 - Deterministic finite-difference descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A1

### B21 - Randomized projection descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A1

### B22 - Lower bound for estimation of a random spherical center

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A1

### B23 - Bounded coordinate forward differences and projected acceleration

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic — queries and output in the ball

**Witness or lower-bound scope.** Deterministic witness

$$
(d+1)\lceil2\sqrt Q\rceil\le6d\sqrt Q
$$

**Sources.** [2](https://arxiv.org/abs/2609.18230v2)

**Conditions.** $d\ge1$, $Q\ge1$.; All forward-difference probes lie in $B_2(0,R)$ and the output lies in $B_2(0,R/2)$; uniqueness is part of the class.

**Oracle correspondence.** Exact scalar values, queried only in B_2(0,R). Any algorithm transfer must separately prove that every finite-difference probe is legal.

**Guarantee conversion.** One deterministic policy succeeds on every objective in the bounded view under a fixed pathwise cap. Stronger randomized source lower bounds cover this policy class by a constant random seed.

**Output rule.** The target output lies in B_2(0,R). The upper witnesses return points in B_2(0,R/2); lower source algorithms permit all target outputs.

**Resource conversion.** One target scalar value equals one source scalar value; each finite-difference location and queried center is charged.

**Source location.** [2](https://arxiv.org/abs/2609.18230v2) theorem: Definition 3.1, Definition 3.2, Theorem 3.3; Section 4 bounded-probe construction; pdf pages: 6; 7; 8; 9; 10; 11; 12; printed pages: 6; 7; 8; 9; 10; 11; 12

Official arXiv PDF returns v2 dated 19 October 2026. Statement, model and finite-difference query legality checked; full external proof not independently certified.

### B24 - Wu et al. exact-transcript lower bound

**Admission.** Eligible evidence; not selected in the displayed bracket

**Direction.** lower

**View.** Deterministic — queries and output in the ball

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c_{\mathrm{W26}}d\min\{\sqrt Q,(d/\log(ed))^{1/3}\}
$$

**Sources.** [2](https://arxiv.org/abs/2609.18230v2)

**Conditions.** $d\ge d_{0,\mathrm{W26}}$, $Q\ge1/c_{\varepsilon,\mathrm{W26}}$; the retained universal constant is chosen at most $1/128$.; The source hard function is globally smooth and has a unique minimizer in the half-radius ball. The source constants remain unspecified; the common window can be restricted by shrinking $c_{\varepsilon,\mathrm{W26}}$.

**Oracle correspondence.** Exact scalar values, queried only in B_2(0,R). Any algorithm transfer must separately prove that every finite-difference probe is legal.

**Guarantee conversion.** One deterministic policy succeeds on every objective in the bounded view under a fixed pathwise cap. Stronger randomized source lower bounds cover this policy class by a constant random seed.

**Output rule.** The target output lies in B_2(0,R). The upper witnesses return points in B_2(0,R/2); lower source algorithms permit all target outputs.

**Resource conversion.** One target scalar value equals one source scalar value; each finite-difference location and queried center is charged.

**Source location.** [2](https://arxiv.org/abs/2609.18230v2) theorem: Theorems 3.4–3.5; Corollaries 3.6–3.7; pdf pages: 7; 8; printed pages: 7; 8

The integer form requires $1\le m\le d/4$ and $m^3\log(ed)\le c_0d$; fewer than $dm/8$ calls leaves gap at least $2^{-17}\beta R^2/m^2$.

The hard family has strong-convexity modulus $\beta/(4096m^2)$; this is not an additional public target-class assumption.

The source matching window is $1/c_\varepsilon\le Q\le(d/\log(ed))^{2/3}$ at sufficiently large dimension. A smaller universal $c_\varepsilon\le1/128$ is used for comparison here. The source saturated branch is preserved but is not the current envelope.

The complete transcript/compiler lower-bound proof has not been independently verified.

### B25 - Half-radius positive-definite quadratic lower transfer

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic — queries and output in the ball

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\max\{5d/16,\,(d/4096)\min\{d,\sqrt Q/2\}\}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $d\ge1$, $Q\ge128$ (equivalently $Q_{\mathrm{src}}\ge32$).; Theorem 2.1 positive-definite quadratic family at source radius $R/2$; one target call is one source call.

**Oracle correspondence.** Exact scalar values, queried only in B_2(0,R). Any algorithm transfer must separately prove that every finite-difference probe is legal.

**Guarantee conversion.** One deterministic policy succeeds on every objective in the bounded view under a fixed pathwise cap. Stronger randomized source lower bounds cover this policy class by a constant random seed.

**Output rule.** The target output lies in B_2(0,R). The upper witnesses return points in B_2(0,R/2); lower source algorithms permit all target outputs.

**Resource conversion.** One target scalar value equals one source scalar value; each finite-difference location and queried center is charged.

**Local argument.** A6

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Section 2 oracle model; Theorem 2.1, especially the positive-definite quadratic hard-family statement; pdf pages: 2; 3; printed pages: 2; 3

Source class membership, uniqueness and the half-radius factor four checked.

The source model is unrestricted randomized with success at least 2/3; the target deterministic bounded policy is a permitted special case.

Official HTML https://arxiv.org/html/2610.00345v1 and author PDF https://borowiecki.dev/pdf/2610.00345 were consulted.

### B26 - Half-radius strongly convex hard-subclass lower transfer

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic — queries and output in the ball

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\frac{3d}{4000}\left[1+\frac{\log(Q/4)}{\log3}\right]
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $d\ge1$, $Q\ge4\cdot128^2=65536$ (equivalently $Q_{\mathrm{src}}\ge128^2$).; Use source $L=\beta$, $\mu=\beta/2$ and localization radius $R/2$; only the lower bound transfers to the target class.

**Oracle correspondence.** Exact scalar values, queried only in B_2(0,R). Any algorithm transfer must separately prove that every finite-difference probe is legal.

**Guarantee conversion.** One deterministic policy succeeds on every objective in the bounded view under a fixed pathwise cap. Stronger randomized source lower bounds cover this policy class by a constant random seed.

**Output rule.** The target output lies in B_2(0,R). The upper witnesses return points in B_2(0,R/2); lower source algorithms permit all target outputs.

**Resource conversion.** One target scalar value equals one source scalar value; each finite-difference location and queried center is charged.

**Local argument.** A6

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5, lower inequality, with mu=L/2; pdf pages: 4; printed pages: 4

Source normalization $Q_{\mathrm{src}}=Q/4$ yields the numerical activation condition $Q\ge65536$. The source strongly convex upper is not transferred.

### B27 - Interior-body finite-difference center-of-gravity localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic — queries and output in the ball

**Witness or lower-bound scope.** Deterministic witness

$$
(2d+1)\left[1+\left\lceil\frac{d\log Q}{-\log(1-1/e)}\right\rceil\right]=O(d^2\log Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $d\ge1$, $Q\ge128$ (equivalently $Q_{\mathrm{src}}\ge32$).; Centroids are in $B_2(0,R/2)$ and $h=\varepsilon/(\beta R\sqrt d)\le R/128$, so every central-difference probe remains in $B_2(0,R)$.

**Oracle correspondence.** Exact scalar values, queried only in B_2(0,R). Any algorithm transfer must separately prove that every finite-difference probe is legal.

**Guarantee conversion.** One deterministic policy succeeds on every objective in the bounded view under a fixed pathwise cap. Stronger randomized source lower bounds cover this policy class by a constant random seed.

**Output rule.** The target output lies in B_2(0,R). The upper witnesses return points in B_2(0,R/2); lower source algorithms permit all target outputs.

**Resource conversion.** One target scalar value equals one source scalar value; each finite-difference location and queried center is charged.

**Local argument.** A7

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2, finite-difference cutting-plane construction; pdf pages: 29; printed pages: 29

The concrete finite-difference and center-of-gravity algorithm was inspected. The proof record checks every target query and output, including the boundary of the inner ball.

### B28 - Return the center without oracle calls

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic — queries and output in the ball

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $0<Q\le8$.

**Oracle correspondence.** Exact scalar values, queried only in B_2(0,R). Any algorithm transfer must separately prove that every finite-difference probe is legal.

**Guarantee conversion.** One deterministic policy succeeds on every objective in the bounded view under a fixed pathwise cap. Stronger randomized source lower bounds cover this policy class by a constant random seed.

**Output rule.** The target output lies in B_2(0,R). The upper witnesses return points in B_2(0,R/2); lower source algorithms permit all target outputs.

**Resource conversion.** One target scalar value equals one source scalar value; each finite-difference location and queried center is charged.

**Local argument.** A5

### B29 - Call counts are nonnegative

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic — queries and output in the ball

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
0
$$

**Conditions.** $0<Q\le8$.

**Oracle correspondence.** Exact scalar values, queried only in B_2(0,R). Any algorithm transfer must separately prove that every finite-difference probe is legal.

**Guarantee conversion.** One deterministic policy succeeds on every objective in the bounded view under a fixed pathwise cap. Stronger randomized source lower bounds cover this policy class by a constant random seed.

**Output rule.** The target output lies in B_2(0,R). The upper witnesses return points in B_2(0,R/2); lower source algorithms permit all target outputs.

**Resource conversion.** One target scalar value equals one source scalar value; each finite-difference location and queried center is charged.

**Local argument.** A5

### B30 - Antipodal quadratic centers orthogonal to the query span

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic — queries and output in the ball

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
d
$$

**Conditions.** $Q>8$; deterministic algorithms only.

**Oracle correspondence.** Exact scalar values, queried only in B_2(0,R). Any algorithm transfer must separately prove that every finite-difference probe is legal.

**Guarantee conversion.** One deterministic policy succeeds on every objective in the bounded view under a fixed pathwise cap. Stronger randomized source lower bounds cover this policy class by a constant random seed.

**Output rule.** The target output lies in B_2(0,R). The upper witnesses return points in B_2(0,R/2); lower source algorithms permit all target outputs.

**Resource conversion.** One target scalar value equals one source scalar value; each finite-difference location and queried center is charged.

**Local argument.** A5

## 5. Local arguments

### A1 - Smooth exact-value complexity just below the zero-query threshold

**Scope.** Global convexity and $\beta$-smoothness; a global minimizer in $B_2(R)$; unrestricted exact scalar queries and output; fixed worst-case budget; $2<Q=\beta R^2/\varepsilon<4$.

Writing $\gamma=1-2/Q\in(0,1/2)$,


$$
T_{\mathrm{det}}=\Theta(d),\qquad T_{\mathrm{rand},2/3}=\Theta(\max\{1,d\gamma\}).
$$


The constants are uniform in $d,Q$, and in every declared strong-convexity lower budget $0<\mu\le\beta$.

Let $g=\nabla f(0)$. The convex function $h(x)=f(x)-\langle g,x\rangle$ is minimized at zero. A $1/\beta$ descent step for $h$ from a minimizer $x_*$ of $f$ gives


$$
f(0)-f_*\le R\|g\|-\|g\|^2/(2\beta).
$$


For a rank-$k$ orthogonal projector $P$, central differences in an orthonormal basis of its range yield $\widehat g=Pg+e$ with $e\in\operatorname{range}(P)$ and $\|e\|\le\beta h\sqrt{k}/2$. At $\widehat x=-\widehat g/\beta$, cancellation of the cross term in the smoothness inequality gives


$$
f(\widehat x)-f_*\le R\|g\|-\frac{\|g\|^2+\|Pg\|^2}{2\beta}+\frac{\|e\|^2}{2\beta}\le\frac{\beta R^2}{2(1+a)}+\frac{\|e\|^2}{2\beta},\quad a=\frac{\|Pg\|^2}{\|g\|^2}.
$$


The zero-gradient case satisfies the same error estimate.

For a Haar-uniform subspace choose $k=\min\{d,\max\{24,\lceil4d\gamma\rceil\}\}$. If $k<d$, then $\mathbb E a=k/d$ and $\operatorname{Var}(a)=2k(d-k)/(d^2(d+2))\le2k/d^2$. Thus $\Pr(a<k/(2d))\le8/k\le1/3$, and $k/(2d)\ge2\gamma$. For $k=d$, $a=1\ge2\gamma$ deterministically. Set


$$
m(\gamma)=(1-\gamma)-(1+2\gamma)^{-1}>0,\qquad h=R\sqrt{m(\gamma)/k}.
$$


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


$$
\frac{3d}{4000}\left[1+\frac{\log(\beta_hR_h^2/\varepsilon)}{\log((\beta_h+\mu_h)/(\beta_h-\mu_h))}\right]
$$


when $\mu_h/\beta_h\in[1/2,1]$ and $\beta_hR_h^2/\varepsilon\ge128^2$. Choose $\mu_h=\beta_h/2$, so the denominator is $\log3$. A convex $\beta$-smooth class contains this subclass with $\beta_h=\beta$, $R_h=R$. A public lower curvature budget $\mu\le\beta/2$ also contains it, uniformly in the public condition number.

For the ball-restricted Lipschitz class choose $R_h=R/2$, $\beta_h=2L/(3R)$, and $\mu_h=\beta_h/2$. On $B_2(R)$, $\|\nabla f(x)\|\le\beta_h(\|x\|+\|x_*\|)\le L$, and the global minimizer remains inside the feasible ball. One source value simulates one restricted value. The stronger source oracle permits all such algorithms, and $Q_h=A/6$. The explicit window makes $\log(A/6)$ and $\log A$ uniformly comparable.

For a selected-component finite sum with all components equal to the same hard function, one component query is one source query. This transfer has cost one, not $n$. A logarithmic and a dimension-dependent lower bound may be maximized only where both respective windows hold.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

### A4 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A5 - Bounded deterministic zero threshold and dimension floor

**Scope.** Only bounded\_query\_deterministic; $d\ge1$, $\beta,R,\varepsilon>0$.

Smoothness at the unique global minimizer gives $f(0)-f_*\le\beta\|x_*\|_2^2/2\le\beta R^2/8$. Thus output zero uses no calls when $Q\le8$; nonnegative cost proves exact zero.

For $Q>8$, suppose a deterministic procedure uses $T<d$ values. Answer its queries with $\beta(\|x\|_2^2+R^2/4)/2$. After the transcript is fixed choose a vector $v$ of length $R/2$ orthogonal to the span of every queried vector. The two fixed objectives $f_\pm(x)=\beta\|x\mp v\|_2^2/2$ produce exactly that transcript. Both are globally smooth, strictly convex, and have a unique allowed minimizer. For their common output $z$, the average of the two objective gaps is $\beta(\|z\|_2^2+R^2/4)/2\ge\beta R^2/8>\varepsilon$. One objective therefore defeats the procedure. This proves 

$$
\begin{aligned}&N_{\mathrm{bq}}^*\ge d\end{aligned}
$$

. Adaptivity is respected by completing the fixed pair after its common transcript is determined; every reply remains the value of both objectives. The argument also permits unrestricted queries/output, hence certainly applies to the restricted view.

**Limits of the argument.** An elementary local consequence, not a claim attributed to Theorem 3.5. Determinism is essential to this transcript argument.

### A6 - Half-radius transfer of unrestricted lower bounds to the bounded contract

**Scope.** Only bounded\_query\_deterministic; $Q\ge128$ for Theorem 2.1 and $Q\ge65536$ for Theorem 2.5.

Set the source smoothness $L=\beta$ and source localization radius $\rho=R/2$, so $Q_{\mathrm{src}}=\beta\rho^2/\varepsilon=Q/4$. Theorem 2.1 expressly supplies positive-definite quadratic hard instances. They have unique minimizers in $B_2(0,\rho)$ and therefore belong to the new view's class. Every restricted deterministic policy is also a policy allowed by the source's unrestricted randomized model (use a constant seed); deterministic success implies its success-probability requirement. One restricted value is one source value, with the same fixed cap, objective gap and output. Restricting algorithms cannot defeat the source lower bound. Its condition $\varepsilon\le\beta\rho^2/32$ becomes $Q\ge128$, and its formula becomes $\max\{5d/16,(d/4096)\min\{d,\sqrt Q/2\}\}$. The minimum changes branch at $Q=4d^2$.

For Theorem 2.5 take the source subclass with $\mu=\beta/2$ and the same $\rho$. Strong convexity supplies uniqueness; this subclass is contained in the target without imposing strong convexity on every target function. Its accuracy condition becomes $Q\ge4\cdot128^2=65536$. The lower bound is $(3d/4000)[1+\log(Q/4)/\log3]$. Both transfers are lower-bound transfers. Neither the quadratic recovery upper nor the strongly convex upper is inherited by the full smooth target.

**Limits of the argument.** Source theorem statements, hard-family inclusion and this reduction were checked. The complete source proofs were not independently re-proved.; The source radius must be halved. Omitting the factor four would incorrectly activate source bounds at Q=32 or Q=16384.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

### A7 - Legal ball-restricted realization of the finite-difference cutting-plane upper

**Scope.** Only bounded\_query\_deterministic; $Q\ge128$.

Use Appendix C.2 with $L=\beta$ and localization body $X_0=B_2(0,\rho)$, $\rho=R/2$. Choose $\Delta=\varepsilon/(4\rho)=\varepsilon/(2R)$ and central-difference step $h=2\Delta/(\beta\sqrt d)=\varepsilon/(\beta R\sqrt d)$. Each centroid $x_k$ stays in $B_2(0,R/2)$, and $h=R/(Q\sqrt d)\le R/128$; thus $x_k$ and all $x_k\pm he_i$ lie in the allowed ball. The finite-difference vector has norm error at most $\Delta$. The best queried centroid, including any early-stop point, also lies in the half-radius ball.

For completeness, the source volume argument remains valid with a minimizer on the boundary of the inner ball. Put $\alpha=\varepsilon/(4\beta\rho^2)=1/Q$; $X_\alpha=x_*+\alpha(X_0-x_*)$ lies inside $X_0$, has relative volume $\alpha^d$, and has gap at most $\varepsilon/2$. Each nonzero central cut through a centroid shrinks volume by at least the fixed factor $1-1/e$. If a point of $X_\alpha$ is cut off, convexity and the gradient approximation give gap at the cutting centroid at most $\varepsilon/2+2\rho\Delta=\varepsilon$. If the approximate gradient is zero, that centroid already has gap at most $2\rho\Delta$. Taking $K=1+\lceil d\log Q/[-\log(1-1/e)]\rceil$ ensures the required strict volume decrease. Each step costs $2d+1$ values, including its center. This gives the stated fixed bound and $O(d^2\log Q)$. Exact centroid computation is an allowed unpriced Borel operation on the public localization body; malformed histories can use a fixed zero-output convention.

**Limits of the argument.** The source center-of-gravity argument and its cited centroid-volume inequality remain external dependencies; this record verifies domain legality, cost and parameter substitution.; This is an explicit algorithm transfer, not an automatic implication from an unrestricted upper bound.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

### A8 - Guarded current envelope and disposition of the 2609.18230 source lower bound

**Scope.** Only the five new bounded\_query\_deterministic comparisons. All constants below are universal; d and Q vary jointly.

The direct bounded acceleration upper is at most $6d\sqrt Q$ for $Q\ge1$. Combining it with the deterministic floor $d$ gives $\Theta(d)$ on $8<Q<128$. For $128\le Q\le4d^2$, the half-radius quadratic lower selects $\sqrt Q/2$, hence the current rate is $\Theta(d\sqrt Q)$. For $128\le Q<65536$ and $Q>4d^2$, the quadratic lower is $\Omega(d^2)$, while the cutting-plane upper is $O(d^2\log Q)=O(d^2)$ with a uniform numerical factor bounded by $\log65536$; this finite transition cell has no asymptotic gap.

For $Q\ge65536$ and $Q>4d^2$, the compatible envelope is $L=\Omega(d\max\{d,\log Q\})$ and $U=O(d\min\{\sqrt Q,d\log Q\})$. The displayed ratio is only an upper bound on the unresolved gap, $O(\min\{\sqrt Q,d\log Q\}/\max\{d,\log Q\})$, in particular at most a logarithmic factor in $Q$. It need not diverge on every slice (for example, fixed d may give a constant ratio).

The source Theorem 3.5 has its own cutoff $(d/\log(ed))^{2/3}$ and unspecified absolute dimension/accuracy thresholds. We retain the original theorem formula and the two source branch regions, using a possibly smaller universal $c_{\varepsilon,\mathrm{W26}}\le1/128$ only to align the comparison windows. This does not assign the original constant a numerical value. Since $(d/\log(ed))^{1/3}\le d$ and $\sqrt Q=2(\sqrt Q/2)$, its lower-rate expression is at most twice $d\min\{d,\sqrt Q/2\}$ on the retained source window. It adds no larger asymptotic envelope than the transferred lower. It remains source evidence, not a selected current bracket and not a reason to place a current GAP at its earlier saturation cutoff. No numerical comparison of unspecified hidden constants is asserted.

**Limits of the argument.** This is the strongest envelope among the explicitly compared registered candidates, not a certification of exhaustive current literature.; Complete proofs of the external theorems were not independently verified.

**Sources.** [2](https://arxiv.org/abs/2609.18230v2) [1](https://arxiv.org/html/2610.00345v1)

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] Wendao Wu, Haihan Zhang, Chenheng Zhang, Yanyi Li, Chunyuan Zheng, Cong Fang, Haoxuan Li, Zhouchen Lin. Near-Optimal Deterministic Exact-Value Complexity for Smooth Convex Optimization. arXiv:2609.18230v2 (19 October 2026).

https://arxiv.org/abs/2609.18230v2
