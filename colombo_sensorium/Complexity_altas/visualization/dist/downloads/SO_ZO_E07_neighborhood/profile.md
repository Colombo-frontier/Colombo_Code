# Convex optimization with Hölder-continuous gradients and exact values

**Setting ID.** `SO_ZO_E07_neighborhood`

Single-objective optimization

Minimize $f$ globally over $B_2(0,R)$ and return a point with small objective gap.

**Status.** Polynomial gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Gradient holder; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; operation: Function value; feedback quality: Exact

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic algorithms; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $B_2(0,R)$ and return a point with small objective gap.

### Admissible model

$f$ is convex and continuously differentiable on an open neighborhood of $B_2(0,R+\tau)$, with $\tau>0$. For every $x,y$ in this neighborhood, $\|\nabla f(x)-\nabla f(y)\|_2\le H_\nu\|x-y\|_2^\nu$, where $0<\nu<1$.

Minimize over $B_2(0,R)$, allowing boundary optima. The neighborhood thickness is part of the query permission; a function defined in the ball is not automatically extended to the ambient space.

### Oracle interface

At any finite query point $x$ in $B_2(0,R+\tau)$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

Projection and the stated proximal operations over known geometry are free.

The public inputs are $d$, $\nu$, $H_\nu$, $R$, $\tau$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in B_2(0,R)$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in B_2(0,R)}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

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

$\nu$: Gradient Hölder exponent **Domain:** $0<\nu<1$.

$H_\nu$: Gradient Hölder modulus **Domain:** $H_\nu>0$.

$\|\nabla f(x)-\nabla f(y)\|_2\le H_\nu\|x-y\|_2^\nu$

$R$: Feasible-ball radius **Domain:** $R>0$.

The output must belong to $B_2(0,R)$; the query radius is specified separately in the interface.

$\tau$: Thickness of the queryable neighborhood outside the ball **Domain:** $\tau>0$.

The query domain is $B_2(0,R+\tau)$.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$W$: Accuracy ratio for Hölder-continuous gradients **Domain:** $W>0$.

$W=H_\nu R^{1+\nu}/\varepsilon$

$C_\nu$: Dimension or accuracy constant depending only on the fixed Hölder exponent **Domain:** $C_\nu>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$W_{0,\nu}$: Accuracy threshold depending only on the fixed Hölder exponent **Domain:** $W_{0,\nu}>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $B_2(0,R)$.

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

$f_*=\inf_{x\in B_2(0,R)}f(x)$.

$\nabla f,\nabla^2f,D^jf$: Gradient, Hessian, and higher Fréchet derivatives **Domain:** $\nabla f\in\mathbb{R}^d,\ \nabla^2f\in\mathbb{R}^{d\times d}$; $D^jf$ is a $j$-linear form.

Used only at derivative orders and on regions where the model guarantees its existence.

$\|\cdot\|_{\mathrm{op}}$: Euclidean induced matrix or tensor operator norm **Domain:** Take the supremum over Euclidean unit input vectors of the corresponding order.

$\|T\|_{\mathrm{op}}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|$

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=B_2(0,R)$ and $\mathcal{X}=B_2(0,R)$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

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

### R1 - Parameter regime E07.R1

**Region.** Fix $0<\nu<1$; require $W\ge W_{0,\nu}$, $d\ge\max\{8,C_\nu W^{8/(1+3\nu)}\log(eW)\}$ and $\tau>0$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Polynomial gap

**Lower bound.** B4, B9

$$
\Omega_\nu(\max\{d,W^{2/(1+3\nu)}\})
$$

**Upper bound.** B3

$$
O_\nu(d W^{2/(1+3\nu)})
$$

**Gap or comparison.** $O_\nu\!\left(\frac{dW^{2/(1+3\nu)}}{\max\{d,W^{2/(1+3\nu)}\}}\right)=O_\nu(\min\{d,W^{2/(1+3\nu)}\})$

### R2 - Parameter regime E07.R1

**Region.** Fix $0<\nu<1$; require $W\ge W_{0,\nu}$, $d\ge\max\{8,C_\nu W^{8/(1+3\nu)}\log(eW)\}$ and $\tau>0$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Polynomial gap

**Lower bound.** B8, B10

$$
\Omega_\nu(\max\{d,W^{2/(1+3\nu)}\})
$$

**Upper bound.** B7

$$
O_\nu(d W^{2/(1+3\nu)})
$$

**Gap or comparison.** $O_\nu\!\left(\frac{dW^{2/(1+3\nu)}}{\max\{d,W^{2/(1+3\nu)}\}}\right)=O_\nu(\min\{d,W^{2/(1+3\nu)}\})$

### R3 - Coarse-accuracy Theta_nu(d) closure

**Region.** Fix0<nu<1; d integer>=1; H_nu,R,tau,epsilon>0;0<W=H_nu R^(1+nu)/epsilon<=1.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B9

$$
\Omega(d)
$$

**Upper bound.** B3

$$
O_\nu(d)
$$

**Gap or comparison.** $Theta_nu(1)$

### R4 - Coarse-accuracy Theta_nu(d) closure

**Region.** Fix0<nu<1; d integer>=1; H_nu,R,tau,epsilon>0;0<W=H_nu R^(1+nu)/epsilon<=1.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B10

$$
\Omega(d)
$$

**Upper bound.** B7

$$
O_\nu(d)
$$

**Gap or comparison.** $Theta_nu(1)$

## 4. Bounds and supporting evidence

### B1 - Universal accelerated gradient method with finite differences

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O_\nu\!\left(d(H_\nu R^{1+\nu}/\varepsilon)^{2/(1+3\nu)}\right)
$$

**Sources.** [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf) [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf)

**Conditions.** $W=H_\nu R^{1+\nu}/\varepsilon\ge1$. This is a constructive upper bound, without a claim of zeroth-order optimality. The gradient approximation error is controlled by $h^\nu$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_HOLDER

**Source location.** [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf) theorem: Universal gradient method with finite-difference simulation

### B2 - Value-interface reduction of a randomized local-oracle lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_\nu((H_\nu R^{1+\nu}/\varepsilon)^{2/(1+3\nu)})
$$

**Sources.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf)

**Conditions.** Fix $0<\nu<1$ and take sufficiently small accuracy in the source's high-dimensional window. The lower bound holds first for a stronger local first-order interface, and therefore also for exact scalar-value algorithms.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_HOLDER

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 11; printed pages: 11; theorem: Theorem 12, $p=2$, specialized to one sequential query

### B3 - Universal accelerated gradient method with finite differences

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O_\nu(d[1+W^{2/(1+3\nu)}])
$$

**Sources.** [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf) [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf)

**Conditions.** $0<\nu<1,\ H_\nu,R,\tau,\varepsilon>0$

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_HOLDER

**Source location.** [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf) pdf pages: 12; printed pages: 11; theorem: Theorem 3, Eq.(4.3)

### B4 - Value-interface reduction of a randomized local-oracle lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_\nu(W^{2/(1+3\nu)})
$$

**Sources.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf)

**Conditions.** Fix $0<\nu<1$; require $W\ge W_{0,\nu}$ and $d\ge\max\{8,C_\nu W^{8/(1+3\nu)}\log(eW)\}$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_HOLDER

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 11; printed pages: 11; theorem: Theorem12

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 7; printed pages: 7; theorem: Theorem2 / Remark3

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 8; printed pages: 8; theorem: Radial shielding O1/O2

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 18; printed pages: 18; theorem: Lemma20 proof

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 25; printed pages: 25; theorem: Theorem12 proof

### B5 - Universal accelerated gradient method with finite differences

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O_\nu\!\left(d(H_\nu R^{1+\nu}/\varepsilon)^{2/(1+3\nu)}\right)
$$

**Sources.** [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf) [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf)

**Conditions.** $W=H_\nu R^{1+\nu}/\varepsilon\ge1$. This is a constructive upper bound, without a claim of zeroth-order optimality. The gradient approximation error is controlled by $h^\nu$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_HOLDER

**Source location.** [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf) theorem: Universal gradient method with finite-difference simulation

### B6 - Value-interface reduction of a randomized local-oracle lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_\nu((H_\nu R^{1+\nu}/\varepsilon)^{2/(1+3\nu)})
$$

**Sources.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf)

**Conditions.** Fix $0<\nu<1$ and take sufficiently small accuracy in the source's high-dimensional window. The lower bound holds first for a stronger local first-order interface, and therefore also for exact scalar-value algorithms.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_HOLDER

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 11; printed pages: 11; theorem: Theorem 12, $p=2$, specialized to one sequential query

### B7 - Universal accelerated gradient method with finite differences

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O_\nu(d[1+W^{2/(1+3\nu)}])
$$

**Sources.** [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf) [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf)

**Conditions.** $0<\nu<1,\ H_\nu,R,\tau,\varepsilon>0$

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_HOLDER

**Source location.** [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf) pdf pages: 12; printed pages: 11; theorem: Theorem 3, Eq.(4.3)

### B8 - Value-interface reduction of a randomized local-oracle lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_\nu(W^{2/(1+3\nu)})
$$

**Sources.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) [2](https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf)

**Conditions.** Fix $0<\nu<1$; require $W\ge W_{0,\nu}$ and $d\ge\max\{8,C_\nu W^{8/(1+3\nu)}\log(eW)\}$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_HOLDER

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 11; printed pages: 11; theorem: Theorem12

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 7; printed pages: 7; theorem: Theorem2 / Remark3

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 8; printed pages: 8; theorem: Radial shielding O1/O2

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 18; printed pages: 18; theorem: Lemma20 proof

**Source location.** [1](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) pdf pages: 25; printed pages: 25; theorem: Theorem12 proof

### B9 - Affine zero-transcript nullspace argument

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** Algorithm scope stated in the evidence below

$$
d+1
$$

**Conditions.** d is an integer >=1; 0<nu<1; H_nu,R,tau,epsilon>0; W=H_nu R^(1+nu)/epsilon.

**Oracle correspondence.** Globally affine subclass; a scalar value is one scalar linear observation, with the affine intercept included in the deterministic nullspace proof. All query locations remain within B_2(0,R+tau).

**Guarantee conversion.** Every deterministic measurable adaptive strategy with cap <=d fails on a fixed affine instance.

**Output rule.** Any output in B_2(0,R), including an unqueried point, is covered.

**Resource conversion.** Fixed worst-case cap on every path; all scalar values, including initialization, are counted.

**Local argument.** ZO_PROOF_AFFINE_DIMENSION

### B10 - Adaptive spherical linear-measurement argument

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** Algorithm scope stated in the evidence below

$$
\lceil d/9\rceil
$$

**Conditions.** d is an integer >=1; 0<nu<1; H_nu,R,tau,epsilon>0; W=H_nu R^(1+nu)/epsilon.

**Oracle correspondence.** Globally affine subclass; a scalar value is one scalar linear observation, with the affine intercept included in the deterministic nullspace proof. All query locations remain within B_2(0,R+tau).

**Guarantee conversion.** Every private-random measurable adaptive strategy with fixed cap k<d/9 fails the per-instance success requirement >=2/3 on some fixed affine instance.

**Output rule.** Any output in B_2(0,R), including an unqueried point, is covered.

**Resource conversion.** Fixed worst-case cap on every path; all scalar values, including initialization, are counted.

**Local argument.** ZO_PROOF_AFFINE_DIMENSION

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: e2aa05d80d106db03f59d1f4e82822cc462f2e322edf1871ef7068e3ca0b2213

### Native proof: ZO_PROOF_HOLDER

Native pointer: /proofs/0; canonical SHA-256: 8e9b2cccbdd9204cd27a869418c0a80b7c7d0eace21574f0af7378874d978538

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 00ba7b58f36c9acf20dbb9e3a7e5a040a85cc433dbfe67cc927a54201faaf59f

Writing $W=H_\nu R^{1+\nu}/\varepsilon$, an upper is $O_\nu(d[1+W^{2/(1+3\nu)}])$. A lower $\Omega_\nu(W^{2/(1+3\nu)})$ holds for $W\ge W_{0,\nu}$ and
$$d\ge\max\{8,C_\nu W^{8/(1+3\nu)}\log(eW)\}.$$

At any feasible point, forward differences with $0<h\le\tau$ satisfy $\|\widehat g-\nabla f(x)\|\le\sqrt dH_\nu h^\nu/(1+\nu)$. Thus $d+1$ exact values achieve any prescribed positive gradient error. On a set of diameter $2R$, shifting the reported function value downward by $2R\eta$ gives a valid lower first-order model. The upper model error is at most $4R\eta+H_\nu\|y-x\|^{1+\nu}/(1+\nu)$. Young's inequality bounds the latter by $M_\delta\|y-x\|^2/2+\delta/2$, where $M_\delta=C_\nu H_\nu^{2/(1+\nu)}\delta^{-(1-\nu)/(1+\nu)}$. Choose $\eta\le\delta/(8R)$. The universal inexact accelerated model bound is $O(M_\delta R^2/N^2+N\delta)$. Taking $\delta$ a small multiple of $\varepsilon/N$ and solving yields the stated iteration count, multiplied by $O(d)$ values. The additive one is needed because unrestricted affine terms remain legal even if $H_\nu$ is tiny.

For the lower use Diakonikolas and Guzman, Theorem 12, at norm $p=2$ and parallel batch size one. Its two terms scale as $W^{2/(1+3\nu)}$ and $dW^{-6/(1+3\nu)}/\log M$. Choose $M$ a small constant multiple of the first term. The displayed dimension makes the second no smaller than the first. The radial shielding in the source construction handles exterior queries, and its ball-contained witness preserves the constrained optimum comparison. If the target returns an unqueried feasible point, append one query there to meet the source's successful-query convention; the $W\ge W_{0,\nu}$ condition absorbs that one call. Scale coordinates by $R$ and values by $H_\nu R^{1+\nu}$. The source lower concerns a stronger local first-order oracle and so also limits exact-value algorithms, without acquiring an extra factor of $d$.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/0/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 310b39ff6c6a6f928f7f9e93758385a7daf89355592d0c00945697b60f96b721

Public buffer $\tau>0$; optimization/output in $B_2(R)$ and queries allowed in $B_2(R+\tau)$; fixed $0<\nu<1$ and gradient Hölder budget $H_\nu$.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 9266f6c8ee956db730f537ce9b1c422ac833f41d9444814fc82174651676a644

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 5446f485e7a1cd19c193ce23539918bf50e1b3028a573c3e589ccd63e4d5146e

SO_SRC_c39da60c875a03f8

#### Native item 2

Native pointer: /proofs/0/source_refs/1; canonical SHA-256: d71eaf50b02cec1af0acc335c696c3e23d237df6af6766c1d2eb519789aa8894

SO_SRC_8cf103dfaaf94469

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 0d60687e124153e6acaef0225d191cf96eecc861f6c458ceca8fa10399161ab7

Finite differences and a Hölder-gradient neighborhood

### Native proof: ZO_PROOF_AFFINE_DIMENSION

Native pointer: /proofs/1; canonical SHA-256: 1a78dbdfdf518f52d7668b082ee238bf202cb8300998880cf17d9cb640ae4f08

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: bf1bf3d88d54a714150ea6316d162fbf02e6ffd3a83bffdcd8b8885e7457215e

Retained premises, not historical recertification: /common_specification @ cb48cb4b4baea9df2c2680eec34eefd13baf4283f8883190d24fe490f128f366 supplies the Euclidean feasible/output ball of radius R, scalar exact-value oracle, fixed-path query cost, and the gradient seminorm inequality <=H_nu on the query neighborhood. /views @ 2f0a5ec56525ede164a1e741b632b782e6e1d6a60694e8420371420f75b33245 supplies arbitrary measurable adaptive deterministic algorithms and private-random algorithms with per-instance success >=2/3. /resource_projections/0 @ 51e8191c0794f51712b73e70c0665ecc79d2490f05e1d9dd0bc91c93dd6879de fixes one value per call. The q1 minimax quantities are /quantities/0 @ 8f04168525f60569d0129c9d52a55c82fcf0e8406645a6e3ddf554667b400cea and /quantities/2 @ 98a48d9e22187046a9e92061ea4f10395029a666bb1545cf6c39f1085961c6f5. No external theorem is used below.

