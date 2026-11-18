# Unknown convex quadratics: exact values

**Setting ID.** `SO_ZO_E05`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Fully optimal

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Lipschitz gradient; structure: Quadratic

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

An unknown quadratic $f(x)=\frac12x^\top Ax-b^\top x+c$, where $A\in\mathbb{R}^{d\times d}$ is symmetric and $0\preceq A\preceq\beta I_d$, $b\in\mathbb{R}^d$, and $c\in\mathbb{R}$ hold.

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

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

$I_d,\preceq$: Identity matrix and positive-semidefinite order **Domain:** $I_d\in\mathbb{R}^{d\times d}$; the order applies to real symmetric matrices of the same size.

$A\preceq B$ means that $v^\top(B-A)v\ge0$ for every $v\in\mathbb{R}^d$.

$A,b,c$: Matrix, linear coefficient, and constant of the unknown quadratic objective **Domain:** $A=A^\top\in\mathbb{R}^{d\times d},\ b\in\mathbb{R}^d,\ c\in\mathbb{R}$.

$f(x)=\tfrac12x^\top Ax-b^\top x+c$, $0\preceq A\preceq\beta I_d$.

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

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime E05.R1

**Region.** $Q\ge32$; the unknown quadratic coefficient matrix satisfies $0\preceq A\preceq\beta I_d$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B2, B10

$$
\Omega(d\min\{d,\sqrt Q\})
$$

**Upper bound.** B1, B9

$$
O(d\min\{d,\sqrt Q\})
$$

**Gap or comparison.** $O(1)$

### R2 - Parameter regime E05.NEW.zero_region

**Region.** $Q\le2$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B4, B12

$$
0
$$

**Upper bound.** B3, B11

$$
0
$$

### R3 - Parameter regime E05.NEW.endpoint_det

**Region.** $2<Q<4$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B6

$$
\Omega(d)
$$

**Upper bound.** B5

$$
O(d)
$$

**Gap or comparison.** $O(1)$

### R4 - Parameter regime E05.NEW.constant_bridge

**Region.** $4\le Q<32$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B8, B16

$$
\Omega(d)
$$

**Upper bound.** B7, B15

$$
O(d)
$$

**Gap or comparison.** $O(1)$

### R5 - Parameter regime E05.NEW.endpoint_rand

**Region.** $2<Q<4$.

**Views.** Randomized

**Quantity.** Q2

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B14

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Upper bound.** B13

$$
O(\max\{1,d(1-2/Q)\})
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Exact quadratic finite-difference acceleration or quadratic interpolation

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d\min\{d,\sqrt Q\})\quad(Q\ge32)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Central differences recover the gradient exactly; alternatively, $(d+1)(d+2)/2$ values recover all coefficients and allow an exact solution.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.2 and Appendix C.1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.2 and Appendix C.1; pdf pages: 3; printed pages: 3

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.2 and Appendix C.1; pdf pages: 28; printed pages: 28

### B2 - Adaptive linear-measurement lower bound for unknown quadratics

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt Q\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\varepsilon\le \beta R^2/32$.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Quadratic hard family in Theorem 2.1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Quadratic hard family in Theorem 2.1; pdf pages: 3; printed pages: 3

### B3 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

### B4 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

### B5 - Deterministic finite-difference descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Conditions.** $2<Q<4$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

### B6 - Deterministic hard family with indistinguishable directions

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega(d)
$$

**Conditions.** $2<Q<4$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

### B7 - Exact quadratic finite-difference acceleration or quadratic interpolation

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $4\le Q<32$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C; pdf pages: 29; printed pages: 29

### B8 - Adaptive linear-measurement lower bound for unknown quadratics

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $Q\ge 3$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

### B9 - Exact quadratic finite-difference acceleration or quadratic interpolation

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d\min\{d,\sqrt Q\})\quad(Q\ge32)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Central differences recover the gradient exactly; alternatively, $(d+1)(d+2)/2$ values recover all coefficients and allow an exact solution.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.2 and Appendix C.1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.2 and Appendix C.1; pdf pages: 3; printed pages: 3

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.2 and Appendix C.1; pdf pages: 28; printed pages: 28

### B10 - Adaptive linear-measurement lower bound for unknown quadratics

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt Q\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\varepsilon\le \beta R^2/32$.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Quadratic hard family in Theorem 2.1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Quadratic hard family in Theorem 2.1; pdf pages: 3; printed pages: 3

### B11 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

### B12 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

### B13 - Randomized projection descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q<4$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

### B14 - Lower bound for estimation of a random spherical center

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Conditions.** $2<Q<4$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

### B15 - Exact quadratic finite-difference acceleration or quadratic interpolation

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $4\le Q<32$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C; pdf pages: 29; printed pages: 29

### B16 - Adaptive linear-measurement lower bound for unknown quadratics

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $Q\ge 3$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

## 5. Local arguments

### A1 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A2 - Smooth exact-value complexity just below the zero-query threshold

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

### A3 - Extending the endpoint bound to fixed accuracy windows

**Scope.** All model budgets are fixed while accuracy varies; exact unrestricted value access.

The endpoint lower bound at $Q=3$ yields $\Omega(d)$ for every $Q\ge3$. The deterministic finite-difference accelerated bound is $O(d)$ on every fixed numerical interval $4\le Q\le128^2$.

Solving to a smaller error also solves to any larger error, so minimax complexity is nondecreasing as $\varepsilon$ decreases. At $Q=3$, the endpoint lemma gives $\gamma=1/3$ and hence a uniform $\Omega(d)$ randomized lower bound. The deterministic accelerated upper bound $O(d\sqrt Q)$ is at most $128$ times its universal constant on the stated interval. The same upper bound applies to randomized algorithms. The endpoint hard family is already quadratic, so the lower statement transfers unchanged to the quadratic subclass; the quadratic upper follows by restriction of the smooth algorithm.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1