I. Subclass and preservation. Every f(x)=a.x+b, with arbitrary a in R^d and b in R, is globally convex C1 and has gradient Holder seminorm zero, hence belongs for every permitted positive H_nu and every tau>0. Its constrained minimum is b-R||a||. Each permitted value is the single scalar a.q+b; neither an unqueried output nor free postprocessing yields an additional observation. The subclass retains the original query domain, output ball, guarantees and fixed path caps; it does not impose an affine promise on the target.

II. Exact deterministic lower. Suppose a deterministic algorithm has cap k<=d and run it on the admissible zero function. Let q_1,...,q_m, m<=k, be its actual queries and y its feasible output. If m>=1 the m homogeneous equations a.q_i+b=0 in d+1 unknowns admit a nonzero solution (a,b), necessarily with a!=0 because a=0 would force b=0. Choose sign sigma with sigma a.y>=0 and lambda>epsilon/(R||a||). The fixed instance f(x)=sigma lambda(a.x+b) reproduces every response and therefore the entire adaptive transcript and output. Its gap is lambda(sigma a.y+R||a||)>epsilon, a contradiction. If m=0 choose any nonzero a, choose its sign similarly, and scale; no response constraints are needed. Thus T_det>=d+1 exactly, including d=1.

III. Exact randomized lower. Let an algorithm have integer cap k. If k>=d, k>=d/9 is immediate; assume k<d. For each L>0 choose a uniformly on the radius-L sphere, independently of its private random tape, and consider f_a(x)=a.x. Fix the tape. Construct an augmented transcript with one new orthogonal linear measurement at each of k steps. Maintain the span of previous augmented directions. If the algorithm's next actual query q has a nonzero orthogonal component, measure along that component's unit direction and reconstruct a.q from that answer and the already measured projection. If q lies in the span its answer is already determined, so measure any measurably selected orthogonal unit direction instead. After the algorithm stops, pad to k steps in the same way. Each such unit-direction measurement can be obtained at (R+tau) times the direction and divided by R+tau, using one permitted scalar value. Only the reconstructed original answers are shown to the original algorithm. Its output Y is therefore measurable in the enlarged history. This construction also handles dependent queries and data-dependent stopping.

Conditional on the enlarged history after j measurements and the fixed tape, write a=p_j+z_j. Rotational symmetry shows inductively that z_j is uniform on the sphere of radius sqrt(L^2-||p_j||^2) in the (d-j)-dimensional orthogonal complement: a new predictable orthogonal direction fixes exactly its one coordinate and leaves a uniform orthogonal residual. Consequently E[a|history]=p_j and the next squared-coordinate conditional mean is (L^2-||p_j||^2)/(d-j). Starting at p_0=0, the recursion gives E||p_j||^2=jL^2/d. This proves the needed adaptive measurement statement directly, without an external information theorem.

Average also over the private tape. The gap Z=RL+a.Y lies in [0,2RL] and E Z=RL+E[p_k.Y]>=RL-R E||p_k||>=RL(1-sqrt(k/d)). Uniform per-instance success >=2/3, integrated over the sphere, gives Pr(Z<=epsilon)>=2/3. For 2RL>epsilon this implies E Z<=2epsilon/3+2RL/3. Hence sqrt(k/d)>=1/3-2epsilon/(3RL). The fixed algorithm must satisfy this for every L, since slopes have no magnitude bound. Letting L tend to infinity gives k>=d/9 and therefore T_rand>=ceil(d/9) exactly. The constructed instances are fixed before the random tape, so the adversarial-instance quantifier is preserved.

IV. Envelope and endpoints. Retain b3/b4 only on their existing contracts and guards: /bounds @ d65950486a96732b19558449b3ee25c31c49fc99c9517c50c71e028cf1aff836, /comparisons @ 6a65a84e8fa068c8ece09c60f2732e04941a530a00704f718a33a858fc633ab6, and ZO_PROOF_HOLDER /proofs/0 @ 8e9b2cccbdd9204cd27a869418c0a80b7c7d0eace21574f0af7378874d978538. Combining either dimension lower with its view's b4 gives Omega_nu(max{d,W^(2/(1+3nu))}) on the existing high-dimensional guard. The upper remains O_nu(d W^(2/(1+3nu))) there; the additive one in b3 is absorbed because W>=W_{0,nu}>0 with nu fixed. Taking their ratio gives O_nu(min{d,W^(2/(1+3nu))}). For W>=1 the dimension condition implies W^(2/(1+3nu))<=C_nu^(-1/4)d^(1/4); for W<1 it is <=1<=d. Thus on the guarded family the new lower is equivalently Omega_nu(d), without asserting an exact crossover constant. Improvement of order occurs when d/W^(2/(1+3nu)) tends to infinity. Both new exact lower bounds are valid on the whole target, so zero calls are impossible at any finite epsilon. The globally valid retained b3 upper and these lowers imply Theta_nu(d) when 0<W<=1, with constants uniform in d,H_nu,R,tau,epsilon. This is a coarse-accuracy consequence, not an extension of b4's source guard or a saturation theorem for fine accuracy.

V. Parameter roles. /parameters @ e1be3d294321ee3bab25a05b2d4b9fb30b42ec381b201529b93df389c92e4819 defines W and its dependencies. Under x=Ru and f divided by H_nu R^(1+nu), the Holder budget becomes one and the accuracy becomes 1/W; exact values are rescaled without changing the number of scalar observations. The buffer remains positive, and the retained finite-difference proof uses h<=tau with arbitrary positive h, so its call rate is uniform in tau. ZO_PROOF_HOLDER explicitly fixes 0<nu<1 and uses constants depending on nu. Moving only nu from tracked_parameters to fixed_parameters in the two active q1 records records that existing convention for every fixed nu; it does not restrict the nu domain, change a quantity expression or guarantee, or claim uniformity as nu approaches 0 or 1. The historical q2 identities are not identified with q1.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: fb9564db193d8f490955d651d1fa3be3469bcc20983451d70fce09287a473d65

#### Native item 1

Native pointer: /proofs/1/limitations/0; canonical SHA-256: b238dda521f6362498ad7b9ed529389c20ceb71be166c7816f899c531ba4a130

The retained accelerated upper and old precision-dependent lower remain conditional baseline premises; their external dependencies are not recertified.

#### Native item 2

Native pointer: /proofs/1/limitations/1; canonical SHA-256: e3b370117e30e5ca131902aa0ece6a75ca090566be8cdd1998bda2ed8e706e7d

No low-dimensional fine-accuracy saturation theorem or smoothing/regularization transfer is asserted.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 184ecce8441bbdf6167eb1d34f90c97cdbda8ad3ac262eada650c733e2fdc246

d is an integer >=1; 0<nu<1; H_nu,R,tau,epsilon>0; W=H_nu R^(1+nu)/epsilon.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: cc7e861e6a22378ce0044403d30c7f25c40aadb5c45a0c8fe80a63c8c05a08ac

Affine subclass dimension lower bounds and guarded envelope combination

### Native proof: ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

Native pointer: /proofs/2; canonical SHA-256: d495904fe22bbd3a48a1de305eccb9eeb9dbd872bc9a9691e0a612d3c1cfbd92

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: 6b16dea0aeec9f942d193da8fff707ae5c0d379f0d2e91adda1d586c4f42962a

For each fixed0<nu<1, all native d>=1,Hnu,R,tau,epsilon>0 and0<W<=1, the retained globalq1 b3 gives O_nu(d[1+W^(2/(1+3nu))])<=2C_nu d. The same-contract affine b5 gives deterministicd+1 or randomizedceil(d/9)>=d/9; thus both separate minimax q1 costs areTheta_nu(d). The complete frozen ZO_PROOF_AFFINE_DIMENSION partIV already states this closure on the entire coarse region. New nativec2 rows publish that known consequence. Although d1W1 violates oldG d>=8, it was already inside the old certified joint/proof domain, so it is not a strictdomainextension witness. W1,d1,arbitrarily smalltau>0 are included. Only fixednu enters hidden constants; no uniformnuendpoint claim orq2 identity merge is made. Originalb4 retainsG. Oldb3/source-chain recertification remains separatelypending; this derivation is conditional on the accepted baseline, not a fresh external source certification.

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: d8326689898c168b9baa4840d579a3dcb722a6196ba9935b5f203d63b2b8658d

#### Native item 1

Native pointer: /proofs/2/limitations/0; canonical SHA-256: 169044e0d4c3cda8c1a6726155e3f4ec9331b45416bd1b52141e8dd567461ff3

user-feedback-guided curated analyst_derivation; not a prior blind scout result; no old approval/source-read credit transferred

#### Native item 2

Native pointer: /proofs/2/limitations/1; canonical SHA-256: f32fbff2e31d9fb69deace36ed7b339a1d0539d8f82ae462ab845a17c6c50355

External retained premises keep their original validity; this candidate has no native approval.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 16a34262a1018e6b7e3d68fb1ed997fa6692ddede14b7e0586f6ec79f9d518fd

For each fixed0<nu<1, all d>=1,Hnu,R,tau,epsilon>0,0<W=Hnu R^(1+nu)/epsilon<=1.

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 2dea7f66a2cb372b483ac1749f231d8c86ed3c89d2a8b9ffcb158ab87458c18f

Publish the already-derived coarse-accuracy affine closure

### Native proof: ZO_PROOF_HOLDER_ROLE_RECONCILIATION_20261116

Native pointer: /proofs/3; canonical SHA-256: 071f8e623647abd620d430d6fc9de8e7c969833bc75056e7399f5914c3ba5647

#### Native field: baseline_refs

Native pointer: /proofs/3/baseline_refs; canonical SHA-256: bf78703ab44218b02bf3920638d94e2608cbcfe1823a1d3e48a160dd946fc787

#### Native item 1

Native pointer: /proofs/3/baseline_refs/0; canonical SHA-256: 74bda9968471ec2cbb5112d57c8d960538c6c47397f397611ec1c8cfee44efd0

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/0/pointer; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/0/sha256; canonical SHA-256: 07d69d61e2ff81fcf2835bed7878eabf07f18040c42f855b647d821cd910f259

51b05de8d8a8e0ae573478b47746828b88a2d983d2fe5ce9fcbc09c5eb7f5bce

#### Native item 2

Native pointer: /proofs/3/baseline_refs/1; canonical SHA-256: da1be1fa566f01849620469710961b337738629de9a435440fcadd8655cb8a0b

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/1/pointer; canonical SHA-256: 4b81cab280b1e31c2ea7afa9a416577b7c9c22795698d5d642e0394c36a90edd

/quantities/2

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/1/sha256; canonical SHA-256: d291f5ef382672ac6a0218a82d4451c0e4c4c0f81f45a8b80851641195b795dd

fb3ad8d6809557267686a323b048448d3c54f50b399e14315754d4dbe1a6a61c

#### Native item 3

Native pointer: /proofs/3/baseline_refs/2; canonical SHA-256: 9e6059c9ed49c4366b5c67322b8ca74682188c4915b0438ed15fe0942ac0684d

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/2/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/2/sha256; canonical SHA-256: 8760cf1f8df73f0b8bf36cdec472b0ff6dd02a79c542971ce79b563065a51607

e1be3d294321ee3bab25a05b2d4b9fb30b42ec381b201529b93df389c92e4819

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: b30123c9e7040fe42a147ccd95481d978826ef0912fbec87fad30d68126edbca

The CURRENT frozen native /quantities/0 and /quantities/2 already put parameter SO_ZO_E07_neighborhood_p_6290a52d96 in fixed_parameters and exclude it from tracked_parameters; both are unchanged in this candidate. Their exact canonical hashes are 51b05de8d8a8e0ae573478b47746828b88a2d983d2fe5ce9fcbc09c5eb7f5bce and fb3ad8d6809557267686a323b048448d3c54f50b399e14315754d4dbe1a6a61c. The target fixed alias is the literal native nu symbol and names that same parameter. The remaining five joint coordinates and derivedW are unchanged, with uniform_in covering everyjoint coordinate, and only fixednu allowed in hidden constants. Thus no current controlled metadata normalization is needed or proposed. Mark targetresolution resolved and remove stale active requests claiming that currentq1 tracksnu. The historical quantity_metadata_normalization_log is preserved byte-for-byte as data; it is evidence of the prior sequence, not a fresh operation or newread/approval credit. Retain all separate source-chain recertification and finer-accuracy obligations. Resolving this role annotation does not resolve literature or recertify historical source premises, alter a minimax task, mergeq2/q1, or add a new rate.

#### Native field: proof_refs

Native pointer: /proofs/3/proof_refs; canonical SHA-256: d934cb996025e51da156430181dc224175552271e7c145cf6a946e8970e6e8c7

#### Native item 1

Native pointer: /proofs/3/proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native item 2

Native pointer: /proofs/3/proof_refs/1; canonical SHA-256: 7d4f1029db044951f0a9b42b06fd65e78e3539000eef8266adc6c8e822275b95

ZO_PROOF_AFFINE_DIMENSION

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: 3527b9882f9311a8740b72a305ee77ec90cc66e5ee687f8727bc1ac479ed5741

Unchanged deterministic/randomized native q1 fixed-nu families.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: fdf7f72ade72f7613f73852f1198c2bc51d5587bff9370386d99aecbf34ea404

Reconcile active joint-role requests with already normalized native quantities

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 9158b3918d793f8f1712ce347a77323d4c003ae0ff1d026f33d4ef361be3b00c

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 175f75f1457bbb10de5085617c3b58ac5fa70c2c91fc1e8a1de5a32c762d80ef

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 1be4df1882d7dc11262587d473c3249fb487e302d20679736541e076f34b8e52

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: ef0b1e5fdac8755356d02984f3fa24c510e67559724f3923955eb93302b0dd6f

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 64f30799886797821382addf983ec01a5c3711692d0e3b0d1708c334d497bfb3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 45f1160f7272623c213cff5e47fa967191c639d6175a43417f9298408bb4eb84

None.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 5829a28477ba6822c9d6ccd2025a6e5261969490536cdff085f41e992c77848d

SO_ZO_E07_neighborhood__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 3e72c54439e32a133a8632f4a37a2cfe3801c719f811ac50ad53770e8c7d3b3e

Distinct historical q2 quantity; no q2-to-q1 transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 850b2404f434493bbb1f5b42c97041abb8128c8b84ec4a9ce4c93157c38727d8

W>=1, original guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 6a1bc94dc7cebb708c803483b2ce4ec95feb27a74fe976c1143a2b7e07506a91

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 45f1160f7272623c213cff5e47fa967191c639d6175a43417f9298408bb4eb84

None.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 4382cda97485f4a0d75a3a07c52ffbdfc76baca25bc6860e2aac0e7b5d37c23e

SO_ZO_E07_neighborhood__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 3e72c54439e32a133a8632f4a37a2cfe3801c719f811ac50ad53770e8c7d3b3e

Distinct historical q2 quantity; no q2-to-q1 transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 1525a3f274cf597b2142ed459aff548e86892308b52bcdd11aabd04f4d2b311d

Original small-accuracy high-dimensional source window.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 86df9b21e925ffa95a0d0a657ce4c65bb01860259477c650a6375eb35b82a8e2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: d754c71e5e50ff3e695c0ac14a1e41414c2f86de8f09641ffe43d4cffc5e3f4a

SO_ZO_E07_neighborhood__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 9d6caff56a6ef6899529e2370cc1e6ef7a9320f94cdf118a1ff09095bf4cac7d

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 798f3a75c3a50626ead772ae7f086df470b5624403cb26887448df5ba44765b3

Conditional baseline retention; W>=W_{0,nu}>0 absorbs the additive one.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: eadd94c66e2c0e3ac3b85197016bcf615b7336eecc1ac227eb444ccf96ec2662

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: bf476e989586d32a2ce02d9632836c92882a871d13a30b0de179a23df4977f99

SO_ZO_E07_neighborhood__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 9d6caff56a6ef6899529e2370cc1e6ef7a9320f94cdf118a1ff09095bf4cac7d

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: ef5ef65f3828941f01a5bedcb8844d5401ba8120a122acc903598b0691c46904

Retained guarded precision lower in the maximum; asymptotically redundant to the new dimension term on G.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: 0c44a07b087c3678e6a9d24d8ece285987a4b0b2a0bd26e42d4c8ec6bca369b7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: 6ab631db2880106e77c61285acd88f191c50d5e4a5ccd4cf96ccdeecfc6be23c

SO_ZO_E07_neighborhood__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: 10b0e6ebe4bbd0dfe88819bd13420698617edbd8e968f5324f9a29693900529b

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 7d4f1029db044951f0a9b42b06fd65e78e3539000eef8266adc6c8e822275b95

ZO_PROOF_AFFINE_DIMENSION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: 4cca111c3ee8cb9c30c177eb0b352904ec036fa6252968cd876a41bbb08d4598

Exact d+1 affine lower, with all adaptive queries and unqueried outputs covered.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 8025f9836b14630c5e1ea39d31e5c2499012c617c4e80c48b37905814693326c

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 2a67e346777d400abe70cc89c43fb91ed979c63a5dbb47d8bd8580d78f144936

G is a symbolic source activation condition; no exact envelope crossover is asserted.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 67f60b1375cabc3d033aaa6489da7191f6f6253fe01d5231270b9a484971eae0

W>=W_{0,nu}>0 absorbs b3's additive one with nu-dependent constants.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 3a5c1acb401f162050a8f674b9f041bcdded5b6d9b41422948b152425174e519

Globally b5 rules out zero calls, including d=1; b3+b5 give Theta_nu(d) for 0<W<=1.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 7844c604022fc7fdad5ef5243ddd1c62aa9409c17afc493561733ed8ecd2a9bd

tau>0 can be arbitrarily small. nu=0, nu=1 and tau=0 are outside the contract.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: ecda5fc89c4eb17d66fb76f5f75520330059aee3bcd63a80bb9824d1844dcb01

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/0; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: ecda5fc89c4eb17d66fb76f5f75520330059aee3bcd63a80bb9824d1844dcb01

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: e4c17e5962820ad1f3ad8db3985a01965be3ffd167442af88167c1957b53f4e1

O_\nu\!\left(\frac{dW^{2/(1+3\nu)}}{\max\{d,W^{2/(1+3\nu)}\}}\right)=O_\nu(\min\{d,W^{2/(1+3\nu)}\})

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 40a398cbf76b57c3a2037156b10896c5d876bd91958ad5cf7b5c57db507e894b

\Omega_\nu(\max\{d,W^{2/(1+3\nu)}\})

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 1a085902eaeecf3833185e8636e0a80f1c737dbfc0c78d03d085c62b42a9ade2

At most O_nu(W^(2/(1+3nu))) on G; sharper precision and low-dimensional saturation are not certified.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 59d1bfe8032dbfae3fecddaab4ae7ee4be7da37d3f6293877c0c41dd590902c8

O_\nu(d W^{2/(1+3\nu)})

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 2bebe81f92efdef357a802adfb22a9cf3c0c57beee3f73961149ca15e0217f1b

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 438738ab246ad7a3cb2085b7b01752f61be212f43dca5ff10b3a9a9c676eedb4

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: c7a31aa3f72f205d15a69e6a6006759c2463cb87ad4d769dfafbdd60301885ef

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 45f1160f7272623c213cff5e47fa967191c639d6175a43417f9298408bb4eb84

None.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: baede674fd0ae9d16becd2d17461249459b01b26ae3cef4573696dcc4a1d5c47

SO_ZO_E07_neighborhood__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 3e72c54439e32a133a8632f4a37a2cfe3801c719f811ac50ad53770e8c7d3b3e

Distinct historical q2 quantity; no q2-to-q1 transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 850b2404f434493bbb1f5b42c97041abb8128c8b84ec4a9ce4c93157c38727d8

W>=1, original guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: f16225532e5d8dec9b1764c617f86997b18d1250a65f5a114ab7951b946c6116

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 45f1160f7272623c213cff5e47fa967191c639d6175a43417f9298408bb4eb84

None.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: e1342d64304ea0d85884a307dc813d8447bc8349365fb5457258df5c9c01372c

SO_ZO_E07_neighborhood__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 3e72c54439e32a133a8632f4a37a2cfe3801c719f811ac50ad53770e8c7d3b3e

Distinct historical q2 quantity; no q2-to-q1 transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 1525a3f274cf597b2142ed459aff548e86892308b52bcdd11aabd04f4d2b311d

Original small-accuracy high-dimensional source window.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 089d7f530ba23fa85de750780f9652a8a888a20af52cdae31d8c65cd62e76ec6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: a5e70eabcc3a730664047de954dd6f60e79d434558ebb02f417abb92792009a7

SO_ZO_E07_neighborhood__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 9d6caff56a6ef6899529e2370cc1e6ef7a9320f94cdf118a1ff09095bf4cac7d

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 798f3a75c3a50626ead772ae7f086df470b5624403cb26887448df5ba44765b3

Conditional baseline retention; W>=W_{0,nu}>0 absorbs the additive one.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: c694799347b36847f0475dbde401b97a5700aeebaad913cc54f95cafde48864e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: 3f8872ec1292ea4554c8c22a721503f2a266232663d7ab853bc542e7fd5d93e9

SO_ZO_E07_neighborhood__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 9d6caff56a6ef6899529e2370cc1e6ef7a9320f94cdf118a1ff09095bf4cac7d

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: ef5ef65f3828941f01a5bedcb8844d5401ba8120a122acc903598b0691c46904

Retained guarded precision lower in the maximum; asymptotically redundant to the new dimension term on G.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: 2e8b965c190d9ffa2de4307a716ccb271036422aa01d10535bb1a2694e0440d6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: 7f1dbab3e9f430813219675b5655627b86f81863fdc6654493101f1cc6ff5fd8

SO_ZO_E07_neighborhood__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: 10b0e6ebe4bbd0dfe88819bd13420698617edbd8e968f5324f9a29693900529b

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 7d4f1029db044951f0a9b42b06fd65e78e3539000eef8266adc6c8e822275b95

ZO_PROOF_AFFINE_DIMENSION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: e391d888dfee5ca177da4fd11a384ec735a1a94e073038d9b444ccce4682c268

Exact ceil(d/9) affine lower for private-random 2/3 success with fixed path cap.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 8025f9836b14630c5e1ea39d31e5c2499012c617c4e80c48b37905814693326c

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 2a67e346777d400abe70cc89c43fb91ed979c63a5dbb47d8bd8580d78f144936

G is a symbolic source activation condition; no exact envelope crossover is asserted.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 67f60b1375cabc3d033aaa6489da7191f6f6253fe01d5231270b9a484971eae0

W>=W_{0,nu}>0 absorbs b3's additive one with nu-dependent constants.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 3a5c1acb401f162050a8f674b9f041bcdded5b6d9b41422948b152425174e519

Globally b5 rules out zero calls, including d=1; b3+b5 give Theta_nu(d) for 0<W<=1.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: 7844c604022fc7fdad5ef5243ddd1c62aa9409c17afc493561733ed8ecd2a9bd

tau>0 can be arbitrarily small. nu=0, nu=1 and tau=0 are outside the contract.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: ecda5fc89c4eb17d66fb76f5f75520330059aee3bcd63a80bb9824d1844dcb01

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/0; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: ecda5fc89c4eb17d66fb76f5f75520330059aee3bcd63a80bb9824d1844dcb01

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/0; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: e4c17e5962820ad1f3ad8db3985a01965be3ffd167442af88167c1957b53f4e1

O_\nu\!\left(\frac{dW^{2/(1+3\nu)}}{\max\{d,W^{2/(1+3\nu)}\}}\right)=O_\nu(\min\{d,W^{2/(1+3\nu)}\})

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 40a398cbf76b57c3a2037156b10896c5d876bd91958ad5cf7b5c57db507e894b

\Omega_\nu(\max\{d,W^{2/(1+3\nu)}\})

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 1a085902eaeecf3833185e8636e0a80f1c737dbfc0c78d03d085c62b42a9ade2

At most O_nu(W^(2/(1+3nu))) on G; sharper precision and low-dimensional saturation are not certified.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 59d1bfe8032dbfae3fecddaab4ae7ee4be7da37d3f6293877c0c41dd590902c8

O_\nu(d W^{2/(1+3\nu)})

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 1710c786483407ee8e264f864c518febc92c476cce28d35e10e5626b42ae05b8

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 15806ff65a199916af36bc972bcf99ba63ad483dcc9dc02313aebe9f0534fe10

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 99b9c46aa0a698c233e2585cf75c6b1726c75901061ec91f4e25a64055eed05b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 5829a28477ba6822c9d6ccd2025a6e5261969490536cdff085f41e992c77848d

SO_ZO_E07_neighborhood__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 3e72c54439e32a133a8632f4a37a2cfe3801c719f811ac50ad53770e8c7d3b3e

Distinct historical q2 quantity; no q2-to-q1 transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 850b2404f434493bbb1f5b42c97041abb8128c8b84ec4a9ce4c93157c38727d8

W>=1, original guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 87220cb034ab554804756d78e02f501d9f35d18ceb7e2773684aeb4394763254

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 4382cda97485f4a0d75a3a07c52ffbdfc76baca25bc6860e2aac0e7b5d37c23e

SO_ZO_E07_neighborhood__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 3e72c54439e32a133a8632f4a37a2cfe3801c719f811ac50ad53770e8c7d3b3e

Distinct historical q2 quantity; no q2-to-q1 transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 1525a3f274cf597b2142ed459aff548e86892308b52bcdd11aabd04f4d2b311d

Original small-accuracy high-dimensional source window.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: bbe77f269ba4e5c8e4bbfd80d103fa848bdd58e8c255a692a1df846662006259

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 1378b093104aa7fd2ed1b0304f53a52fe06a901ac55f03405d63a068be781ba7

Fix0<nu<1; d integer>=1; H_nu,R,tau,epsilon>0;0<W=H_nu R^(1+nu)/epsilon<=1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: d754c71e5e50ff3e695c0ac14a1e41414c2f86de8f09641ffe43d4cffc5e3f4a

SO_ZO_E07_neighborhood__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 9e6dd3281c9bb73ab09001d59455626b37a0f0d233e298d5dcb11b662853256c

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 8277755b003dc176592b17032c722cf73bc9b9fa8fe8512a0884ee408909fe5a

Same native q1; coarse bound follows from complete new publishing derivation.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: b8c72257b8a267d76ed80a9de9148639a5f4e937374c0a4cbc700cd7e7dd2170

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: bf476e989586d32a2ce02d9632836c92882a871d13a30b0de179a23df4977f99

SO_ZO_E07_neighborhood__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 9d6caff56a6ef6899529e2370cc1e6ef7a9320f94cdf118a1ff09095bf4cac7d

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: e0aef9f60b532f11b7ba52ae212a3404ce9f93622976503a0e0b00e2c89c0774

Only valid on its original G overlap; W^p<=1<=d on the coarse region, so it adds no stronger order than the affine lower. Its original guard is unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: 47e2003a4aab45c1c187ba8f5046ee06d2392fdc8db4720bf7d108d3933c65fb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 1378b093104aa7fd2ed1b0304f53a52fe06a901ac55f03405d63a068be781ba7

Fix0<nu<1; d integer>=1; H_nu,R,tau,epsilon>0;0<W=H_nu R^(1+nu)/epsilon<=1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: 6ab631db2880106e77c61285acd88f191c50d5e4a5ccd4cf96ccdeecfc6be23c

SO_ZO_E07_neighborhood__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 9e6dd3281c9bb73ab09001d59455626b37a0f0d233e298d5dcb11b662853256c

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 8277755b003dc176592b17032c722cf73bc9b9fa8fe8512a0884ee408909fe5a

Same native q1; coarse bound follows from complete new publishing derivation.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 97510d4281d6ec4990b6dc10d0406eb53651691e948ffa0b092cf266036e06cc

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: e81c7b31f20853dc9476cf832ee8ed216f4e61c628c8591924eb8812d2bccd0e

W=1 included;d=1 included;arbitrarily smalltau>0 permitted.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 9a4ffeed34e4999bbc9fbb2fb8309042f47f4bccca63776a9f6da6e684e76bf0

Onlynu may enter hidden constants. No high-dimensional b4 guard extension.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: ecda5fc89c4eb17d66fb76f5f75520330059aee3bcd63a80bb9824d1844dcb01

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/constant_dependencies/0; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: ecda5fc89c4eb17d66fb76f5f75520330059aee3bcd63a80bb9824d1844dcb01

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/fixed_parameters/0; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: 888d4fd54755f0d9f8c1044e3bcc1c0ca6c178957ba9eb0cece4e1196c5bb12b

\Theta_\nu(1)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 2c3270cd326857cb83ddaf05fc93e833998ac4db0784515c3d2791b08b50a98d

\Omega(d)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 82872db19b7b113c5c87956359d27dcc96bd897fbabf0fdcc7f7be031ec4c65b

No rate gap on this guarded coarse region, conditionally on retained b3. No maximal coarse threshold or global all-precision closure is asserted.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: 5263d192b67f1751aabc75eb1019e141f6f05c5ae0f36b418930554edb3cfc18

O_\nu(d)

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: efce98db684f371b5c99c9e246a20c4507ae4e4d2c06e24d290f8f926e5d93ed

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 1b99524838f139cc2bdcfb4d84a989a434d421ba624798fbbed9d649d1b6daeb

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: a713c7244b2a86bd85d3c0ac152b38e26c8f34515bbfb494a41d19816dc644f9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: baede674fd0ae9d16becd2d17461249459b01b26ae3cef4573696dcc4a1d5c47

SO_ZO_E07_neighborhood__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 3e72c54439e32a133a8632f4a37a2cfe3801c719f811ac50ad53770e8c7d3b3e

Distinct historical q2 quantity; no q2-to-q1 transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 850b2404f434493bbb1f5b42c97041abb8128c8b84ec4a9ce4c93157c38727d8

W>=1, original guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: f9b2f1e7ac51fd134fcd30a98c95de9500308299dff844f6b94e89f856f61fd5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: e1342d64304ea0d85884a307dc813d8447bc8349365fb5457258df5c9c01372c

SO_ZO_E07_neighborhood__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: 3e72c54439e32a133a8632f4a37a2cfe3801c719f811ac50ad53770e8c7d3b3e

Distinct historical q2 quantity; no q2-to-q1 transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 1525a3f274cf597b2142ed459aff548e86892308b52bcdd11aabd04f4d2b311d

Original small-accuracy high-dimensional source window.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 804eb9dabaf0aac5c8cb1bc30e1783e27e46f9a44306e48895464851fe21ce14

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 1378b093104aa7fd2ed1b0304f53a52fe06a901ac55f03405d63a068be781ba7

Fix0<nu<1; d integer>=1; H_nu,R,tau,epsilon>0;0<W=H_nu R^(1+nu)/epsilon<=1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: a5e70eabcc3a730664047de954dd6f60e79d434558ebb02f417abb92792009a7

SO_ZO_E07_neighborhood__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 9e6dd3281c9bb73ab09001d59455626b37a0f0d233e298d5dcb11b662853256c

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 8277755b003dc176592b17032c722cf73bc9b9fa8fe8512a0884ee408909fe5a

Same native q1; coarse bound follows from complete new publishing derivation.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 03eec35684a88561b7ddfda43a5aca0ac291b52d6f444273352ae33f47733247

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: 3f8872ec1292ea4554c8c22a721503f2a266232663d7ab853bc542e7fd5d93e9

SO_ZO_E07_neighborhood__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 9d6caff56a6ef6899529e2370cc1e6ef7a9320f94cdf118a1ff09095bf4cac7d

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: e0aef9f60b532f11b7ba52ae212a3404ce9f93622976503a0e0b00e2c89c0774

Only valid on its original G overlap; W^p<=1<=d on the coarse region, so it adds no stronger order than the affine lower. Its original guard is unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: 4ca0e8564c92690aabcb8969761a8863d69f6738bd0aa49368eb059c6da97358

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: 1378b093104aa7fd2ed1b0304f53a52fe06a901ac55f03405d63a068be781ba7

Fix0<nu<1; d integer>=1; H_nu,R,tau,epsilon>0;0<W=H_nu R^(1+nu)/epsilon<=1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: 7f1dbab3e9f430813219675b5655627b86f81863fdc6654493101f1cc6ff5fd8

SO_ZO_E07_neighborhood__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: 9e6dd3281c9bb73ab09001d59455626b37a0f0d233e298d5dcb11b662853256c

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: 8277755b003dc176592b17032c722cf73bc9b9fa8fe8512a0884ee408909fe5a

Same native q1; coarse bound follows from complete new publishing derivation.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: 97510d4281d6ec4990b6dc10d0406eb53651691e948ffa0b092cf266036e06cc

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: e81c7b31f20853dc9476cf832ee8ed216f4e61c628c8591924eb8812d2bccd0e

W=1 included;d=1 included;arbitrarily smalltau>0 permitted.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: 9a4ffeed34e4999bbc9fbb2fb8309042f47f4bccca63776a9f6da6e684e76bf0

Onlynu may enter hidden constants. No high-dimensional b4 guard extension.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: ecda5fc89c4eb17d66fb76f5f75520330059aee3bcd63a80bb9824d1844dcb01

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/0; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: ecda5fc89c4eb17d66fb76f5f75520330059aee3bcd63a80bb9824d1844dcb01

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/0; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 888d4fd54755f0d9f8c1044e3bcc1c0ca6c178957ba9eb0cece4e1196c5bb12b

\Theta_\nu(1)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 2c3270cd326857cb83ddaf05fc93e833998ac4db0784515c3d2791b08b50a98d

\Omega(d)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 82872db19b7b113c5c87956359d27dcc96bd897fbabf0fdcc7f7be031ec4c65b

No rate gap on this guarded coarse region, conditionally on retained b3. No maximal coarse threshold or global all-precision closure is asserted.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: 5263d192b67f1751aabc75eb1019e141f6f05c5ae0f36b418930554edb3cfc18

O_\nu(d)

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 34d28b41193fd0bc45ce85f4bfd161250479950586081846fd7c03a0dbd31647

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: cc94c4beabd8dc4c4f11b565c5772af3035d58c6807a0ef75b1f23c795f5d714

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 64248f15a6cd79187380247b0ec90b72c097a318f925c065a86647a77f0b7cc6

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 2117a83ad8116727ac02f1aa241104512467811b74e7f71c0fdebc66c5bb554b

coarse_G

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 9e6dd3281c9bb73ab09001d59455626b37a0f0d233e298d5dcb11b662853256c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 9f8a53b1f08c6b3621c929464e617347f2591b4dfbb5254933e6b54002269d33

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 7a17f64436581038bd888d438dc17c040826fa4aa2a1b660a01778d94a450481

Both old guarded comparisons and the newly registered closed coarse comparisons apply. Closure refers only to the two newly published coarse comparisons; old high-dimensional entries are not claimed optimal. Retained b3 source-chain recertification remains separately pending.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 30f227875a71b2eae0633a802f798923d1a4badb4f3c1233e3dd56e6e59fe9d4

D intersect G intersect{0<W<=1}

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 00fde33ff75d6753aeeed974b33de85b6c1e297a20cadf9f01b6fe9c334b5258

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 80a81811c16e7d0ae0bdc7ac3d2676a23e4652940240ccb1671b0dc095d29829

coarse_not_G

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 9e6dd3281c9bb73ab09001d59455626b37a0f0d233e298d5dcb11b662853256c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 9f8a53b1f08c6b3621c929464e617347f2591b4dfbb5254933e6b54002269d33

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 4e259a0244f5280ca249ccde1ad9935ec2729b8b636b7bba4dfcee29e50fb993

New native comparison coverage of already-derived Theta_nu(d);d=1,W=1 witnesses nonempty outsideG. Closure refers only to the two newly published coarse comparisons; old high-dimensional entries are not claimed optimal. Retained b3 source-chain recertification remains separately pending.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 7a4b080c6d764b6cd8afb98e6080d57cf3d3ff6d27a598b537ca556cb9cbd874

D intersect G^c intersect{0<W<=1}

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

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 832225bccf4d09e787c0206520241c8477d12071c7732aedf3d5160353c56034

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 6a3c46de0ad7db0b193ddab1c47ff1d41478232c259776afbd3b1d2fa3c5e347

fine_G

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 709585414f582def3a0f516a02d507385d214b40359572bd7350251e8680d8e9

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/1; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 5a2fe69a62fb37e7bafe3eb521c822615b01a377bc8551b219c3834aeccbb3ed

Original high-dimensional scientific brackets retained.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: a8f372c499c955ad15e61d0ab9cbe2757af760566bc94b061cd7de7fdcbec0c2

D intersect G intersect{W>1}

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: 08c3cea05f170448c21c38d428921833e0843ef09c162bc854ccf3496f7b08de

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: c7e3f1600ab9063214a79c5b8401577c50b5aa037065c01d9749ade107d0c5e9

fine_not_G

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: 2719b9193c651fd3603879f87bab763436a941c46fdb65b077dde85e4e3434fa

Only global b3/b5 remain; sharper envelopes are unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: f0fab9cd4114e41ccd747bca4bdf2c181673b053d4808fdbcdb28492d95d6c9b

D intersect G^c intersect{W>1}

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: f649883d4709f24d53b5ece8a60a5961f23ad58724d14174d9718c030a433ab6

G retains its exact original symbolic source guard. The independent Boolean choices W<=1 versusW>1 and G versusG^c partitionD; empty cells harmless. Each view has its own native comparison.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: fd6f627e6bc3ec38f1da11e2611f4631b841aa50420f11dece67e5a4499d6878

No bookkeeping omissions. Fine-complement remains scientifically unassessed beyond the globally recorded upper and affine lower.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 554c76ce4caa853eb41ed1be1271862b74e60d1da90d88aa1f5c931681650e33

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 620e79ef90498d26d0dbd2193e15f7b8e5642c65406a7e70fb80949e042bd8ac

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 16ef0dd4e048c6dc3f41d3ad497f20f6b7c1ed406a30fca814851471dfe6f8f1

Combine compatible lower bounds by a maximum and divide the unchanged upper by it. Exact constants d+1 and ceil(d/9) describe the new inequalities; rate crossovers remain asymptotic. Globally, retained b3 and new b5 also give Theta_nu(d) for 0<W<=1 and rule out zero calls.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: d10a76b2b4ec939af41bc1acddfe7c19d8249442c4a48660d60664613098653e

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: f4834beeb1229fdec3ad69f2f38d89b67ae7b57ecbac4d19fec5c78904cc96c4

affine-dimension-deterministic

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: bb03200d020801dc2f6b0727148ff928f89c51a49aaea08c981d6ecef55fec6f

Within the registered guard, d/W^(2/(1+3nu)) tends to infinity: lower improvement factor d/W^(2/(1+3nu)).

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: ccb1f2b82f4e7f07c6efb4f60ba3840863351a9107b349ba251061f4b5bbf55d

Upper unchanged; lower Omega_nu(max{d,W^(2/(1+3nu))}) on the registered guard.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: cbc04f7f3ced81363f88291d0168d4301a8ca880ba3fd70cfdd3b9abcf85fa7a

Upper O_nu(d W^(2/(1+3nu))); lower Omega_nu(W^(2/(1+3nu))) on the registered guard.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 18b6f68dd592faa8bb410819350c9b71dc9bc292ca69b801cc49e5f8fa432c51

Upper/status unchanged; lower order unchanged if d=O_nu(W^(2/(1+3nu))). No new native comparison outside G.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: a1baaa1b54a50aab06544fccb057f24b80b2dffb57877113faa8c3aea8d1739f

D; adopted on D intersect G.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: e8d07e8932c60aa90c2c88fefdbd09fd7e82cd3d5a1038fd6d1add39b9058ffa

Fix nu,H_nu,R,tau; let W tend to infinity, epsilon=H_nu R^(1+nu)/W, and choose integer d>=max{8,C_nu W^(8/(1+3nu)) log(eW)}. Then d/W^(2/(1+3nu)) tends to infinity.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 01f7481901aea929d17657d1b7049c7b107f4a18a0cdfe924749a07a1d03d026

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 16ef0dd4e048c6dc3f41d3ad497f20f6b7c1ed406a30fca814851471dfe6f8f1

Combine compatible lower bounds by a maximum and divide the unchanged upper by it. Exact constants d+1 and ceil(d/9) describe the new inequalities; rate crossovers remain asymptotic. Globally, retained b3 and new b5 also give Theta_nu(d) for 0<W<=1 and rule out zero calls.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: fcaf56f37af1d3e99dfaaec2caf23a14d79ca20c6c24040aa32e70fd67666255

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 502a00d41e222fd1a0456e806f71030810967743f8ddf156567615cfbc6109aa

affine-dimension-randomized

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: bb03200d020801dc2f6b0727148ff928f89c51a49aaea08c981d6ecef55fec6f

Within the registered guard, d/W^(2/(1+3nu)) tends to infinity: lower improvement factor d/W^(2/(1+3nu)).

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: ccb1f2b82f4e7f07c6efb4f60ba3840863351a9107b349ba251061f4b5bbf55d

Upper unchanged; lower Omega_nu(max{d,W^(2/(1+3nu))}) on the registered guard.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: cbc04f7f3ced81363f88291d0168d4301a8ca880ba3fd70cfdd3b9abcf85fa7a

Upper O_nu(d W^(2/(1+3nu))); lower Omega_nu(W^(2/(1+3nu))) on the registered guard.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 18b6f68dd592faa8bb410819350c9b71dc9bc292ca69b801cc49e5f8fa432c51

Upper/status unchanged; lower order unchanged if d=O_nu(W^(2/(1+3nu))). No new native comparison outside G.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: a1baaa1b54a50aab06544fccb057f24b80b2dffb57877113faa8c3aea8d1739f

D; adopted on D intersect G.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: e8d07e8932c60aa90c2c88fefdbd09fd7e82cd3d5a1038fd6d1add39b9058ffa

Fix nu,H_nu,R,tau; let W tend to infinity, epsilon=H_nu R^(1+nu)/W, and choose integer d>=max{8,C_nu W^(8/(1+3nu)) log(eW)}. Then d/W^(2/(1+3nu)) tends to infinity.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 0b35584f1bc8c4a7db33ab7a472fed76cb72fcdaa5aaae2a67f4a826b0364635

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: b30123c9e7040fe42a147ccd95481d978826ef0912fbec87fad30d68126edbca

The CURRENT frozen native /quantities/0 and /quantities/2 already put parameter SO_ZO_E07_neighborhood_p_6290a52d96 in fixed_parameters and exclude it from tracked_parameters; both are unchanged in this candidate. Their exact canonical hashes are 51b05de8d8a8e0ae573478b47746828b88a2d983d2fe5ce9fcbc09c5eb7f5bce and fb3ad8d6809557267686a323b048448d3c54f50b399e14315754d4dbe1a6a61c. The target fixed alias is the literal native nu symbol and names that same parameter. The remaining five joint coordinates and derivedW are unchanged, with uniform_in covering everyjoint coordinate, and only fixednu allowed in hidden constants. Thus no current controlled metadata normalization is needed or proposed. Mark targetresolution resolved and remove stale active requests claiming that currentq1 tracksnu. The historical quantity_metadata_normalization_log is preserved byte-for-byte as data; it is evidence of the prior sequence, not a fresh operation or newread/approval credit. Retain all separate source-chain recertification and finer-accuracy obligations. Resolving this role annotation does not resolve literature or recertify historical source premises, alter a minimax task, mergeq2/q1, or add a new rate.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 709585414f582def3a0f516a02d507385d214b40359572bd7350251e8680d8e9

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 2e928593ba4d9415918726b47607ae56e3252990e7fc27db6b43bba9d4832f57

fixed-holder-exponent-roles

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 774d700cb8e8661f08feb81ca31f48486e8b172ac47e83700af116837c0f5780

No independent cost improvement from role normalization.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: bbb74a48803dbc83c68c2e7d807ddacdf50bc9fbf559e467b7cab168ef2e1438

Current fixednu quantities are kept byte-identical; targetresolution and active requests now agree with them.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 350510f2b5bf47109d763391ba0a1f79a6bdb7d68015bbff0fda40ddeae7b818

Historical pre-normalization metadata once trackednu; the CURRENT frozen quantities0/2 already fixnu and exclude it fromtrackedparameters.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 02df1394799f974c256f871b8a400e0208a2b372ee0837750f4587f43643835b

All quantity expressions, units, views, guarantees, resources and parameter domains.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 9578b56872cf2429e559b19ea1b5f3fd105b6e9e03bfb27070380f7c0b25fb7b

Actual frozen quantities0/2, their canonical hashes, exact native fixednu parameter, and unchanged historical normalizationlog; no current metadata operation is needed.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 3b97d018cb77c4b316ebaaaf166df2af3f49bb7c0bbe88366ed77363b4e5cbc5

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 314f7318259417d4a43af3c2de4d23ae9bc1e99161b523a63dd2d3f4eb6b9a7e

Direct applicability fails; any future reduction needs its own proof and guard.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 709585414f582def3a0f516a02d507385d214b40359572bd7350251e8680d8e9

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 7c618c960993c2c63f9a8722ed4c676f485abf712e8849cc8d7e95eb1eb7db6b

katyusha-direct-theorem

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 50446632d7eed558fb7d733ed5a6dd99640a04b4464028aab864dc38ad6db49e

None established.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: ddb0cfec53b6f735819139d0a3f8cdafc7dedc855f465a3a487c20f7291a38cd

No source claim enters either envelope.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: 2ea197d5d74e514094031fa03b25e2146a667b7d6f94eac83ee380e9a2354fe3

Native envelopes before evaluating this lead.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 3269a06b47e4cb16d1161e6045fa8fe2a6c08969036aea6a2abceb772094f0dd

Only the source contract described in its finding.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: bb7f5e87dffe8fe2150cd69d2fa0f4a412adabf182a69f76ff8497c3aa48cb10

Source hypotheses do not cover the locally Holder, ball-constrained target.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: 24e8e6031f3f9bf81435b86d88caca1d2b51067adc0ac4f42000a4301e472b90

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 314f7318259417d4a43af3c2de4d23ae9bc1e99161b523a63dd2d3f4eb6b9a7e

Direct applicability fails; any future reduction needs its own proof and guard.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 709585414f582def3a0f516a02d507385d214b40359572bd7350251e8680d8e9

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: c7ee2e20ea7a02761b008b3fb453c01043661da9636ff1b702e985ad860ba01a

ardfds-direct-theorem

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 50446632d7eed558fb7d733ed5a6dd99640a04b4464028aab864dc38ad6db49e

None established.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: ddb0cfec53b6f735819139d0a3f8cdafc7dedc855f465a3a487c20f7291a38cd

No source claim enters either envelope.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: 2ea197d5d74e514094031fa03b25e2146a667b7d6f94eac83ee380e9a2354fe3

Native envelopes before evaluating this lead.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: 3269a06b47e4cb16d1161e6045fa8fe2a6c08969036aea6a2abceb772094f0dd

Only the source contract described in its finding.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: bb7f5e87dffe8fe2150cd69d2fa0f4a412adabf182a69f76ff8497c3aa48cb10

Source hypotheses do not cover the locally Holder, ball-constrained target.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: ec4716e50f0b2ec50264d6f84a526ba35760065b956c2a080a6d341cc8941b1f

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 8d95b102989fb464044ace0926c0e937dc080387e708b1084d75b4b88d4c7b62

Same-quantity retainedb3+b5 algebra and existing baseline coarse proof already cover the whole region. Adding nativec2 closes the publication gap only; no strictdomainextension witness is supplied.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: 9f8a53b1f08c6b3621c929464e617347f2591b4dfbb5254933e6b54002269d33

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: 98134e10e4472452731b3d63ffbf35ec5124648ed3c796fe1bc4170555d1510d

E07_COARSE_NATIVE_CLOSURE_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: 46c73d24e97d0c975ed165461c52c883707932f1562f1d0843d073996cf190a3

Native row publication only: no new inequality, no expansion beyond the already certified mathematical domain, and no new main-rate improvement.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: 7249f099445029410a160bddb6fd935004aff56d921f462672a9f41815a78001

explicit_region_registration

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/5/new_envelope; canonical SHA-256: 83917c440b35eb4bfcd2eae0030ed38242d9c872e328d5319d6796022f2eb00b

The same proved Theta_nu(d) is now published in two native optimal coarse comparisons.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/5/old_envelope; canonical SHA-256: 87d99ec9c5b7150ed3849d838c4504442a2bf0d8115e4ad58c6187915926d3bc

The frozen joint analysis and ZO_PROOF_AFFINE_DIMENSION partIV already establish Theta_nu(d) on the complete0<W<=1 domain, includingd1W1; only native comparison rows wereG-restricted.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/5/unchanged_region; canonical SHA-256: ae88cd7a279cf69f0b2b4b906638216d5c38ec8c36bda350024a034a43b8717c

All immutable native contracts; all statements outside the explicit new guarded adoption remain unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: dbc4cce450b944b1da893c7ca4d51366a163a8311e2fa1fecda0dd5cc75bfa1d

Fixednu0<nu<1;full nativepositive domain with0<W<=1.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: d34c7cf6635cde23b63e3c86120399384b09f93cc5b4b1381ce2b166e1cb2740

d=1,W=1 is an already covered baseline proof point; it is outside oldG but is NOT outside the old certified mathematical domain.

#### Native item 7

Native pointer: /joint_analysis/impact/6; canonical SHA-256: 4de7d9d89052e46c8cebe5339bdd3fcf736aa8d46cc1f77f0bf26ae9e15caf2b

#### Native field: argument

Native pointer: /joint_analysis/impact/6/argument; canonical SHA-256: 08cda29880ee77babd91694a71916943f88779b0a915e20c979574fbb79d5db4

Publish the previously derived 0<W<=1, fixed-nu Theta_nu(d) consequence as two native comparisons. Use the retained global upper and accepted affine dimension lower with their correct view/guarantee and constants. No new primary theorem or stronger gradient regularity is assumed. This revision addresses the preserved actual independent-review issues. Publication and typed projection obligations are explicit; every mathematical formula and adoption guard is verified against the exact native candidate, and historical effects are not reported as new frontier gains. Fresh revision addresses the preserved actual independent reviewer metadata issues with exact typed pending resource opportunities and honest closed/open publication bookkeeping. Unproved mappings remain pending, distinct IDs remain distinct, and no source guard or native inequality is broadened.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/6/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/6/comparison_ids; canonical SHA-256: 8a1fcbbafb77805ac018106120c1fd98987059c702151f41e19d4e58a952364c

#### Native item 1

Native pointer: /joint_analysis/impact/6/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/6/comparison_ids/1; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/impact/6/comparison_ids/2; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 4

Native pointer: /joint_analysis/impact/6/comparison_ids/3; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/6/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/6/finding_id; canonical SHA-256: 3960cd89f54e3104783225b9535f19700b2bd62a5746fe0c10be87b07a59a311

curated_feedback_SO_ZO_E07_neighborhood_20261116_2f6e197d61

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/6/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/6/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/6/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/6/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/6/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/6/validity_region; canonical SHA-256: e0eb801b1c2812bfd4e58d2f70585d54d30539e3fd6c4dcee0d07d666671a4f0

D: d integer >=1; 0<nu<1; H_nu,R,tau,epsilon>0; W=H_nu R^(1+nu)/epsilon. For each fixed nu, q1 is the native minimax fixed-path scalar-value cost for its view's g1 guarantee.

#### Native field: witness

Native pointer: /joint_analysis/impact/6/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: ef5cdf599b4f1676c07a0020087e045ef2bd7c39e22d61c7fcf81a6ffc20d099

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: d8f965f6c4d9a284be1d24cf394a62e4e234e70948b88e7fb554587053180cc1

Smoothing/regularization, buffer-safe queries and a fixed-cap guarantee conversion for arXiv:2407.09190v1 have not been proved; no upper transfer is adopted.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 072fc108f68a45c05f95ca3241bc970e9522ae86370ceebbd721ff939806decd

Fine-accuracy low/intermediate-dimension saturation branches outside the registered guard have not been assembled.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 4bda48fa92fe9f50a41e903f5016d88a8c51e70b305ee4bf0825cddc8547f321

The preceding actual fresh reviewer read parts of the primary sources, including Nesterov Theorem 3 and Diakonikolas-Guzman Theorem 12/Appendix C.2, but did not complete fresh standalone recertification of the historical finite-difference-to-inexact-accelerated-model upper transfer or exterior-query/unqueried-output lower transfer. Using the declared existing-Atlas baseline as a conditional maintenance premise does not mean those old source chains were freshly reverified. Keep these targeted recertification tasks explicit; suspend affected retention if actual counterevidence is found. This note claims no new source-read credit, theorem adoption, or completed verification.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: f2c879a3424bab36266ee5079a8c689423c92ced588543f6b8202a1b4fa68ffc

Assess the guard-preserving deterministic q2 b1 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 8b8683ea81657b918647365c03abac3a0a7441211c611e2501d3bd644317f561

Assess the guard-preserving deterministic q2 b2 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 6d5023bd7d33c4d6bc2d75f105222e2eb2d7399fc526cbaf823bfbf017296ddb

Assess the guard-preserving randomized q2 b1 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native item 7

Native pointer: /joint_analysis/pending_obligations/6; canonical SHA-256: 5188db387db78b439114c7dd01bf62521c204d2b7afc2876bb0a135fcf00197d

Assess the guard-preserving randomized q2 b2 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native item 8

Native pointer: /joint_analysis/pending_obligations/7; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 8b4b848503cf17850444f1a2ea63a7705dfa049ec2856aa676814d57956fbdb5

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: fdf21052a77d2d6f6510d1fc3d72ee6fbcc3dd1a397b132ef4a3545fcc4ff48a

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: d754c71e5e50ff3e695c0ac14a1e41414c2f86de8f09641ffe43d4cffc5e3f4a

SO_ZO_E07_neighborhood__deterministic__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 23935e84ee30f8d10f50aaec3fe459c773c9f32d38ae02c0c7f662eb7db9b72c

Unchanged native view/g1/q1/scalar-value contract and original guard.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 9d6caff56a6ef6899529e2370cc1e6ef7a9320f94cdf118a1ff09095bf4cac7d

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 61282c34a37473e0dfd1f0cd03eb4246634786cfdf9ee81dcecf655819bab2fd

Finite-difference/inexact accelerated-model premises in ZO_PROOF_HOLDER.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 88996cc194392014897d8e6e703e450474da175a29e04ab297bc1102b4c7b7f5

Accepted /bounds and /proofs/0 (ZO_PROOF_HOLDER); not freshly recertified.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 9266f6c8ee956db730f537ce9b1c422ac833f41d9444814fc82174651676a644

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 5446f485e7a1cd19c193ce23539918bf50e1b3028a573c3e589ccd63e4d5146e

SO_SRC_c39da60c875a03f8

#### Native item 2

Native pointer: /joint_analysis/provenance/0/source_refs/1; canonical SHA-256: d71eaf50b02cec1af0acc335c696c3e23d237df6af6766c1d2eb519789aa8894

SO_SRC_8cf103dfaaf94469

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 0a9cb162bd0b98a531992227c4c01aafc6960c67ab07760c719da92b24864232

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: bf476e989586d32a2ce02d9632836c92882a871d13a30b0de179a23df4977f99

SO_ZO_E07_neighborhood__deterministic__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 23935e84ee30f8d10f50aaec3fe459c773c9f32d38ae02c0c7f662eb7db9b72c

Unchanged native view/g1/q1/scalar-value contract and original guard.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 9d6caff56a6ef6899529e2370cc1e6ef7a9320f94cdf118a1ff09095bf4cac7d

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 6d8246448e973a8e5f0b55a940aa5e0b179844a4f81ae88e9ac680ae9cef8b3d

Theorem 12 specialization and shielding/output transfer in ZO_PROOF_HOLDER.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 88996cc194392014897d8e6e703e450474da175a29e04ab297bc1102b4c7b7f5

Accepted /bounds and /proofs/0 (ZO_PROOF_HOLDER); not freshly recertified.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: f9714ac9b3439ec8507313184f9b0a41ec08b98aebe3542f2d6f3af27333bc1d

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: d71eaf50b02cec1af0acc335c696c3e23d237df6af6766c1d2eb519789aa8894

SO_SRC_8cf103dfaaf94469

#### Native item 2

Native pointer: /joint_analysis/provenance/1/source_refs/1; canonical SHA-256: 5446f485e7a1cd19c193ce23539918bf50e1b3028a573c3e589ccd63e4d5146e

SO_SRC_c39da60c875a03f8

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: aefdde364f142a4c9dfc5e64a219313b4fa98977234c6c89a240ba908409d811

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 6ab631db2880106e77c61285acd88f191c50d5e4a5ccd4cf96ccdeecfc6be23c

SO_ZO_E07_neighborhood__deterministic__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 665edee9644ed9d25b0ad667f3fb880b7b6ad58d148aebaf9088ebce8c8a1a64

Affine seminorm zero gives subclass inclusion; native queries, outputs, per-instance guarantee and fixed scalar caps are preserved. The random prior is seed-independent.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: ede9164e34fb157c4f3376d7721f7e47b8b07e22a23dc384c0fd8f471be26298

subclass_transfer

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 10b0e6ebe4bbd0dfe88819bd13420698617edbd8e968f5324f9a29693900529b

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 7d4f1029db044951f0a9b42b06fd65e78e3539000eef8266adc6c8e822275b95

ZO_PROOF_AFFINE_DIMENSION

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 95ef582e40372e8f2ba5c44b8c018cebaa45b40da8c30539f0e109e82199659e

Globally affine functions with unbounded slope.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: dbe51ff3b1fea2d03a0269b74fde1786be3f076faa73a4381124758a71bce2fb

ZO_PROOF_AFFINE_DIMENSION, parts I-II and IV.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 7df4c1fb7ec15b4064d6b564457c94b9a54d860d2fe52607c99deaad1f017a6a

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: a5e70eabcc3a730664047de954dd6f60e79d434558ebb02f417abb92792009a7

SO_ZO_E07_neighborhood__randomized__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 23935e84ee30f8d10f50aaec3fe459c773c9f32d38ae02c0c7f662eb7db9b72c

Unchanged native view/g1/q1/scalar-value contract and original guard.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 9d6caff56a6ef6899529e2370cc1e6ef7a9320f94cdf118a1ff09095bf4cac7d

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 61282c34a37473e0dfd1f0cd03eb4246634786cfdf9ee81dcecf655819bab2fd

Finite-difference/inexact accelerated-model premises in ZO_PROOF_HOLDER.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 88996cc194392014897d8e6e703e450474da175a29e04ab297bc1102b4c7b7f5

Accepted /bounds and /proofs/0 (ZO_PROOF_HOLDER); not freshly recertified.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 9266f6c8ee956db730f537ce9b1c422ac833f41d9444814fc82174651676a644

#### Native item 1

Native pointer: /joint_analysis/provenance/3/source_refs/0; canonical SHA-256: 5446f485e7a1cd19c193ce23539918bf50e1b3028a573c3e589ccd63e4d5146e

SO_SRC_c39da60c875a03f8

#### Native item 2

Native pointer: /joint_analysis/provenance/3/source_refs/1; canonical SHA-256: d71eaf50b02cec1af0acc335c696c3e23d237df6af6766c1d2eb519789aa8894

SO_SRC_8cf103dfaaf94469

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 22aeb1d4c9bb08d03b878cb63a7f97dcba6fa434da301f112d74c306e6e65929

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: 3f8872ec1292ea4554c8c22a721503f2a266232663d7ab853bc542e7fd5d93e9

SO_ZO_E07_neighborhood__randomized__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: 23935e84ee30f8d10f50aaec3fe459c773c9f32d38ae02c0c7f662eb7db9b72c

Unchanged native view/g1/q1/scalar-value contract and original guard.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 9d6caff56a6ef6899529e2370cc1e6ef7a9320f94cdf118a1ff09095bf4cac7d

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 6d8246448e973a8e5f0b55a940aa5e0b179844a4f81ae88e9ac680ae9cef8b3d

Theorem 12 specialization and shielding/output transfer in ZO_PROOF_HOLDER.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: 88996cc194392014897d8e6e703e450474da175a29e04ab297bc1102b4c7b7f5

Accepted /bounds and /proofs/0 (ZO_PROOF_HOLDER); not freshly recertified.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: f9714ac9b3439ec8507313184f9b0a41ec08b98aebe3542f2d6f3af27333bc1d

#### Native item 1

Native pointer: /joint_analysis/provenance/4/source_refs/0; canonical SHA-256: d71eaf50b02cec1af0acc335c696c3e23d237df6af6766c1d2eb519789aa8894

SO_SRC_8cf103dfaaf94469

#### Native item 2

Native pointer: /joint_analysis/provenance/4/source_refs/1; canonical SHA-256: 5446f485e7a1cd19c193ce23539918bf50e1b3028a573c3e589ccd63e4d5146e

SO_SRC_c39da60c875a03f8

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 1a5487026c976e6b5b9d31a84caafc7dd53f24969d4a48836dc904afad023c85

D intersect G

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: 0611d321f4f2ff3124bf3cb8a0438fba93576ae8181b73a4d902a053481f9d91

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: 7f1dbab3e9f430813219675b5655627b86f81863fdc6654493101f1cc6ff5fd8

SO_ZO_E07_neighborhood__randomized__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 665edee9644ed9d25b0ad667f3fb880b7b6ad58d148aebaf9088ebce8c8a1a64

Affine seminorm zero gives subclass inclusion; native queries, outputs, per-instance guarantee and fixed scalar caps are preserved. The random prior is seed-independent.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: ede9164e34fb157c4f3376d7721f7e47b8b07e22a23dc384c0fd8f471be26298

subclass_transfer

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 10b0e6ebe4bbd0dfe88819bd13420698617edbd8e968f5324f9a29693900529b

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: 7d4f1029db044951f0a9b42b06fd65e78e3539000eef8266adc6c8e822275b95

ZO_PROOF_AFFINE_DIMENSION

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: 95ef582e40372e8f2ba5c44b8c018cebaa45b40da8c30539f0e109e82199659e

Globally affine functions with unbounded slope.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: e807eb4cdbef6eae28c164faa29f1697da963224995a0e2a1b16b56a1c345bc2

ZO_PROOF_AFFINE_DIMENSION, parts I, III-IV.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 49ff144b5b3c09edc3d893fe03e0c82bfec3fa8578d6d4037e6a5264450a34c0

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 618699d6159ec639c5a0a07453f9b8fc17686fa80e4dcd1f2c51907d0b08bb16

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: fa5e390ece55c6b8e51ee91f48b354c5e9ac4ff51b7bb79b305cd73e7af0a2bc

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: 8c42041c3d721fd9a7c249e43a89935601f6430ba09523a58b00f260883449ec

User-feedback-guided curator synthesis plus the explicitly recorded new primary-source reads. Previous partial searches and retained-source recertification limits persist; neither a new exhaustive search nor a completed native approval is claimed.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 73a733f1a0484d4584406ba86e90322bc2bd49e0b57e5c257141f12f28ae757d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 5a92b05309f83680f4d44d3ff5570d1aa064b0323cde40402666737ba1475e53

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: eee3cf1eedf1a409e1ddd714c3ce27b555f2aca8dfc9fd3b49a7dc476335e1b7

Global q1 b3 and b5 apply on the full coarse region; the original b4 lower is retained only on G. On W<=1 it is order-dominated by affine d, so no guard extension is needed. On old comparisons retain the guarded envelope; q2 identities are never silently merged. Under the explicitly conditional retained premises, coarse closure is natively published for both views. SO_ZO_E07_neighborhood__deterministic__b3: included — Conditional baseline retention; W>=W_{0,nu}>0 absorbs the additive one.; SO_ZO_E07_neighborhood__deterministic__b4: included — Retained guarded precision lower in the maximum; asymptotically redundant to the new dimension term on G.; SO_ZO_E07_neighborhood__deterministic__b5: included — Exact d+1 affine lower, with all adaptive queries and unqueried outputs covered.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 4ca2fdba93dd2a03c508d4ca6f2e6f0d1c379f313dfd8300e61bf9126e3b953d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: d754c71e5e50ff3e695c0ac14a1e41414c2f86de8f09641ffe43d4cffc5e3f4a

SO_ZO_E07_neighborhood__deterministic__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: bf476e989586d32a2ce02d9632836c92882a871d13a30b0de179a23df4977f99

SO_ZO_E07_neighborhood__deterministic__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 6ab631db2880106e77c61285acd88f191c50d5e4a5ccd4cf96ccdeecfc6be23c

SO_ZO_E07_neighborhood__deterministic__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: d10a76b2b4ec939af41bc1acddfe7c19d8249442c4a48660d60664613098653e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 24a16b4fdd23b2a0d9b6429d8c9f229e303e63a1feeb1b779a6c9b357e762fc1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/1; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/2; canonical SHA-256: 7d4f1029db044951f0a9b42b06fd65e78e3539000eef8266adc6c8e822275b95

ZO_PROOF_AFFINE_DIMENSION

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 48cccacf93d4d9b0adb0fc0fe994f310fe934f79be119a2954193fc3c4a55ecd

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: 988fcd63f292382214c6b850f55802daa36b30c0e0f5f74c0f53462630676125

Global q1 b3 and b5 apply on the full coarse region; the original b4 lower is retained only on G. On W<=1 it is order-dominated by affine d, so no guard extension is needed. On old comparisons retain the guarded envelope; q2 identities are never silently merged. Under the explicitly conditional retained premises, coarse closure is natively published for both views. SO_ZO_E07_neighborhood__deterministic__b3: included — Same native q1; coarse bound follows from complete new publishing derivation.; SO_ZO_E07_neighborhood__deterministic__b4: dominated — Only valid on its original G overlap; W^p<=1<=d on the coarse region, so it adds no stronger order than the affine lower. Its original guard is unchanged.; SO_ZO_E07_neighborhood__deterministic__b5: included — Same native q1; coarse bound follows from complete new publishing derivation.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 4ca2fdba93dd2a03c508d4ca6f2e6f0d1c379f313dfd8300e61bf9126e3b953d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: d754c71e5e50ff3e695c0ac14a1e41414c2f86de8f09641ffe43d4cffc5e3f4a

SO_ZO_E07_neighborhood__deterministic__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: bf476e989586d32a2ce02d9632836c92882a871d13a30b0de179a23df4977f99

SO_ZO_E07_neighborhood__deterministic__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 6ab631db2880106e77c61285acd88f191c50d5e4a5ccd4cf96ccdeecfc6be23c

SO_ZO_E07_neighborhood__deterministic__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: bcda87c3d8e6b6dba4b289520b432c9604ca227084ce0a5637cf249146e051cd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 24a16b4fdd23b2a0d9b6429d8c9f229e303e63a1feeb1b779a6c9b357e762fc1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/1; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/2; canonical SHA-256: 7d4f1029db044951f0a9b42b06fd65e78e3539000eef8266adc6c8e822275b95

ZO_PROOF_AFFINE_DIMENSION

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: f86e74026b313db973d7686c6b51587bd74bdd8865fe97e5f6ac869ef6989cbd

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: 2aa08ac660e1303c876ccf2f2a50dad0ec68ea356c0ae366f4f67ace0ac336a5

Global q1 b3 and b5 apply on the full coarse region; the original b4 lower is retained only on G. On W<=1 it is order-dominated by affine d, so no guard extension is needed. On old comparisons retain the guarded envelope; q2 identities are never silently merged. Under the explicitly conditional retained premises, coarse closure is natively published for both views. SO_ZO_E07_neighborhood__randomized__b3: included — Conditional baseline retention; W>=W_{0,nu}>0 absorbs the additive one.; SO_ZO_E07_neighborhood__randomized__b4: included — Retained guarded precision lower in the maximum; asymptotically redundant to the new dimension term on G.; SO_ZO_E07_neighborhood__randomized__b5: included — Exact ceil(d/9) affine lower for private-random 2/3 success with fixed path cap.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 327b81f8b2ca52ed22e1cb247078ca8a17161e33b381d2f561d64620eda1d070

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: a5e70eabcc3a730664047de954dd6f60e79d434558ebb02f417abb92792009a7

SO_ZO_E07_neighborhood__randomized__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 3f8872ec1292ea4554c8c22a721503f2a266232663d7ab853bc542e7fd5d93e9

SO_ZO_E07_neighborhood__randomized__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 7f1dbab3e9f430813219675b5655627b86f81863fdc6654493101f1cc6ff5fd8

SO_ZO_E07_neighborhood__randomized__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: fcaf56f37af1d3e99dfaaec2caf23a14d79ca20c6c24040aa32e70fd67666255

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 24a16b4fdd23b2a0d9b6429d8c9f229e303e63a1feeb1b779a6c9b357e762fc1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/1; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/2; canonical SHA-256: 7d4f1029db044951f0a9b42b06fd65e78e3539000eef8266adc6c8e822275b95

ZO_PROOF_AFFINE_DIMENSION

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 771a1a54a1fc355193ac3cc650238cd61a22ded0e278f289c2d6eda9c955f75d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 512dcf899451a90e3db0a7357899db041205302f723d9396679b848d22c34b02

Global q1 b3 and b5 apply on the full coarse region; the original b4 lower is retained only on G. On W<=1 it is order-dominated by affine d, so no guard extension is needed. On old comparisons retain the guarded envelope; q2 identities are never silently merged. Under the explicitly conditional retained premises, coarse closure is natively published for both views. SO_ZO_E07_neighborhood__randomized__b3: included — Same native q1; coarse bound follows from complete new publishing derivation.; SO_ZO_E07_neighborhood__randomized__b4: dominated — Only valid on its original G overlap; W^p<=1<=d on the coarse region, so it adds no stronger order than the affine lower. Its original guard is unchanged.; SO_ZO_E07_neighborhood__randomized__b5: included — Same native q1; coarse bound follows from complete new publishing derivation.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 327b81f8b2ca52ed22e1cb247078ca8a17161e33b381d2f561d64620eda1d070

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: a5e70eabcc3a730664047de954dd6f60e79d434558ebb02f417abb92792009a7

SO_ZO_E07_neighborhood__randomized__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 3f8872ec1292ea4554c8c22a721503f2a266232663d7ab853bc542e7fd5d93e9

SO_ZO_E07_neighborhood__randomized__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: 7f1dbab3e9f430813219675b5655627b86f81863fdc6654493101f1cc6ff5fd8

SO_ZO_E07_neighborhood__randomized__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 45481c073b92eee7f6eeae1d2a278779c54ac0b7231c09b404b6b1645943d5a2

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 24a16b4fdd23b2a0d9b6429d8c9f229e303e63a1feeb1b779a6c9b357e762fc1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs/1; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs/2; canonical SHA-256: 7d4f1029db044951f0a9b42b06fd65e78e3539000eef8266adc6c8e822275b95

ZO_PROOF_AFFINE_DIMENSION

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 29fc5be6368de74502198e18583f86a217c936e01725a0fef621a472999eed93

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 8a1fcbbafb77805ac018106120c1fd98987059c702151f41e19d4e58a952364c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/2; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/3; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: d0167f548742ead3d895787ec442b4a84beeb280ebe70d01f9a7603611e9c56f

remaining-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: d8f965f6c4d9a284be1d24cf394a62e4e234e70948b88e7fb554587053180cc1

Smoothing/regularization, buffer-safe queries and a fixed-cap guarantee conversion for arXiv:2407.09190v1 have not been proved; no upper transfer is adopted.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: ff782b3b3b69874f2920545f3ac37673d9e68ddfdb5d20adff10868b7c2650ea

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 8a1fcbbafb77805ac018106120c1fd98987059c702151f41e19d4e58a952364c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/2; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/3; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: a4b3d9806c41184784f257b17680c859184105b903c13a4dc473b5d4a38646ea

remaining-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 072fc108f68a45c05f95ca3241bc970e9522ae86370ceebbd721ff939806decd

Fine-accuracy low/intermediate-dimension saturation branches outside the registered guard have not been assembled.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: dfed23d79264914c9d6cbb6dafca1f173d243e4b622b05c40a7343c8679ba487

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: b30123c9e7040fe42a147ccd95481d978826ef0912fbec87fad30d68126edbca

The CURRENT frozen native /quantities/0 and /quantities/2 already put parameter SO_ZO_E07_neighborhood_p_6290a52d96 in fixed_parameters and exclude it from tracked_parameters; both are unchanged in this candidate. Their exact canonical hashes are 51b05de8d8a8e0ae573478b47746828b88a2d983d2fe5ce9fcbc09c5eb7f5bce and fb3ad8d6809557267686a323b048448d3c54f50b399e14315754d4dbe1a6a61c. The target fixed alias is the literal native nu symbol and names that same parameter. The remaining five joint coordinates and derivedW are unchanged, with uniform_in covering everyjoint coordinate, and only fixednu allowed in hidden constants. Thus no current controlled metadata normalization is needed or proposed. Mark targetresolution resolved and remove stale active requests claiming that currentq1 tracksnu. The historical quantity_metadata_normalization_log is preserved byte-for-byte as data; it is evidence of the prior sequence, not a fresh operation or newread/approval credit. Retain all separate source-chain recertification and finer-accuracy obligations. Resolving this role annotation does not resolve literature or recertify historical source premises, alter a minimax task, mergeq2/q1, or add a new rate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 8a1fcbbafb77805ac018106120c1fd98987059c702151f41e19d4e58a952364c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/2; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/3; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 3e14526e35b394fe370a6fc3dd84e97e336771629d764f97e1112f9be119d23a

remaining-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 71f420b00a1b3a7aa039639cee0b412144ef178a484d0515f41f6c486c74b115

Independently review the supplied q1 metadata normalizations before adopting the joint-role annotation.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 0810f730354b22f01b2c4e108c67075792ef43cc19757001e4176d9acf4aeb8d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs/0; canonical SHA-256: 9ab091c1d78f7d7c967502398efbac60f13fad324b47d3808a793efe3c194707

ZO_PROOF_HOLDER_ROLE_RECONCILIATION_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs/1; canonical SHA-256: a9c08f7cfe80adc9241eb717f583c58f5933b28b462df58935be4a145f138378

ZO_PROOF_HOLDER

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 2c396dfcb003dc7b0b59be7345fe45cafbf6df4cf663a1d7916ed0958feda6a4

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 8a1fcbbafb77805ac018106120c1fd98987059c702151f41e19d4e58a952364c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/2; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/3; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 2ad76a816cfedf1ea354b21e9948710836a980becdf5124dd84ab11a1a2b3afe

remaining-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 4bda48fa92fe9f50a41e903f5016d88a8c51e70b305ee4bf0825cddc8547f321

The preceding actual fresh reviewer read parts of the primary sources, including Nesterov Theorem 3 and Diakonikolas-Guzman Theorem 12/Appendix C.2, but did not complete fresh standalone recertification of the historical finite-difference-to-inexact-accelerated-model upper transfer or exterior-query/unqueried-output lower transfer. Using the declared existing-Atlas baseline as a conditional maintenance premise does not mean those old source chains were freshly reverified. Keep these targeted recertification tasks explicit; suspend affected retention if actual counterevidence is found. This note claims no new source-read credit, theorem adoption, or completed verification.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: f41984036099008b9bd4986b65af26c5ec342d5822ea6b8fa507a55797e96cc7

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: ddc3ea12a4bee8e4c2ec67e9e473d7d7370143c06a8335ccc7da974a5581190d

Explicit native source SO_ZO_E07_neighborhood__deterministic__b1 and targetsame-view q1 comparison IDs SO_ZO_E07_neighborhood__deterministic__c1,SO_ZO_E07_neighborhood__deterministic__c2. Literal ID differences do not prove mathematical incomparability, but do forbid automatic inclusion. Retain EXACT bound validity: ($W=H_\nu R^{1+\nu}/\varepsilon\ge1$. This is a constructive upper bound, without a claim of zeroth-order optimality. The gradient approximation error is controlled by $h^\nu$.). This is an upper on W>=1; the coarsec2 region0<W<=1 can overlap this guard onlyatW1, never allW<1. Check finite-difference displacements/buffer, actual scalar-query cost and fixed-path success mapping before a quantity-matched q1 bound could be published. The currentq1 globalb3/affineb5 and guardedb4 already account for their recorded orders; any newly justified consequence must be compared with that envelope. No new inequality, source verification, main-rate gain or identity merge is claimed. Existing direct-row dispositions are not a completed judgment of the mathematical transfer; this typed pending row explicitly retains that assessment and its possible gap effect.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 6148231ebc71399732144d2306fb6fc72a359f98ec4046a0221d433ef65d9cac

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/0; canonical SHA-256: 5829a28477ba6822c9d6ccd2025a6e5261969490536cdff085f41e992c77848d

SO_ZO_E07_neighborhood__deterministic__b1

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 0708b99923f11db7fc1f128355e85398ba6c3e1801f19d4617d140dec59753fb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids/0; canonical SHA-256: 6a3c46de0ad7db0b193ddab1c47ff1d41478232c259776afbd3b1d2fa3c5e347

fine_G

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids/1; canonical SHA-256: c7e3f1600ab9063214a79c5b8401577c50b5aa037065c01d9749ade107d0c5e9

fine_not_G

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids/2; canonical SHA-256: 2117a83ad8116727ac02f1aa241104512467811b74e7f71c0fdebc66c5bb554b

coarse_G

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids/3; canonical SHA-256: 80a81811c16e7d0ae0bdc7ac3d2676a23e4652940240ccb1671b0dc095d29829

coarse_not_G

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: b25d75a9f0af6205d84eec608b63e0b8ca920457036ec6bf84b446ea97d17996

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: b4cd0f90c451d15d6f4cb2fd7cd2e0fd19f1a414cc3c7d2409d2653c307cdaef

historical-q2-deterministic-b1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: f2c879a3424bab36266ee5079a8c689423c92ced588543f6b8202a1b4fa68ffc

Assess the guard-preserving deterministic q2 b1 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: b77a3536c485a2b0598010228286f8b6c050794a4393c0cef579d930b6d463af

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: ddc3ea12a4bee8e4c2ec67e9e473d7d7370143c06a8335ccc7da974a5581190d

Explicit native source SO_ZO_E07_neighborhood__deterministic__b1 and targetsame-view q1 comparison IDs SO_ZO_E07_neighborhood__deterministic__c1,SO_ZO_E07_neighborhood__deterministic__c2. Literal ID differences do not prove mathematical incomparability, but do forbid automatic inclusion. Retain EXACT bound validity: ($W=H_\nu R^{1+\nu}/\varepsilon\ge1$. This is a constructive upper bound, without a claim of zeroth-order optimality. The gradient approximation error is controlled by $h^\nu$.). This is an upper on W>=1; the coarsec2 region0<W<=1 can overlap this guard onlyatW1, never allW<1. Check finite-difference displacements/buffer, actual scalar-query cost and fixed-path success mapping before a quantity-matched q1 bound could be published. The currentq1 globalb3/affineb5 and guardedb4 already account for their recorded orders; any newly justified consequence must be compared with that envelope. No new inequality, source verification, main-rate gain or identity merge is claimed. Existing direct-row dispositions are not a completed judgment of the mathematical transfer; this typed pending row explicitly retains that assessment and its possible gap effect.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 6148231ebc71399732144d2306fb6fc72a359f98ec4046a0221d433ef65d9cac

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/0; canonical SHA-256: 5829a28477ba6822c9d6ccd2025a6e5261969490536cdff085f41e992c77848d

SO_ZO_E07_neighborhood__deterministic__b1

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 0708b99923f11db7fc1f128355e85398ba6c3e1801f19d4617d140dec59753fb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids/0; canonical SHA-256: 6a3c46de0ad7db0b193ddab1c47ff1d41478232c259776afbd3b1d2fa3c5e347

fine_G

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids/1; canonical SHA-256: c7e3f1600ab9063214a79c5b8401577c50b5aa037065c01d9749ade107d0c5e9

fine_not_G

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids/2; canonical SHA-256: 2117a83ad8116727ac02f1aa241104512467811b74e7f71c0fdebc66c5bb554b

coarse_G

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids/3; canonical SHA-256: 80a81811c16e7d0ae0bdc7ac3d2676a23e4652940240ccb1671b0dc095d29829

coarse_not_G

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: b25d75a9f0af6205d84eec608b63e0b8ca920457036ec6bf84b446ea97d17996

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: 3026e4a1618407349afa3bd9b11804e64d0f2c27d70e7932f23675dea1d1c331

historical-q2-deterministic-b1-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: f2c879a3424bab36266ee5079a8c689423c92ced588543f6b8202a1b4fa68ffc

Assess the guard-preserving deterministic q2 b1 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: a5e273415762e8feb327e06798a4496cc6082b957ae209300dcb314267b7a151

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: 4bba7c2ee2e86df62930113587e3ec701f848fc3f20ee413061f4f8d9cf8f89e

Explicit native source SO_ZO_E07_neighborhood__deterministic__b2 and targetsame-view q1 comparison IDs SO_ZO_E07_neighborhood__deterministic__c1,SO_ZO_E07_neighborhood__deterministic__c2. Literal ID differences do not prove mathematical incomparability, but do forbid automatic inclusion. Retain EXACT bound validity: (Fix $0<\nu<1$ and take sufficiently small accuracy in the source's high-dimensional window. The lower bound holds first for a stronger local first-order interface, and therefore also for exact scalar-value algorithms.). This lower requires fixednu, sufficiently small source accuracy and its original high-dimensional conditions. Do not replace those conditions by the whole coarsec2 region, by a universal numeric threshold, or by any parent native domain. A legal reduction/quantity map must be proved before adoption. The currentq1 globalb3/affineb5 and guardedb4 already account for their recorded orders; any newly justified consequence must be compared with that envelope. No new inequality, source verification, main-rate gain or identity merge is claimed. Existing direct-row dispositions are not a completed judgment of the mathematical transfer; this typed pending row explicitly retains that assessment and its possible gap effect.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: 26fefd1ba151b7fd4924eb9f551672de05398c7f2d0879cedb2a5e0db052813a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/0; canonical SHA-256: 4382cda97485f4a0d75a3a07c52ffbdfc76baca25bc6860e2aac0e7b5d37c23e

SO_ZO_E07_neighborhood__deterministic__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 0708b99923f11db7fc1f128355e85398ba6c3e1801f19d4617d140dec59753fb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids/0; canonical SHA-256: 6a3c46de0ad7db0b193ddab1c47ff1d41478232c259776afbd3b1d2fa3c5e347

fine_G

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids/1; canonical SHA-256: c7e3f1600ab9063214a79c5b8401577c50b5aa037065c01d9749ade107d0c5e9

fine_not_G

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids/2; canonical SHA-256: 2117a83ad8116727ac02f1aa241104512467811b74e7f71c0fdebc66c5bb554b

coarse_G

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids/3; canonical SHA-256: 80a81811c16e7d0ae0bdc7ac3d2676a23e4652940240ccb1671b0dc095d29829

coarse_not_G

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: b25d75a9f0af6205d84eec608b63e0b8ca920457036ec6bf84b446ea97d17996

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/1; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 4d084cb6be4a8fcfd3eaf1a04ea5b40d61eba18531c0c6de07dd681bd987a7ca

historical-q2-deterministic-b2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 8b8683ea81657b918647365c03abac3a0a7441211c611e2501d3bd644317f561

Assess the guard-preserving deterministic q2 b2 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: 2c9a5c55648aee18c1be901330ea3439bbefec20c4fcf8fbcb1dc730c1d27376

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: 4bba7c2ee2e86df62930113587e3ec701f848fc3f20ee413061f4f8d9cf8f89e

Explicit native source SO_ZO_E07_neighborhood__deterministic__b2 and targetsame-view q1 comparison IDs SO_ZO_E07_neighborhood__deterministic__c1,SO_ZO_E07_neighborhood__deterministic__c2. Literal ID differences do not prove mathematical incomparability, but do forbid automatic inclusion. Retain EXACT bound validity: (Fix $0<\nu<1$ and take sufficiently small accuracy in the source's high-dimensional window. The lower bound holds first for a stronger local first-order interface, and therefore also for exact scalar-value algorithms.). This lower requires fixednu, sufficiently small source accuracy and its original high-dimensional conditions. Do not replace those conditions by the whole coarsec2 region, by a universal numeric threshold, or by any parent native domain. A legal reduction/quantity map must be proved before adoption. The currentq1 globalb3/affineb5 and guardedb4 already account for their recorded orders; any newly justified consequence must be compared with that envelope. No new inequality, source verification, main-rate gain or identity merge is claimed. Existing direct-row dispositions are not a completed judgment of the mathematical transfer; this typed pending row explicitly retains that assessment and its possible gap effect.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: 26fefd1ba151b7fd4924eb9f551672de05398c7f2d0879cedb2a5e0db052813a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs/0; canonical SHA-256: 4382cda97485f4a0d75a3a07c52ffbdfc76baca25bc6860e2aac0e7b5d37c23e

SO_ZO_E07_neighborhood__deterministic__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 0708b99923f11db7fc1f128355e85398ba6c3e1801f19d4617d140dec59753fb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids/0; canonical SHA-256: 6a3c46de0ad7db0b193ddab1c47ff1d41478232c259776afbd3b1d2fa3c5e347

fine_G

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids/1; canonical SHA-256: c7e3f1600ab9063214a79c5b8401577c50b5aa037065c01d9749ade107d0c5e9

fine_not_G

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids/2; canonical SHA-256: 2117a83ad8116727ac02f1aa241104512467811b74e7f71c0fdebc66c5bb554b

coarse_G

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids/3; canonical SHA-256: 80a81811c16e7d0ae0bdc7ac3d2676a23e4652940240ccb1671b0dc095d29829

coarse_not_G

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: b25d75a9f0af6205d84eec608b63e0b8ca920457036ec6bf84b446ea97d17996

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/1; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: f2bc12f809eb09c9905b16d5adb8812f13a39e1294a7c121b2598224ed6f04f6

historical-q2-deterministic-b2-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: 8b8683ea81657b918647365c03abac3a0a7441211c611e2501d3bd644317f561

Assess the guard-preserving deterministic q2 b2 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/obligations/12; canonical SHA-256: 6c37f7629fc9e87fc73e911f772616d5199aa6379ddc6ed7a42c03b07c91c6dd

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/argument; canonical SHA-256: 30edb05e71f390f611ab41166f20cbbf35bc8d6a0dbd3e2904711f9a38cafaf1

Explicit native source SO_ZO_E07_neighborhood__randomized__b1 and targetsame-view q1 comparison IDs SO_ZO_E07_neighborhood__randomized__c1,SO_ZO_E07_neighborhood__randomized__c2. Literal ID differences do not prove mathematical incomparability, but do forbid automatic inclusion. Retain EXACT bound validity: ($W=H_\nu R^{1+\nu}/\varepsilon\ge1$. This is a constructive upper bound, without a claim of zeroth-order optimality. The gradient approximation error is controlled by $h^\nu$.). This is an upper on W>=1; the coarsec2 region0<W<=1 can overlap this guard onlyatW1, never allW<1. Check finite-difference displacements/buffer, actual scalar-query cost and fixed-path success mapping before a quantity-matched q1 bound could be published. The currentq1 globalb3/affineb5 and guardedb4 already account for their recorded orders; any newly justified consequence must be compared with that envelope. No new inequality, source verification, main-rate gain or identity merge is claimed. Existing direct-row dispositions are not a completed judgment of the mathematical transfer; this typed pending row explicitly retains that assessment and its possible gap effect.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs; canonical SHA-256: 1d3070bc066b13ec2eeeea5a547d6f0d4b83483ca0b47ccbcb81b05774563850

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs/0; canonical SHA-256: baede674fd0ae9d16becd2d17461249459b01b26ae3cef4573696dcc4a1d5c47

SO_ZO_E07_neighborhood__randomized__b1

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids; canonical SHA-256: 0708b99923f11db7fc1f128355e85398ba6c3e1801f19d4617d140dec59753fb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids/0; canonical SHA-256: 6a3c46de0ad7db0b193ddab1c47ff1d41478232c259776afbd3b1d2fa3c5e347

fine_G

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids/1; canonical SHA-256: c7e3f1600ab9063214a79c5b8401577c50b5aa037065c01d9749ade107d0c5e9

fine_not_G

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids/2; canonical SHA-256: 2117a83ad8116727ac02f1aa241104512467811b74e7f71c0fdebc66c5bb554b

coarse_G

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids/3; canonical SHA-256: 80a81811c16e7d0ae0bdc7ac3d2676a23e4652940240ccb1671b0dc095d29829

coarse_not_G

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids; canonical SHA-256: 1f26789f455620bfd27a2534b9cd00c48b9f47468828149ce4905cdaa8ae4c1a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/0; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/1; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/id; canonical SHA-256: 7ea9af843d92366a17937c505b3a8d636adf08b74acfafdb0fa0344fac494b64

historical-q2-randomized-b1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/lead; canonical SHA-256: 6d5023bd7d33c4d6bc2d75f105222e2eb2d7399fc526cbaf823bfbf017296ddb

Assess the guard-preserving randomized q2 b1 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 14

Native pointer: /joint_analysis/synthesis_coverage/obligations/13; canonical SHA-256: c9ff340444428b6e8c180039401ce399438094c5bfec211a606e7fb6f5b67123

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/argument; canonical SHA-256: 30edb05e71f390f611ab41166f20cbbf35bc8d6a0dbd3e2904711f9a38cafaf1

Explicit native source SO_ZO_E07_neighborhood__randomized__b1 and targetsame-view q1 comparison IDs SO_ZO_E07_neighborhood__randomized__c1,SO_ZO_E07_neighborhood__randomized__c2. Literal ID differences do not prove mathematical incomparability, but do forbid automatic inclusion. Retain EXACT bound validity: ($W=H_\nu R^{1+\nu}/\varepsilon\ge1$. This is a constructive upper bound, without a claim of zeroth-order optimality. The gradient approximation error is controlled by $h^\nu$.). This is an upper on W>=1; the coarsec2 region0<W<=1 can overlap this guard onlyatW1, never allW<1. Check finite-difference displacements/buffer, actual scalar-query cost and fixed-path success mapping before a quantity-matched q1 bound could be published. The currentq1 globalb3/affineb5 and guardedb4 already account for their recorded orders; any newly justified consequence must be compared with that envelope. No new inequality, source verification, main-rate gain or identity merge is claimed. Existing direct-row dispositions are not a completed judgment of the mathematical transfer; this typed pending row explicitly retains that assessment and its possible gap effect.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs; canonical SHA-256: 1d3070bc066b13ec2eeeea5a547d6f0d4b83483ca0b47ccbcb81b05774563850

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/0; canonical SHA-256: baede674fd0ae9d16becd2d17461249459b01b26ae3cef4573696dcc4a1d5c47

SO_ZO_E07_neighborhood__randomized__b1

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids; canonical SHA-256: 0708b99923f11db7fc1f128355e85398ba6c3e1801f19d4617d140dec59753fb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids/0; canonical SHA-256: 6a3c46de0ad7db0b193ddab1c47ff1d41478232c259776afbd3b1d2fa3c5e347

fine_G

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids/1; canonical SHA-256: c7e3f1600ab9063214a79c5b8401577c50b5aa037065c01d9749ade107d0c5e9

fine_not_G

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids/2; canonical SHA-256: 2117a83ad8116727ac02f1aa241104512467811b74e7f71c0fdebc66c5bb554b

coarse_G

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids/3; canonical SHA-256: 80a81811c16e7d0ae0bdc7ac3d2676a23e4652940240ccb1671b0dc095d29829

coarse_not_G

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids; canonical SHA-256: 1f26789f455620bfd27a2534b9cd00c48b9f47468828149ce4905cdaa8ae4c1a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/0; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/1; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/id; canonical SHA-256: 68f1457d315e3a9d692429e164514843c6b80656f4e5dc6ef4b05b33d3459bc7

historical-q2-randomized-b1-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/lead; canonical SHA-256: 6d5023bd7d33c4d6bc2d75f105222e2eb2d7399fc526cbaf823bfbf017296ddb

Assess the guard-preserving randomized q2 b1 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 15

Native pointer: /joint_analysis/synthesis_coverage/obligations/14; canonical SHA-256: e67d0883a02a3b94b0980a34e6cb8bff3b9ef4b863dee2d50ff2df1bebe5149f

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/argument; canonical SHA-256: 4219d246e38649bf9b75b18594ea1d6d48e8702ea7daca25310a61098cd8510d

Explicit native source SO_ZO_E07_neighborhood__randomized__b2 and targetsame-view q1 comparison IDs SO_ZO_E07_neighborhood__randomized__c1,SO_ZO_E07_neighborhood__randomized__c2. Literal ID differences do not prove mathematical incomparability, but do forbid automatic inclusion. Retain EXACT bound validity: (Fix $0<\nu<1$ and take sufficiently small accuracy in the source's high-dimensional window. The lower bound holds first for a stronger local first-order interface, and therefore also for exact scalar-value algorithms.). This lower requires fixednu, sufficiently small source accuracy and its original high-dimensional conditions. Do not replace those conditions by the whole coarsec2 region, by a universal numeric threshold, or by any parent native domain. A legal reduction/quantity map must be proved before adoption. The currentq1 globalb3/affineb5 and guardedb4 already account for their recorded orders; any newly justified consequence must be compared with that envelope. No new inequality, source verification, main-rate gain or identity merge is claimed. Existing direct-row dispositions are not a completed judgment of the mathematical transfer; this typed pending row explicitly retains that assessment and its possible gap effect.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs; canonical SHA-256: e5122f9171b993e19f3bf7b3328b60ff43bdb63048f7dc6e6ad2c88fd1cc6c78

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs/0; canonical SHA-256: e1342d64304ea0d85884a307dc813d8447bc8349365fb5457258df5c9c01372c

SO_ZO_E07_neighborhood__randomized__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids; canonical SHA-256: 0708b99923f11db7fc1f128355e85398ba6c3e1801f19d4617d140dec59753fb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids/0; canonical SHA-256: 6a3c46de0ad7db0b193ddab1c47ff1d41478232c259776afbd3b1d2fa3c5e347

fine_G

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids/1; canonical SHA-256: c7e3f1600ab9063214a79c5b8401577c50b5aa037065c01d9749ade107d0c5e9

fine_not_G

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids/2; canonical SHA-256: 2117a83ad8116727ac02f1aa241104512467811b74e7f71c0fdebc66c5bb554b

coarse_G

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids/3; canonical SHA-256: 80a81811c16e7d0ae0bdc7ac3d2676a23e4652940240ccb1671b0dc095d29829

coarse_not_G

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids; canonical SHA-256: 1f26789f455620bfd27a2534b9cd00c48b9f47468828149ce4905cdaa8ae4c1a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/0; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/1; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/id; canonical SHA-256: 2d2cd4a179db6a94fbde91edcc7740477bb1aa135a981fd321bd26a9fb9a8117

historical-q2-randomized-b2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/lead; canonical SHA-256: 5188db387db78b439114c7dd01bf62521c204d2b7afc2876bb0a135fcf00197d

Assess the guard-preserving randomized q2 b2 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 16

Native pointer: /joint_analysis/synthesis_coverage/obligations/15; canonical SHA-256: cd707e426a0b0e32f7259fc137be4e5f1ca78a4fdb836853de274ab6ce81d9a8

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/argument; canonical SHA-256: 4219d246e38649bf9b75b18594ea1d6d48e8702ea7daca25310a61098cd8510d

Explicit native source SO_ZO_E07_neighborhood__randomized__b2 and targetsame-view q1 comparison IDs SO_ZO_E07_neighborhood__randomized__c1,SO_ZO_E07_neighborhood__randomized__c2. Literal ID differences do not prove mathematical incomparability, but do forbid automatic inclusion. Retain EXACT bound validity: (Fix $0<\nu<1$ and take sufficiently small accuracy in the source's high-dimensional window. The lower bound holds first for a stronger local first-order interface, and therefore also for exact scalar-value algorithms.). This lower requires fixednu, sufficiently small source accuracy and its original high-dimensional conditions. Do not replace those conditions by the whole coarsec2 region, by a universal numeric threshold, or by any parent native domain. A legal reduction/quantity map must be proved before adoption. The currentq1 globalb3/affineb5 and guardedb4 already account for their recorded orders; any newly justified consequence must be compared with that envelope. No new inequality, source verification, main-rate gain or identity merge is claimed. Existing direct-row dispositions are not a completed judgment of the mathematical transfer; this typed pending row explicitly retains that assessment and its possible gap effect.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs; canonical SHA-256: e5122f9171b993e19f3bf7b3328b60ff43bdb63048f7dc6e6ad2c88fd1cc6c78

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs/0; canonical SHA-256: e1342d64304ea0d85884a307dc813d8447bc8349365fb5457258df5c9c01372c

SO_ZO_E07_neighborhood__randomized__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids; canonical SHA-256: 0708b99923f11db7fc1f128355e85398ba6c3e1801f19d4617d140dec59753fb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids/0; canonical SHA-256: 6a3c46de0ad7db0b193ddab1c47ff1d41478232c259776afbd3b1d2fa3c5e347

fine_G

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids/1; canonical SHA-256: c7e3f1600ab9063214a79c5b8401577c50b5aa037065c01d9749ade107d0c5e9

fine_not_G

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids/2; canonical SHA-256: 2117a83ad8116727ac02f1aa241104512467811b74e7f71c0fdebc66c5bb554b

coarse_G

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids/3; canonical SHA-256: 80a81811c16e7d0ae0bdc7ac3d2676a23e4652940240ccb1671b0dc095d29829

coarse_not_G

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids; canonical SHA-256: 1f26789f455620bfd27a2534b9cd00c48b9f47468828149ce4905cdaa8ae4c1a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/0; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/1; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/id; canonical SHA-256: b35461b7a0aaaaac456b67c52cf6f744cad869652ea01201a14200dde7427668

historical-q2-randomized-b2-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/lead; canonical SHA-256: 5188db387db78b439114c7dd01bf62521c204d2b7afc2876bb0a135fcf00197d

Assess the guard-preserving randomized q2 b2 to q1 native c1/c2 transfer before any adoption; retain fixednu, the exact query/output domain, finite-call guarantee and distinct quantity IDs.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 17

Native pointer: /joint_analysis/synthesis_coverage/obligations/16; canonical SHA-256: 1e41c7095c5f57d6df6df92bd9ad0b6a21b36ce09f5bd138ce3bdd2551755937

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/argument; canonical SHA-256: ce1d204a92fabcb877910d6ff87e1e903646b7ac9737c1e474fbabd7df886a0f

This already-derived coarse closure is now actually registered in both native optimalc2 comparisons, on this cell, with decisive nativeproof ZO_PROOF_HOLDER_COARSE_NATIVE_20261116. Globalq1 upper and affine lower match asTheta_nu(d) on0<W<=1. This resolves publication bookkeeping only, not pending historicalsource recertification, q2transfers, or strict certified-domain extension.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs; canonical SHA-256: 3bd81b176df4a309a0c48710b060be9d75a09f42db27cc395955a8e1a9dc1434

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/0; canonical SHA-256: d754c71e5e50ff3e695c0ac14a1e41414c2f86de8f09641ffe43d4cffc5e3f4a

SO_ZO_E07_neighborhood__deterministic__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/1; canonical SHA-256: 6ab631db2880106e77c61285acd88f191c50d5e4a5ccd4cf96ccdeecfc6be23c

SO_ZO_E07_neighborhood__deterministic__b5

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/2; canonical SHA-256: a5e70eabcc3a730664047de954dd6f60e79d434558ebb02f417abb92792009a7

SO_ZO_E07_neighborhood__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/3; canonical SHA-256: 7f1dbab3e9f430813219675b5655627b86f81863fdc6654493101f1cc6ff5fd8

SO_ZO_E07_neighborhood__randomized__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids; canonical SHA-256: a0e64c0a91981fc6b374bd8b8e6fab641bea9a6995439d587963bb031e3707cc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids/0; canonical SHA-256: 2117a83ad8116727ac02f1aa241104512467811b74e7f71c0fdebc66c5bb554b

coarse_G

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids; canonical SHA-256: 9f8a53b1f08c6b3621c929464e617347f2591b4dfbb5254933e6b54002269d33

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/0; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/1; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/id; canonical SHA-256: ee93e85ec9f0cce3a8f367fb5ced9835ada99524f46fbede57a324a712113083

published-coarse_G

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/kind; canonical SHA-256: 50133df05f664fa7a089f5165d8e064594aa92d2dedff6eb73c481199b11b5cd

closed_region_publication

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs; canonical SHA-256: 9e6dd3281c9bb73ab09001d59455626b37a0f0d233e298d5dcb11b662853256c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 18

Native pointer: /joint_analysis/synthesis_coverage/obligations/17; canonical SHA-256: b7b08caa7e86389ff45b4692513f9344f2a60691e1f7800b1e5c52b5b12016b4

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/argument; canonical SHA-256: ce1d204a92fabcb877910d6ff87e1e903646b7ac9737c1e474fbabd7df886a0f

This already-derived coarse closure is now actually registered in both native optimalc2 comparisons, on this cell, with decisive nativeproof ZO_PROOF_HOLDER_COARSE_NATIVE_20261116. Globalq1 upper and affine lower match asTheta_nu(d) on0<W<=1. This resolves publication bookkeeping only, not pending historicalsource recertification, q2transfers, or strict certified-domain extension.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs; canonical SHA-256: 3bd81b176df4a309a0c48710b060be9d75a09f42db27cc395955a8e1a9dc1434

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/0; canonical SHA-256: d754c71e5e50ff3e695c0ac14a1e41414c2f86de8f09641ffe43d4cffc5e3f4a

SO_ZO_E07_neighborhood__deterministic__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/1; canonical SHA-256: 6ab631db2880106e77c61285acd88f191c50d5e4a5ccd4cf96ccdeecfc6be23c

SO_ZO_E07_neighborhood__deterministic__b5

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/2; canonical SHA-256: a5e70eabcc3a730664047de954dd6f60e79d434558ebb02f417abb92792009a7

SO_ZO_E07_neighborhood__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/3; canonical SHA-256: 7f1dbab3e9f430813219675b5655627b86f81863fdc6654493101f1cc6ff5fd8

SO_ZO_E07_neighborhood__randomized__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/cell_ids; canonical SHA-256: 2b56bd2c83a1d2cd73138b941672b030dd55e7e4b18870a29b54f58e1c30bd4b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/cell_ids/0; canonical SHA-256: 80a81811c16e7d0ae0bdc7ac3d2676a23e4652940240ccb1671b0dc095d29829

coarse_not_G

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids; canonical SHA-256: 9f8a53b1f08c6b3621c929464e617347f2591b4dfbb5254933e6b54002269d33

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/0; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/1; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/id; canonical SHA-256: ebc3b43656c9189cca70850f66ebe089042774b364e85bd33671fd701c724f90

published-coarse_not_G

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/kind; canonical SHA-256: 50133df05f664fa7a089f5165d8e064594aa92d2dedff6eb73c481199b11b5cd

closed_region_publication

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs; canonical SHA-256: 9e6dd3281c9bb73ab09001d59455626b37a0f0d233e298d5dcb11b662853256c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs/0; canonical SHA-256: b59c429bd476d81f3070495111023e8b35fbc8ec7318acc5ec13aeb74dc4a85e

ZO_PROOF_HOLDER_COARSE_NATIVE_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 19

Native pointer: /joint_analysis/synthesis_coverage/obligations/18; canonical SHA-256: dcf8b9501c073e0749e4e2a6d2a585212ebc611bfab070afdf33dbcacaf793b5

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids; canonical SHA-256: 8a1fcbbafb77805ac018106120c1fd98987059c702151f41e19d4e58a952364c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/0; canonical SHA-256: 58b0a066672d2c2f417d77d8e2b077489ba7cdf4119b31e22842d5197cdfc44e

SO_ZO_E07_neighborhood__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/1; canonical SHA-256: 68bc20c9672b2c1c3d154e6b2453e8b9a60ffb5ac118051b0eb4f6252fad8229

SO_ZO_E07_neighborhood__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/2; canonical SHA-256: fc2aa46b1b31c84b2467d9874831f26f2ae5ae2e8929e1a22f8344e25aacab8b

SO_ZO_E07_neighborhood__deterministic__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/3; canonical SHA-256: 336f65fdc6969f4dba1fb97faeed9e77e957c4d7c73591fc951ec41adccdc29d

SO_ZO_E07_neighborhood__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/id; canonical SHA-256: 3e40840a600894217220d41fef8b41e169aa04b880d86f4edc42a2656c986f9a

curated-scope-limit-2f6e197d61

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

Native pointer: /joint_analysis/target; canonical SHA-256: be1543dc97b5d4312a5cc4ff6856742111df9b688adce4b167f2843a7b406fde

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: ecda5fc89c4eb17d66fb76f5f75520330059aee3bcd63a80bb9824d1844dcb01

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 3df045183276ab5954ce0725111b5f26a5715e32f61c1104f53717b497f6ec56

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 4b81cab280b1e31c2ea7afa9a416577b7c9c22795698d5d642e0394c36a90edd

/quantities/2

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 1efd9a58641ee36655a3788f0589a9e772917f92bc109fbda3e8bab1efe50202

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 694fa9d62f66d39967be49160341da6694937e9952a58b813a05264e741bc82d

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: 9144bc7d5c5a4bc0e75d8f79b37fa8644f06b7fc228560431637ce1c0e722819

0<nu<1, fixed separately for each theorem-family member.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 03d37ae0cccad679ab6684b0bb76a7126edc98e3c802c41e2c2ff309465f7cd2

\nu

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: e0eb801b1c2812bfd4e58d2f70585d54d30539e3fd6c4dcee0d07d666671a4f0

D: d integer >=1; 0<nu<1; H_nu,R,tau,epsilon>0; W=H_nu R^(1+nu)/epsilon. For each fixed nu, q1 is the native minimax fixed-path scalar-value cost for its view's g1 guarantee.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 52f7aa30bb7e6088041b5cac1c2f5cc38acc0f7d92dd4df4ecc49b6f193c48c1

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 97fda858e5959560ede6752696f1c0b2552f0283fb09978f8d14b1d0893330c3

SO_ZO_E07_neighborhood_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 6dec1ed0a5128052b40de6e40a919ee9dd12f115d2243412d38bd583fd100993

SO_ZO_E07_neighborhood_p_c20b7fde2a

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: efd00c3a2315cfd9b03d869b622b9ba7e7f329e59f5fb007db21f0ee9740976a

SO_ZO_E07_neighborhood_p_a4aab29c5f

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 10a7db3944e7557de53ddf8f31bab925cdea77e13947146744527eeba13e8082

SO_ZO_E07_neighborhood_p_a0da9ce9fd

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 24827f065ef65557ddf87adc22e2b41a6aad00ead79f67b0c9d8154789c54286

SO_ZO_E07_neighborhood_p_5c322c6737

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 6e0c45e6053ea843a88ec9e9902027d3cd4a5d6b003399fc4ba2c655894de218

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: b6f93ef583fbea24a9eb2fa492a2ca01f7bb7e94bb47d8a823518bdbe9661a13

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: 776b8f0e2095ed838c2c32c216e028e1528409ebee6fa3c7417328f96a56ff56

W=H_nu R^(1+nu)/epsilon, the existing derived parameter. Scaling x=Ru and values by H_nu R^(1+nu) makes the Holder budget one and accuracy 1/W without changing exact-value call count.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: c4c0fc5c8a9dc86f80f8ee9c9d8deb1ae30526dd4c510a0a0aacb2cf30b5acbc

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 6df9ecbdde0d7dd6ffe8e7090fa03186aff36e53e6ab9044a0c347e2e3fea886

SO_ZO_E07_neighborhood_p_b86951d182

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 6dec1ed0a5128052b40de6e40a919ee9dd12f115d2243412d38bd583fd100993

SO_ZO_E07_neighborhood_p_c20b7fde2a

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/2; canonical SHA-256: efd00c3a2315cfd9b03d869b622b9ba7e7f329e59f5fb007db21f0ee9740976a

SO_ZO_E07_neighborhood_p_a4aab29c5f

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/3; canonical SHA-256: c9e53c6c13e2632e36f2d766d527bd97ace1ec0e3dec56a0ab2c808e76207907

SO_ZO_E07_neighborhood_p_6290a52d96

#### Native item 5

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/4; canonical SHA-256: 24827f065ef65557ddf87adc22e2b41a6aad00ead79f67b0c9d8154789c54286

SO_ZO_E07_neighborhood_p_5c322c6737

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: bf225f2e4787e165f5a245e55bb71f55793511a8a605aefe07ca2c056ccf936d

W

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: da484a1550153cd710677ed425cfe576f947b5cb4d84cd120fff805d97966daa

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 97fda858e5959560ede6752696f1c0b2552f0283fb09978f8d14b1d0893330c3

SO_ZO_E07_neighborhood_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 6dec1ed0a5128052b40de6e40a919ee9dd12f115d2243412d38bd583fd100993

SO_ZO_E07_neighborhood_p_c20b7fde2a

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: efd00c3a2315cfd9b03d869b622b9ba7e7f329e59f5fb007db21f0ee9740976a

SO_ZO_E07_neighborhood_p_a4aab29c5f

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 10a7db3944e7557de53ddf8f31bab925cdea77e13947146744527eeba13e8082

SO_ZO_E07_neighborhood_p_a0da9ce9fd

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 24827f065ef65557ddf87adc22e2b41a6aad00ead79f67b0c9d8154789c54286

SO_ZO_E07_neighborhood_p_5c322c6737

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: 6df9ecbdde0d7dd6ffe8e7090fa03186aff36e53e6ab9044a0c347e2e3fea886

SO_ZO_E07_neighborhood_p_b86951d182

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Diakonikolas and Guzmán. Lower Bounds for Parallel and Randomized Convex Optimization. COLT 2019, PMLR 99.

https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf

[2] Yurii Nesterov. Universal gradient methods for convex optimization problems. Mathematical Programming, 2015; checked against the 2013 author manuscript.

https://optimization-online.org/wp-content/uploads/2013/04/3833.pdf
