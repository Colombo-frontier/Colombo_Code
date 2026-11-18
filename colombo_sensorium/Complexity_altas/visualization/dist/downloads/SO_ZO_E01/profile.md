# Lipschitz convex optimization with exact values

**Setting ID.** `SO_ZO_E01`

Single-objective optimization

Minimize $f$ globally over $B_2(0,R)$ and return a point with small objective gap.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Lipschitz function; structure: No additional structure

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

$f:B_2(0,R)\to\mathbb{R}$ is convex and satisfies $|f(x)-f(y)|\le L\|x-y\|_2$ for every $x,y$ in the ball. Neither a definition nor regularity outside the ball is assumed. Continuity on the ball guarantees attainment of the constrained minimum.

### Oracle interface

At any finite query point $x$ in $B_2(0,R)$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

Projection and the stated proximal operations over known geometry are free.

The public inputs are $d$, $L$, $R$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

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

$L$: Public upper bound on the objective Lipschitz constant **Domain:** $L>0$.

$|f(x)-f(y)|\le L\|x-y\|_2$ throughout the function domain specified in this profile.

$R$: Feasible-ball radius **Domain:** $R>0$.

The output must belong to $B_2(0,R)$; the query radius is specified separately in the interface.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$A$: Lipschitz accuracy ratio **Domain:** $A>0$.

$A=LR/\varepsilon$

$s$: Saturation scale involving dimension and accuracy **Domain:** $s>0$.

$s=\min\{d,A^2\}$

$d_0$: Universal dimension threshold required by the lower bound **Domain:** $d_0>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$C$: Upper-bound constant or universal threshold for an applicability window **Domain:** $C>0$.

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

### R1 - Parameter regime E01.R1

**Region.** $d\ge d_0,\ A\ge C,\ A^2\le d,\ C\ge8$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B3

$$
\Omega(dA^2/\log(eA^2))
$$

**Upper bound.** B2, B1

$$
\ O(dA^2\log(edA))
$$

**Gap or comparison.** $O(\log(edA)\log(eA^2))$

### R2 - Parameter regime E01.R2

**Region.** $d\ge d_0,\ A\ge C,\ A^2>d$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B3, B5, B20

$$
\begin{cases}\Omega(d^2/\log(ed)),&A<64,\\\Omega(\max\{d^2/\log(ed),d\min\{d,\sqrt A\}\}),&64\le A<98304,\\\Omega(\max\{d^2/\log(ed),d\min\{d,\sqrt A\},d\log A\}),&A\ge98304.\end{cases}
$$

**Upper bound.** B2, B1

$$
O(\min\{dA^2\log(edA),d^2\log(ed)\log(4A)\})
$$

**Gap or comparison.** $O\!\left(\frac{\min\{dA^2\log(edA),d^2\log(ed)\log(4A)\}}{\max\{d^2/\log(ed),\mathbf{1}_{\{A\ge64\}}d\min\{d,\sqrt A\},\mathbf{1}_{\{A\ge98304\}}d\log A\}}\right)$

### R3 - Parameter regime E01.R4

**Region.** $\varepsilon\ge LR$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B7, B15

$$
0
$$

**Upper bound.** B6, B14

$$
0
$$

### R4 - Parameter regime E01.R1

**Region.** $d\ge d_0,\ A\ge C,\ A^2\le d,\ C\ge8$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B11

$$
\Omega(dA^2/\log(eA^2))
$$

**Upper bound.** B8, B9, B10

$$
\ O(dA^2)
$$

**Gap or comparison.** $O(\log(eA^2))$

### R5 - Parameter regime E01.R2

**Region.** $d\ge d_0,\ A\ge C,\ A^2>d$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B11, B13, B21

$$
\begin{cases}\Omega(d^2/\log(ed)),&A<64,\\\Omega(\max\{d^2/\log(ed),d\min\{d,\sqrt A\}\}),&64\le A<98304,\\\Omega(\max\{d^2/\log(ed),d\min\{d,\sqrt A\},d\log A\}),&A\ge98304.\end{cases}
$$

**Upper bound.** B8, B9, B10

$$
O(\min\{dA^2,d^2\log(ed)\log(4A)\})
$$

**Gap or comparison.** $O\!\left(\frac{\min\{dA^2,d^2\log(ed)\log(4A)\}}{\max\{d^2/\log(ed),\mathbf{1}_{\{A\ge64\}}d\min\{d,\sqrt A\},\mathbf{1}_{\{A\ge98304\}}d\log A\}}\right)$

### R6 - One-dimensional positive-query regime

**Region.** $d=1,\quad 0<\varepsilon<LR$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B17, B19

$$
\Omega(\log(4A))
$$

**Upper bound.** B16, B18

$$
O(\log(4A))
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

### B1 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
\mathrm{Det}:\quad O(d^2\log(d+1)\log(4A))
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic convex localization using exact scalar values within the ball. Geometry, real arithmetic and numerical precision are free.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Z26 Proposition 4

**Source location.** [3](https://arxiv.org/html/2607.16558v2) pdf pages: 12; printed pages: 12; theorem: Z26 Proposition 4

**Source location.** [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) theorem: Z26 Proposition 4

### B2 - Deterministic approximate subgradient extraction and localization envelope

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\min\{dA^2\log(edA),d^2\log(ed)\log(4A)\}\right)
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $0<\varepsilon\le LR/8$; queries restricted to the ball.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_DET_SUBGRAD

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

**Source location.** [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) theorem: Convex value-localization theorem, as normalized in the cited Proposition 4

### B3 - Random support functions or a smooth strongly convex hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(ds/\log(es))
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2)

**Conditions.** $d\ge d_0,\varepsilon\le cLR$; the lower bound covers arbitrary randomized adaptive algorithms.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source gives a necessary query count at constant success probability for arbitrary adaptive randomized algorithms. A higher fixed success requirement inherits the same lower bound.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Theorems 5--6

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Theorems 5--6

**Source location.** [3](https://arxiv.org/html/2607.16558v2) pdf pages: 12; printed pages: 12; theorem: Theorems 5--6

### B4 - Random support functions or a smooth strongly convex hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log A)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Use the smooth strongly convex subclass with minimizer in $B(R/2)$ and $\beta \asymp L/R$, at sufficiently small accuracy.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_PRECISION_LOG

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Class-inclusion corollary of Theorem 2.5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 4; printed pages: 4; theorem: Class-inclusion corollary of Theorem 2.5

### B5 - Multiscale hard family for accuracy dependence

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log A)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $A=LR/\varepsilon\ge6\cdot128^2$

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_PRECISION_LOG

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 4; printed pages: 4; theorem: Theorem 2.5

### B6 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge LR$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_ZERO

### B7 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge LR$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_ZERO

### B8 - Randomized two-point smoothing or convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
\mathrm{Rand}:\quad O\!\left(\min\{dA^2,d^2\log(d+1)\log(4A)\}\right)
$$

**Sources.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $dA^2$ comes from randomized two-point smoothing; the localization branch is deterministic.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Source location.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) pdf pages: 4; printed pages: 4; theorem: S17 Corollary 2; Z26 Propositions 3--4

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: S17 Corollary 2; Z26 Propositions 3--4

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: S17 Corollary 2; Z26 Propositions 3--4

**Source location.** [3](https://arxiv.org/html/2607.16558v2) pdf pages: 12; printed pages: 12; theorem: S17 Corollary 2; Z26 Propositions 3--4

**Source location.** [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) theorem: S17 Corollary 2; Z26 Propositions 3--4

### B9 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
\mathrm{Det}:\quad O(d^2\log(d+1)\log(4A))
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic convex localization using exact scalar values within the ball. Geometry, real arithmetic and numerical precision are free.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Z26 Proposition 4

**Source location.** [3](https://arxiv.org/html/2607.16558v2) pdf pages: 12; printed pages: 12; theorem: Z26 Proposition 4

**Source location.** [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) theorem: Z26 Proposition 4

### B10 - Deterministic approximate subgradient extraction and localization envelope

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\min\{dA^2\log(edA),d^2\log(ed)\log(4A)\}\right)
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $0<\varepsilon\le LR/8$; queries restricted to the ball.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_DET_SUBGRAD

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

**Source location.** [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) theorem: Convex value-localization theorem, as normalized in the cited Proposition 4

### B11 - Random support functions or a smooth strongly convex hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(ds/\log(es))
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2)

**Conditions.** $d\ge d_0,\varepsilon\le cLR$; the lower bound covers arbitrary randomized adaptive algorithms.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source gives a necessary query count at constant success probability for arbitrary adaptive randomized algorithms. A higher fixed success requirement inherits the same lower bound.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Theorems 5--6

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Theorems 5--6

**Source location.** [3](https://arxiv.org/html/2607.16558v2) pdf pages: 12; printed pages: 12; theorem: Theorems 5--6

### B12 - Random support functions or a smooth strongly convex hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log A)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Use the smooth strongly convex subclass with minimizer in $B(R/2)$ and $\beta \asymp L/R$, at sufficiently small accuracy.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_PRECISION_LOG

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Class-inclusion corollary of Theorem 2.5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 4; printed pages: 4; theorem: Class-inclusion corollary of Theorem 2.5

### B13 - Multiscale hard family for accuracy dependence

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log A)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $A=LR/\varepsilon\ge6\cdot128^2$

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_PRECISION_LOG

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 4; printed pages: 4; theorem: Theorem 2.5

### B14 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge LR$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_ZERO

### B15 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge LR$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_ZERO

### B16 - Feasible ternary interval reduction

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(\log(4A))
$$

**Conditions.** $d=1,\quad 0<\varepsilon<LR$, with $A=LR/\varepsilon$.

**Oracle correspondence.** Only exact scalar values at the two interior trisection points are used; both lie in the target interval.

**Guarantee conversion.** The output satisfies the objective-gap requirement deterministically for every admissible convex L-Lipschitz function.

**Output rule.** Return the midpoint of the final interval without querying it; it is feasible.

**Resource conversion.** Exactly two values per step, with k=ceil(log(A)/log(3/2)) fixed before any answer. All initialization and output processing require no additional values.

**Local argument.** ZO_PROOF_UNIVARIATE

### B17 - Multiscale smooth-subclass lower bound and zero-query impossibility

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\log(4A))
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $d=1,\quad 0<\varepsilon<LR$, with $A=LR/\varepsilon$.

**Oracle correspondence.** Restrict the globally smooth hard objectives to the target interval. Each target value is simulated by one source value; the source permits the more general unrestricted query domain.

**Guarantee conversion.** The primary logarithmic lower bound and local one-query lower bound hold for randomized 2/3 success; deterministic algorithms are included.

**Output rule.** The source global minimizer lies in the target interval, so target and source objective gaps agree. Every permitted target output is permitted in the source model.

**Resource conversion.** Fixed worst-case scalar-value cap on every path. Theorem 2.5 applies at A>=98304; the one-query argument and explicit constant comparison extend Omega(log(4A)) uniformly to all A>1.

**Local argument.** ZO_PROOF_PRECISION_LOG, ZO_PROOF_UNIVARIATE

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: arXiv:2610.00345v1: Section 2 characters 6700-11900; Theorem 2.5 characters 13496-15396; Theorem E.5 and Section E.4 characters 112800-119800

Primary archived source SHA256: 1869dd758da361249e15ca5c9bc20792f55d6d7432b04be0d818323539baf105. Fresh exact-ID arXiv metadata dates v1 to 2026-09-29, within cutoff 2026-11-09.

The source model has pointwise 2/3 success, arbitrary adaptive randomized policies, unrestricted queries and outputs, and a fixed worst-case value budget. Theorem E.5 retains a positive dimension-times-depth bound at d=1.

With R_h=R/2, beta_h=2L/(3R), mu_h=beta_h/2, restriction gives an L-Lipschitz target objective with a feasible global minimizer and one-to-one scalar-value simulation. The source accuracy ratio is A/6; its explicit window is A>=98304. The local proof supplies the remaining A>1 interval.

### B18 - Feasible ternary interval reduction

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(\log(4A))
$$

**Conditions.** $d=1,\quad 0<\varepsilon<LR$, with $A=LR/\varepsilon$.

**Oracle correspondence.** Only exact scalar values at two feasible interior trisection points per step are used.

**Guarantee conversion.** The deterministic ternary-search algorithm is an allowed randomized-view algorithm and succeeds with probability one on each instance.

**Output rule.** Return the feasible midpoint of the final interval; no value or certificate at the output is required.

**Resource conversion.** The cap is 2*ceil(log(A)/log(3/2)) scalar values on every execution path, fixed before the first answer.

**Local argument.** ZO_PROOF_UNIVARIATE

### B19 - Multiscale smooth-subclass lower bound and zero-query impossibility

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\log(4A))
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $d=1,\quad 0<\varepsilon<LR$, with $A=LR/\varepsilon$.

**Oracle correspondence.** The source model permits unrestricted exact-value queries; one source value simulates each query to a hard function restricted to the target interval.

**Guarantee conversion.** Both source and target require pointwise success probability at least 2/3 for arbitrary adaptive randomized algorithms with an instance-independent private seed.

**Output rule.** The hard global minimizer is feasible, and the source allows every feasible target output, including unqueried outputs.

**Resource conversion.** Both use fixed worst-case scalar-value caps. The primary logarithmic bound applies for A>=98304; zero-query impossibility gives T>=1 on the remaining interval, yielding a uniform Omega(log(4A)) rate.

**Local argument.** ZO_PROOF_PRECISION_LOG, ZO_PROOF_UNIVARIATE

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: arXiv:2610.00345v1: Section 2 characters 6700-11900; Theorem 2.5 characters 13496-15396; Theorem E.5 and Section E.4 characters 112800-119800

Primary archived source SHA256: 1869dd758da361249e15ca5c9bc20792f55d6d7432b04be0d818323539baf105. Fresh exact-ID arXiv metadata dates v1 to 2026-09-29, within cutoff 2026-11-09.

The source model has pointwise 2/3 success, arbitrary adaptive randomized policies, unrestricted queries and outputs, and a fixed worst-case value budget. Theorem E.5 retains a positive dimension-times-depth bound at d=1.

With R_h=R/2, beta_h=2L/(3R), mu_h=beta_h/2, restriction gives an L-Lipschitz target objective with a feasible global minimizer and one-to-one scalar-value simulation. The source accuracy ratio is A/6; its explicit window is A>=98304. The local proof supplies the remaining A>1 interval.

### B20 - Restriction of the smooth dimension-accuracy hard family to the Lipschitz feasible ball

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt A\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $d\ge d_0,\ A\ge C,\ A^2>d,\ A\ge64$; $L,R>0$ and $A=LR/\varepsilon$.

**Oracle correspondence.** Restrict globally beta_h-smooth source objectives to the ball with beta_h=L/(2R), R_h=R. They are L-Lipschitz there. One target exact scalar value is one unrestricted source value; no derivatives or outside-ball capability is added to the target.

**Guarantee conversion.** Any uniformly correct deterministic target algorithm is a seed-independent source algorithm with success probability one, so the randomized source lower bound applies.

**Output rule.** The source global minimizer is feasible, so constrained and global minima coincide. Any feasible target output, including an unqueried point, is permitted by the source.

**Resource conversion.** Identical fixed worst-case scalar-value cap on every execution path. The exact transferred inequality is T>=max{5d/16,(d/4096)min{d,sqrt(A/2)}} for A>=64.

**Local argument.** ZO_PROOF_SMOOTH_SUBCLASS

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: arXiv:2610.00345v1, Section 2 algorithm/class definitions and Theorem 2.1; archived text characters 8930-11780; theorem begins at 10190.

Primary archived source SHA256: 1869dd758da361249e15ca5c9bc20792f55d6d7432b04be0d818323539baf105. Exact-ID arXiv search 428ffccf8ee3460e80ed036739b105d4e450fe997e86921ea45172f45bd5dfdd exposed v1 dated 2026-09-29, before cutoff 2026-11-09. The primary HTML was fetched and the decisive theorem/model text freshly read.

The source permits arbitrary adaptive randomized unrestricted exact scalar-value queries and outputs, free computation/precision, a fixed worst-case budget, and per-objective success at least 2/3; its positive-definite quadratic subclass already forces the bound.

The local proof calibrates beta_h=L/(2R), R_h=R, proves L-Lipschitzness on the target ball, preserves the objective gap and charges one source value per target value. A>=64 is the exact theorem accuracy guard; both current views inherit the lower bound.

### B21 - Restriction of the smooth dimension-accuracy hard family to the Lipschitz feasible ball

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt A\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $d\ge d_0,\ A\ge C,\ A^2>d,\ A\ge64$; $L,R>0$ and $A=LR/\varepsilon$.

**Oracle correspondence.** Restrict globally beta_h-smooth source objectives to the ball with beta_h=L/(2R), R_h=R. They are L-Lipschitz there. One target exact scalar value is one unrestricted source value; no derivatives or outside-ball capability is added to the target.

**Guarantee conversion.** Source and target both require at least 2/3 private-seed success on every objective for one uniform algorithm.

**Output rule.** The source global minimizer is feasible, so constrained and global minima coincide. Any feasible target output, including an unqueried point, is permitted by the source.

**Resource conversion.** Identical fixed worst-case scalar-value cap on every execution path. The exact transferred inequality is T>=max{5d/16,(d/4096)min{d,sqrt(A/2)}} for A>=64.

**Local argument.** ZO_PROOF_SMOOTH_SUBCLASS

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: arXiv:2610.00345v1, Section 2 algorithm/class definitions and Theorem 2.1; archived text characters 8930-11780; theorem begins at 10190.

Primary archived source SHA256: 1869dd758da361249e15ca5c9bc20792f55d6d7432b04be0d818323539baf105. Exact-ID arXiv search 428ffccf8ee3460e80ed036739b105d4e450fe997e86921ea45172f45bd5dfdd exposed v1 dated 2026-09-29, before cutoff 2026-11-09. The primary HTML was fetched and the decisive theorem/model text freshly read.

The source permits arbitrary adaptive randomized unrestricted exact scalar-value queries and outputs, free computation/precision, a fixed worst-case budget, and per-objective success at least 2/3; its positive-definite quadratic subclass already forces the bound.

The local proof calibrates beta_h=L/(2R), R_h=R, proves L-Lipschitzness on the target ball, preserves the objective gap and charges one source value per target value. A>=64 is the exact theorem accuracy guard; both current views inherit the lower bound.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 71b4f79ca9dac62bf266a01d9022fecc4acfe0e45b633b367c03462a5a37787c

### Native proof: ZO_PROOF_DET_SUBGRAD

Native pointer: /proofs/0; canonical SHA-256: 407c5df5e344384419290b1738e9bef775ee3cb0a66626433c2cb6decdf4fe2c

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 5302a8df00b684fda4ba426691ee465e9cb0c9988936fa01b2026ed2eb070a28

A deterministic procedure obtains an $\eta$-accurate subgradient at a point within distance $\zeta$ of the requested point using at most $7d\lceil\log_2(2L\sqrt d/\eta)\rceil$ values. It yields the convex upper $O(dA^2\log(edA))$ and the strongly convex upper $O(dL^2\log(edA)/(\mu\varepsilon))$, with $A=LR/\varepsilon$.

For a convex one-dimensional restriction, maintain an active interval whose every subderivative lies in $[\ell,u]$. Divide it into six equal pieces and query its seven grid points. Their secant slopes satisfy $s_0\le\cdots\le s_5$. The intervals $[q_1,q_2]$ and $[q_4,q_5]$ have protected subgradient envelopes $[s_0,s_2]$ and $[s_3,s_5]$. Since $(s_2-s_0)+(s_5-s_3)\le u-\ell$, selecting the narrower one halves the envelope width and divides the interval length by six.

Set $\tau=\eta/\sqrt d$, $k=\lceil\log_2(2L/\tau)\rceil$, and $r_1=\zeta/2$. At coordinate $j$, run $k$ subdivisions from half-width $r_j$, move to the final midpoint, and retain the two protected secants of denominator $h_j=2r_j6^{-k}$. Set $r_{j+1}=\tau h_j/(16L)$. Then $r_{j+1}/r_j\le1/8$, and all later displacement is at most $\tau h_j/(8L)$. Translating a protected secant by this displacement changes its slope by at most $\tau/4$. Thus every subgradient of the final common point $y$ has coordinate $j$ in $[\ell_j-\tau/4,u_j+\tau/4]$. The midpoint vector differs from every such subgradient by at most $3\eta/4$ in Euclidean norm. All probe and protection points lie within $\zeta$ of the original point. The scales may be very small, but are positive and require the same finite number of queries.

For a globally Lipschitz convex function and a public projected set $K\subseteq B_2(R)$ containing zero, the extracted vector satisfies
$$f(z)\ge f(x)+\langle\widehat g,z-x\rangle-2L\zeta-2R\eta\quad(z\in K).$$
Choose $\zeta=\varepsilon/(16L)$, $\eta=\varepsilon/(16R)$, so the model error is $\varepsilon/4$ and $\|\widehat g\|\le2L$ in the stated nontrivial range. Projected subgradient descent with step $R/(2L\sqrt N)$ gives averaged gap at most $2LR/\sqrt N+\varepsilon/4$. Taking $N\ge64A^2$ proves the convex rate. The probes may leave $K$ only in the all-space variant.

For a function defined on the ball, keep iterates in $B_2(R-2\delta)$. For strong convexity, apply extraction to $h(x)=f(x)-\mu\|x\|^2/2$, which is convex and at most $2L$-Lipschitz because $\mu R\le L$. Choose $\delta=\gamma/(16L)$, vector error $\eta=\gamma/(8R)$, and add $\mu x$ back. Then $\|\widehat g\|\le4L$ and
$$f(z)\ge f(x)+\langle\widehat g,z-x\rangle+\mu\|z-x\|^2/2-\gamma.$$
With $a_t=2/[\mu(t+1)]$, projection, and $D_t=\|x_t-x_*\|^2$,
$$f(x_t)-f(x_*)-\gamma\le\frac{\mu(t-1)}4D_t-\frac{\mu(t+1)}4D_{t+1}+\frac{16L^2}{\mu(t+1)}.$$
Multiply by $t$ and sum. The initial distance coefficient is zero, and the remaining distance terms telescope. The weighted average has gap at most $32L^2/[\mu(T+1)]+\gamma$. Taking $\gamma=\varepsilon/8$ and $T+1\ge128L^2/(\mu\varepsilon)$, including shrinkage loss at most $2L\delta$, proves the result. Ordinary convex projected descent gives the $A^2$ branch. Deterministic value localization supplies the separate $d^2\log(ed)\log(4A)$ branch; take the minimum only among applicable branches.

For a known body $B_2(r_{\rm in})\subseteq K\subseteq B_2(R_{\rm out})$, the identity $(1-a)K+aB_2(r_{\rm in})\subseteq K$ supplies feasible probe room. Choose $a=\gamma/(16LR_{\rm out})$ and probe radius at most $ar_{\rm in}/2$. Shrinkage costs at most $LaR_{\rm out}$. The query count is independent of the probe radius and uses $R_{\rm out}$ in place of $R$. A finite-sum mean value costs $n$ component values, multiplying these deterministic bounds by $n$.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/0/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 877cdb9cd795caed0e13c33ad2863f0ada58ec1582a858a422039d398b8d6202

Exact real scalar values; finite positive probe scales; free real arithmetic and no bit-precision charge. Ball-restricted variants keep all probes inside the ball; global variants allow all-space probes.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: afe187f3be4db81d4b193c8a2c5076055a0f310fb0d5c7839d30f66b59332f42

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 2

Native pointer: /proofs/0/source_refs/1; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 9b122cc20ebbcbb8c7d338e1124a537a201bd66352037e20d3c520fe88f01dba

Deterministic extraction of an approximate subgradient

### Native proof: ZO_PROOF_PRECISION_LOG

Native pointer: /proofs/1; canonical SHA-256: 3669c61a80d81bbe0aa60db6734f4240fa0120356dbe68abfd4212e4b9184177

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 22a37def08b7d321ee101fa614c49bf15f038bb3f82579c82fc250f797c52cb7

For the smooth class, $Q\ge128^2$ gives $\Omega(d\log Q)$. This also holds in a public strongly convex class with $\kappa\ge2$. For a ball-restricted Lipschitz class, $A=LR/\varepsilon\ge6\cdot128^2$ gives $\Omega(d\log A)$.

Dorn et al., Theorem 2.5, gives
$$\frac{3d}{4000}\left[1+\frac{\log(\beta_hR_h^2/\varepsilon)}{\log((\beta_h+\mu_h)/(\beta_h-\mu_h))}\right]$$
when $\mu_h/\beta_h\in[1/2,1]$ and $\beta_hR_h^2/\varepsilon\ge128^2$. Choose $\mu_h=\beta_h/2$, so the denominator is $\log3$. A convex $\beta$-smooth class contains this subclass with $\beta_h=\beta$, $R_h=R$. A public lower curvature budget $\mu\le\beta/2$ also contains it, uniformly in the public condition number.

For the ball-restricted Lipschitz class choose $R_h=R/2$, $\beta_h=2L/(3R)$, and $\mu_h=\beta_h/2$. On $B_2(R)$, $\|\nabla f(x)\|\le\beta_h(\|x\|+\|x_*\|)\le L$, and the global minimizer remains inside the feasible ball. One source value simulates one restricted value. The stronger source oracle permits all such algorithms, and $Q_h=A/6$. The explicit window makes $\log(A/6)$ and $\log A$ uniformly comparable.

For a selected-component finite sum with all components equal to the same hard function, one component query is one source query. This transfer has cost one, not $n$. A logarithmic and a dimension-dependent lower bound may be maximized only where both respective windows hold.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/1/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 33d1886dbfecb60ab07affb5a5b70ec72413f57bba3bcdaee7db562519fff3ce

The source theorem retains its unrestricted query/output domain, fixed query cap, and stated accuracy window.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 7d6c3836ee73380d5185e810548c207da824c054e9f2dcfc9d6a1af7c006e12b

Explicit logarithmic lower bounds and class restrictions

### Native proof: ZO_PROOF_ZERO

Native pointer: /proofs/2; canonical SHA-256: 1d6580814630c8e2805d1bef988f17262747efcfe8580ea0d6eaace3086f220c

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: e337fe1bbdc7a8471c27bff8578ac9695fda39f5bd738324501658aee12cbc83

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/2/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 1415baad26ae3bdb7a7f19af0ab941587cafa672fc7447677224c888ab47c12b

The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: a1c4db43e97db238b9e152f2d0f29dccb6ee901b91806fdf8840d239abdee28f

Zero-query certificates

### Native proof: ZO_PROOF_UNIVARIATE

Native pointer: /proofs/3; canonical SHA-256: 18bbc378949116023a7416133f9f6d4649b90b8cf96879214e148e7972373199

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: 9b9e47c8f3586db0e12f7b72f3856642903a5c8f5be7be5a7f6d54eb259851ec

Write A=LR/epsilon>1. Upper bound: start with [a,b]=[-R,R]. Query u=a+(b-a)/3 and v=b-(b-a)/3, charging both exact scalar values. If f(u)<=f(v), retain [a,v]; otherwise retain [u,b]. Convexity ensures that the retained closed interval contains a constrained minimizer, including in the equality case. After k steps its length is 2R(2/3)^k. Its midpoint is feasible and is within R(2/3)^k of a retained minimizer, so its objective gap is at most LR(2/3)^k. Taking k=ceil(log(A)/log(3/2)) gives a deterministic budget of 2k values and requires no value at the output. The finite comparisons and affine updates are Borel. This proves O(log(4A)) deterministically and hence also for the randomized 2/3 guarantee.

Lower bound for every A>1: f_+(x)=Lx and f_-(x)=-Lx are admissible on [-R,R]. Their epsilon-success sets satisfy x<=-R+epsilon/L and x>=R-epsilon/L respectively, and are disjoint when epsilon<LR. A zero-query output distribution is common to both objectives; its two success probabilities sum to at most one. Thus the randomized 2/3 guarantee, and also the deterministic guarantee, require at least one scalar-value query.

Logarithmic lower bound: use the subclass transfer in accepted local proof ZO_PROOF_PRECISION_LOG, with its primary premise independently reread here. Dorn et al., arXiv:2610.00345v1, source SHA256 1869dd758da361249e15ca5c9bc20792f55d6d7432b04be0d818323539baf105, Section 2 characters 6700-11900, Theorem 2.5 characters 13496-15396, and Theorem E.5/Section E.4 characters 112800-119800, uses a fixed worst-case budget and pointwise success probability 2/3 for arbitrary adaptive randomized exact-value algorithms. Its queries and outputs are unrestricted. The dimension-times-depth lower argument applies for d=1 as well. Set source localization radius R_h=R/2, smoothness beta_h=2L/(3R), and strong convexity mu_h=beta_h/2. Every source function has a global minimizer x_* in [-R/2,R/2]. Since its gradient vanishes there, for |x|<=R we have |f'(x)|<=beta_h(|x|+|x_*|)<=L. Restriction to [-R,R] is therefore an admissible target function, and its constrained minimum equals its global minimum. A target algorithm can be simulated with one source value per target value, and its feasible output is permitted by the stronger source model. The source ratio beta_h R_h^2/epsilon equals A/6. Theorem 2.5 consequently gives T>=(3/4000)[1+log(A/6)/log(3)] when A>=A_0=6*128^2=98304. This lower bound includes deterministic algorithms.

Uniform combination: for A>=A_0, log(A/6)>=log(4A)/2, since A_0>=144. For 1<A<A_0, T>=1>=log(4A)/log(4A_0). Thus throughout A>1, T>=c log(4A), with c=min{1/log(4A_0),3/(8000 log(3))}>0. Together with the ternary-search upper bound this proves Theta(log(4A)) for both quantities. At A=1 the existing zero-query comparison applies; the new region is strict and does not include that endpoint. Any overlap with an existing high-accuracy comparison specializes to compatible bounds, while its higher-dimensional claims are untouched.

#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: 81b28f775a1d7387fb5d71bc4185c2ae94938cb1b3f5b61b528a834517790102

#### Native item 1

Native pointer: /proofs/3/limitations/0; canonical SHA-256: 270db0d6703cd88d12dc312dd6e35bf172563211b3c680dad6d93a74526635fc

The logarithmic lower bound depends on the stated primary preprint theorem; the ternary-search and zero-query arguments are local proofs.

#### Native item 2

Native pointer: /proofs/3/limitations/1; canonical SHA-256: a6a10a6cc2e68b17e966718170aa01a0fcb1e1064051a3db3837ebb15a3a584a

This establishes the stated one-dimensional region and does not settle higher-dimensional logarithmic gaps.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: f8d32cd02569abb254e67ea6d00e2006e1b51e71218aaaa8a6cd03ccb71fb27b

d=1, L,R>0 and 0<epsilon<LR, for both existing algorithm views, their existing guarantees, and fixed worst-case scalar-value budgets.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /proofs/3/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 9758e32bd20c65bc4634aff36626c29676b9b972e139a5277cee1f18020a8537

Matching one-dimensional exact-value complexity

### Native proof: ZO_PROOF_SMOOTH_SUBCLASS

Native pointer: /proofs/4; canonical SHA-256: e5e2c7f1a5faf77978f81da517faa4181b18716496d7869e67bd3acc8e8b66c2

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: 94bd02d6fa37eb9fb0a9abf677a153d3767b20e4b9e976ff5d770466736ddf08

Primary premise: Dorn et al., arXiv:2610.00345v1, Section 2 and Theorem 2.1, archived SHA256 1869dd758da361249e15ca5c9bc20792f55d6d7432b04be0d818323539baf105, source characters 8930-11780 (theorem begins at 10190). For globally beta_h-smooth convex objectives with a global minimizer in B_2(0,R_h), fixed-budget adaptive randomized exact-value algorithms with per-objective success at least 2/3 require T>=max{5d/16,(d/4096)min{d,sqrt(beta_h R_h^2/epsilon)}} when epsilon<=beta_h R_h^2/32. Queries and outputs may be unrestricted.

Set R_h=R and beta_h=L/(2R). For every source objective choose a global minimizer x_* with norm at most R. Its gradient vanishes. On B_2(0,R), ||grad f(x)||_2<=beta_h ||x-x_*||_2<=2 beta_h R=L. Integrating along segments in the ball proves that the restriction is convex and L-Lipschitz. Its constrained minimum equals the source global minimum.

A target algorithm on this restricted objective is simulated using exactly one source scalar evaluation for each target value. The ball-restricted queries and feasible, possibly unqueried output are allowed by the stronger source model. The output gap and private-seed success probability are unchanged, and the same fixed worst-case cap holds on every path. Thus a uniformly successful target randomized algorithm would solve every source instance. Deterministic algorithms are included as seed-independent algorithms.

Here beta_h R_h^2/epsilon=A/2, so the theorem window is exactly A>=64 and gives T>=max{5d/16,(d/4096)min{d,sqrt(A/2)}}. Since min{d,sqrt(A/2)}>=min{d,sqrt(A)}/sqrt(2), this proves Omega(d min{d,sqrt(A)}) with universal constants. No new target smoothness or global-minimizer promise is imposed: these are properties only of an adversarial subclass.

On each existing R2 domain d>=d_0, A>=C, A^2>d, retain the accepted lower Omega(d^2/log(ed)); retain the independent accepted Omega(d log A) only when A>=98304; add this new lower only when A>=64. Their maximum gives the displayed three-branch lower envelope. Below 64 the old envelope remains unchanged, and equality at 64 is included by the source theorem. At A=d^2 and d tending to infinity the new lower is Omega(d^2), while the stronger old term is Omega(d^2/log(ed)); the improvement is material. Upper bounds and logarithmic-gap labels remain valid; the gap expressions are recomputed as their upper envelope divided by the new compatible lower maximum.

For A^2<=d and A>=64, the new d sqrt(A) rate is dominated by the accepted d A^2/log(e A^2) rate; no R1 change is needed. The zero-query region epsilon>=LR is disjoint from A>=64. At d=1 the transferred constant lower is dominated by the accepted Omega(log(4A)) one-dimensional envelope. Old lower-bound proofs and literature are retained conditionally, rather than recertified.

#### Native field: limitations

Native pointer: /proofs/4/limitations; canonical SHA-256: 423088745d91e21f933c4490d38712616b0fe62b9546606e169e38a8ecda11ec

#### Native item 1

Native pointer: /proofs/4/limitations/0; canonical SHA-256: e5a1ef54ecbf7d7cf1aee4b5dc0403170d22fd3a379a311ff84b1ce0dc564ccf

This is a source-backed local transfer and envelope update, not a completed survey or a claim of global optimality.

#### Native item 2

Native pointer: /proofs/4/limitations/1; canonical SHA-256: c8a5c81763b5766c1be2ab9b3a22ee17910caeec003c7f8ba7b2775a2a6b165d

The new bound is inactive for A<64. Existing source-specific d_0 and C guards are preserved.

#### Native field: scope

Native pointer: /proofs/4/scope; canonical SHA-256: d4ccf9870f9e0b5e7c19762c56de30d5935416c0f6f7d70b6474c6c6dba0a505

Only the two existing E01.R2 comparisons are changed; the transferred theorem itself holds for every integer d>=1 and A>=64.

#### Native field: source_refs

Native pointer: /proofs/4/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /proofs/4/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: 3e376726fdb9e7343c31349659aa397b9931174025fa7c3302ba13d020f1b36d

Smooth hard-instance restriction improves the Lipschitz lower envelope

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: e28426fa7ac2df0a16d03103c80a3ec0d1f97007852d57f2e467712e62255f4d

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 8a8f8ad98bb67b7cf801daf8290454f80d0a367b09e8a68f90f45ddc0fee6e81

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 2ace7e8c050bdc1cd47d2006dbbdf1b9e49484829156db3baca19e69df80e6f1

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 0b850bfd113cf54361f8fe1973c4f88b1a943b0e192313c13dee621aea3c2c43

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: f1db417d7f5c2db0a1f34ad2900dd811e1776dd81bdd1b50a203c5bc13f8f83d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: b52ace3617a2694f3fd43a13ca34d12e53d8401302c19dca80ee7d256033fa38

R1 intersect native guards

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 4e37783ad562a293bffb78fa32c08b157f082850700320ab1070814cbfb40bcc

SO_ZO_E01__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 0538702e2b17559ddbf1d5dc4e9e30f1ae8aeea62f9a253c77aeb29a3f549fd1

Conditional native use; redundant localization branch retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 6e750454546b8573ad20102fe649a054a0ea03af251d51f55f87b2a5b074f50b

Native deterministic localization guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 2ea022528e84e1299647a2ab80736d5be73b9a875d0146b860f917135240a78c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: b52ace3617a2694f3fd43a13ca34d12e53d8401302c19dca80ee7d256033fa38

R1 intersect native guards

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 51b0c2324078b3f4453114cbca82e09925a62434ab1cac2f04866fcf20d16c12

SO_ZO_E01__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7f788e7f368cb53f707d594f905f1b89c250bf666716f06d31fa258719ccb621

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 29752edcd4a7fa866faff0ef568ca1dc0a68b75bcc6a5909624ffdf893ffa241

ZO_PROOF_DET_SUBGRAD

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 97c9646cc2c0bb50ab435177ac8582ebdba77928338065229773b3cd6a5e2b16

Conditional native use.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 848a1c80fbbe8f6c882e221ced6752e51648f25734b9603f2d50093a75ee24b4

A>=8; feasible ball-restricted probes.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: ba8871b442dc3dfc25a73637416bb1539afde0cbebb4279cc9752a007983d08c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 03acf05475a6231ab462d783579c90d9311be4c159dc5db784b7eb8f25c1f0e0

R1 intersect native source guard

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 91c4f33bfebb6e4a43a9c030f3663ce4e7dc2714f65e01cc6271c57d5f650a3c

SO_ZO_E01__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 6c0614df596e19a9f6f1fdb4383f60bb4b1d3e69f25ddafa8ed91399453d74a9

Conditional native lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 0e7f252cc3aab682af8178c182a5372371f84043e4bd8b60a20db5bc37bf2faf

d>=d_0, epsilon<=c LR; c universal.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: aa506e7758039ae95089cddf5f8370144c891f85cab6dc62a21c7813746bce43

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: 85193dba0957a13c1033a96541c4fddfcaada85e081c435f44fa65120eb2f2e6

SO_ZO_E01__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 0b99e3f273083af8fd8b6a6c29bac394f7dfdf7a94728da894d5149bfd8be4cf

Different quantity ID; no transfer adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: ed8027370766a357fad538fc25abe54f808f2320bd48d4476e22169f50ea0f04

Distinct q2; retained smooth-subclass guard.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: 968d10a0f9bd4a8b7d2cd963d45c0ca2f97742b08d7279c6bff45e8896195d17

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: 585eaefd845b615b59f44dc3e3daa168b482980b77b6e8d05aba33c233b18e23

SO_ZO_E01__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: 9eda840e6a9450fcfbb69a73e86baa9735b9d6e10b1c260ae3c89d4f3bd64957

d log A is no stronger than d A^2/log(e A^2).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: 5e6fb74eb2259b00aa72ad0f6199abcfc57275c37a165f6ff1eb6292ba76ea99

A>=98304

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/bound_uses/5; canonical SHA-256: 72ec7a5f6f4eea89381d63b06443e46d6f388cbf914de0d2017839b61cbad1de

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/bound_id; canonical SHA-256: 1e4cb2aeb9db919a5cb9d0b181c1c4cab6ac311d089601d56bef5a9042edb3f6

SO_ZO_E01__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/reason; canonical SHA-256: 2825ff5357ff120fbd6af49a84298839baada40153642fa5600533ccdee178b5

R1 requires A>=8.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/bound_uses/6; canonical SHA-256: 4e60492ebabd19cacb64683d7119640520f146816123f130f338bf4b5cb9a97d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/bound_id; canonical SHA-256: 0b9b494e575e3718b55b00b87fb4094988b5dd30fbfb997ba738c4b9d990ef17

SO_ZO_E01__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/reason; canonical SHA-256: 2825ff5357ff120fbd6af49a84298839baada40153642fa5600533ccdee178b5

R1 requires A>=8.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 8

Native pointer: /joint_analysis/comparisons/0/bound_uses/7; canonical SHA-256: d276b6af38cbadfbf981035ea78ea3ad94d0202bb15241a9042d7df41a9048fe

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/bound_id; canonical SHA-256: 29c3ff41867d52d86767fe0f709299914d78c94644d8a2f5290ee09e3f32e942

SO_ZO_E01__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/reason; canonical SHA-256: 3e27569ff5b0c03d36cfe47219c519c34b019ef5362b824036ead7cbc9cd6584

R1 implies d>=A^2>=64.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 9

Native pointer: /joint_analysis/comparisons/0/bound_uses/8; canonical SHA-256: f57cbeeb303eb7b3412670e8b375983736b6de824bbb37a0cba81054d4c17b29

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/bound_id; canonical SHA-256: 4fed4bb5fb50e132630c6ad9c724da2cedd9fd4d79b7da1336e77c7c77249682

SO_ZO_E01__deterministic__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/reason; canonical SHA-256: 3e27569ff5b0c03d36cfe47219c519c34b019ef5362b824036ead7cbc9cd6584

R1 implies d>=A^2>=64.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 10

Native pointer: /joint_analysis/comparisons/0/bound_uses/9; canonical SHA-256: ce3c543d337d3c620df96523ecbc384b0e7e3bf0315b78d4adc648267a389bca

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/bound_id; canonical SHA-256: 109b0b4392439ae92d3f51969a606e4a2fc115912606c8243d0b978d29776529

SO_ZO_E01__deterministic__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/reason; canonical SHA-256: a74a0097def7eccc6569033a22d80d4b0dcf2caa5b0381c1a06989f34bd616f8

R2 is disjoint from R1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/validity_region; canonical SHA-256: 9a88ee3d6a85c8ea900e4dd748a275e8d32c7dc9a2553494a9fd4aaacbb4cd2b

Native R2 and A>=64

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 2ef0fe3c6eda7792a8f5b2fa0b4418cf275ab3ac4b05f516f6cb6beb744d47af

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: fe0f31304d5f7c6bf7052c9b2990803a5e5dd12736cda757ab8acb73624eec6a

A^2=d is included; R2 is strict.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 67babbee7984a216762333377feba348973f8ad5052e7f6aa3bf5be16ab63e62

For A>=8,A^2<=d the localization rate does not improve the displayed subgradient rate up to universal constants.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 0429e05a04b6ca888b928103e3223cce9acd1a9fe7216554bf9c7cb406c03090

log(A) log(e A^2)=O(A^2), so the precision lower is dominated where active.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 03de2a350960d5a6e5bdb8b883f96efef358aac5338bbd18ae2e0143fe8a6616

O(log(e d A) log(e A^2)) on the compatible guarded intersection

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 331f81ef9ff18f66c463a32ce6c57cd118654ba9fc8e18a5cc6e0150a3b7e523

Omega(d A^2/log(e A^2)), under the retained source guard

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 9cb6667a4bc7c5f709daaff289ea47ee25e21dfb316cbd7f294392ceff100764

Retained logarithmic-factor bracket only; no global-optimality or literature-open claim.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 13fad0584104f67598305b16b94e7c91b7ef027d88f75d719633a6492f1bd844

O(d A^2 log(e d A)), with the original b1/b2 guards retained

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: de1ed52aa28faad00a48d0c3dbc1e75c60fd3215b719f878c040c4d358735213

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: e22f9ac0b58ae12dd916e9d318ef45a389c29349623c3356b4a35124d6c5adfb

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: c3edd3589047ab782baa104da57ca12cd15a1ad92676d3b26f3949fdf5f18dff

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 847ab7023234e245ac39fee0876c6599a80c59600a599994338d167bebc33a5e

R2 intersect native guards

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 4e37783ad562a293bffb78fa32c08b157f082850700320ab1070814cbfb40bcc

SO_ZO_E01__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 97c9646cc2c0bb50ab435177ac8582ebdba77928338065229773b3cd6a5e2b16

Conditional native use.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 6e750454546b8573ad20102fe649a054a0ea03af251d51f55f87b2a5b074f50b

Native deterministic localization guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 884d4eb0964d39c2f6945702d6630f61dc1ab9d379be69a8be5c47f2947e14bc

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 847ab7023234e245ac39fee0876c6599a80c59600a599994338d167bebc33a5e

R2 intersect native guards

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 51b0c2324078b3f4453114cbca82e09925a62434ab1cac2f04866fcf20d16c12

SO_ZO_E01__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7f788e7f368cb53f707d594f905f1b89c250bf666716f06d31fa258719ccb621

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 29752edcd4a7fa866faff0ef568ca1dc0a68b75bcc6a5909624ffdf893ffa241

ZO_PROOF_DET_SUBGRAD

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 046d029968336d152948f3c4f0e3bf15c59ef7b20569b5f6843550999ecd5e3c

Conditional native use; minimum retains branch applicability.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 848a1c80fbbe8f6c882e221ced6752e51648f25734b9603f2d50093a75ee24b4

A>=8; feasible ball-restricted probes.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 6666699daf37dc17a824c1ca45b986694419b766d094280d4adfc707ba5fdc23

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 451b65d81a55fc2295f89a8fb1405b89c71cf1ad366e05d78c3e0d404f158603

R2 intersect native source guard

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 91c4f33bfebb6e4a43a9c030f3663ce4e7dc2714f65e01cc6271c57d5f650a3c

SO_ZO_E01__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 6c0614df596e19a9f6f1fdb4383f60bb4b1d3e69f25ddafa8ed91399453d74a9

Conditional native lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 0e7f252cc3aab682af8178c182a5372371f84043e4bd8b60a20db5bc37bf2faf

d>=d_0, epsilon<=c LR; c universal.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: aa506e7758039ae95089cddf5f8370144c891f85cab6dc62a21c7813746bce43

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: 85193dba0957a13c1033a96541c4fddfcaada85e081c435f44fa65120eb2f2e6

SO_ZO_E01__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 0b99e3f273083af8fd8b6a6c29bac394f7dfdf7a94728da894d5149bfd8be4cf

Different quantity ID; no transfer adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: ed8027370766a357fad538fc25abe54f808f2320bd48d4476e22169f50ea0f04

Distinct q2; retained smooth-subclass guard.

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: 8a734f43efe5522bfa778a8c3749d2775768409ef3cfe70e2d4b2175d5b4dc17

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: 7810eb8677a1685cd8c3f372c0fac1dd49b22fdb2668c143591e95a76f31bd61

R2 AND A>=98304

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: 585eaefd845b615b59f44dc3e3daa168b482980b77b6e8d05aba33c233b18e23

SO_ZO_E01__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: e6fec3f7796e10d8ba70af3b1071bff78a3b8434f5317fb6e3fb2df5c9ef8f6d

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 7ae90a56a7a315485cbe4aa49ab117457db76363ea552e7b155bba4cea438472

Conditional native precision lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: 5e6fb74eb2259b00aa72ad0f6199abcfc57275c37a165f6ff1eb6292ba76ea99

A>=98304

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: 0c338d129a48358cb3011fcda3b9e4d4c6eca819b6873b3cb0d63676cd741383

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: 1e4cb2aeb9db919a5cb9d0b181c1c4cab6ac311d089601d56bef5a9042edb3f6

SO_ZO_E01__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: 032cfa98d61c2be3d198f0828b2ac2b230bbca25286d1040c9c0bd2bfd732a8c

Endpoint c3 is outside the nontrivial R2 source-applicability intersection.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/bound_uses/6; canonical SHA-256: d629433aebf5132790e7969c644081cbb59ca54e76de6fd7582234f15cc7cf4e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/bound_id; canonical SHA-256: 0b9b494e575e3718b55b00b87fb4094988b5dd30fbfb997ba738c4b9d990ef17

SO_ZO_E01__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/reason; canonical SHA-256: 032cfa98d61c2be3d198f0828b2ac2b230bbca25286d1040c9c0bd2bfd732a8c

Endpoint c3 is outside the nontrivial R2 source-applicability intersection.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 8

Native pointer: /joint_analysis/comparisons/1/bound_uses/7; canonical SHA-256: f533c9298c74022b7650af024c45d93a73ac4744e8a7804c99c5f656d85148f4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/bound_id; canonical SHA-256: 29c3ff41867d52d86767fe0f709299914d78c94644d8a2f5290ee09e3f32e942

SO_ZO_E01__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/reason; canonical SHA-256: e310fe30f66c144f5655806ac5a539b0fee4a457175b637d19c51e0db9b95ae8

On any d=1 overlap, localization already has O(log(4A)) cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 9

Native pointer: /joint_analysis/comparisons/1/bound_uses/8; canonical SHA-256: d5e58c6ac21a256c42156349ae3d40e3812d3f0be70ebd4a7f2a87104ac90592

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/bound_id; canonical SHA-256: 4fed4bb5fb50e132630c6ad9c724da2cedd9fd4d79b7da1336e77c7c77249682

SO_ZO_E01__deterministic__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/reason; canonical SHA-256: 42facf4d65ae35a18d1bc0d2bfeebe4d1534cbd0477291962de96fa5400dfd99

On d=1, b5 covers A>=98304; below that fixed threshold log(4A) is bounded and the retained lower is Omega(1).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 10

Native pointer: /joint_analysis/comparisons/1/bound_uses/9; canonical SHA-256: 06ca99c1bdd58062d87a6d97bc1f5bf152e66f2b0171dd1fe525289d300a4b42

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/adopted_region; canonical SHA-256: cb8beeef82331e805732098517d9109335b3d2b397ae69ab07dbfbeed6fb5b02

R2 AND A>=64

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/bound_id; canonical SHA-256: 109b0b4392439ae92d3f51969a606e4a2fc115912606c8243d0b978d29776529

SO_ZO_E01__deterministic__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/mapping_proof_refs; canonical SHA-256: b6b614de1cc1e62370415f950d585eb48d2106a76b076be1ee73061e83f64e52

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/mapping_proof_refs/0; canonical SHA-256: 71a4e2e3071d17a19caa3068c71a150f2b37f9f277b2105d06cceb6fd5cd20d8

ZO_PROOF_SMOOTH_SUBCLASS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/reason; canonical SHA-256: 4345bbec92274b31a363c0a3e6e719e3132245ab83b2f0c8c7d216639e2a392e

Conditional native smooth-subclass lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/validity_region; canonical SHA-256: 9a88ee3d6a85c8ea900e4dd748a275e8d32c7dc9a2553494a9fd4aaacbb4cd2b

Native R2 and A>=64

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 943e35538b10ecdd2d7b6596753b3c670fca520ddf2b852df583c2ab5b955490

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: cce644927cc5342277776d0558ce51b09cd6cc7d78e63f043a313379d2854141

A=64 and A=98304 are included calibrated source-activation thresholds.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 1b1474bc870d6b03bebc3c8c33ac5d21c2e77df57dda44f270e072fbf975dcbe

The displayed smooth rate saturates at A of order d^2; its exact transferred inequality switches at A=2d^2.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 0ab8202f1a2f226439bb267fe5b541159a3371d71d6a4f7fef806cd37c2aee62

Rate crossovers are asymptotic: A of order d^2/log(e d)^2 against the July lower, and log A of order d against the saturated smooth lower.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: dbd72659dd5f50fcaa01de77cce73c2114a6d70e99a485e9df0bd9bb68811053

Keep the guarded upper minimum; no exact crossover constants or intrinsic phase transition are inferred.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: f5a035b50e787d2ea37c257ec5e4a24f70feb5173f008fac4b2f69704f7cbfca

O(min{d A^2 log(e d A),d^2 log(e d) log(4A)}/max{d^2/log(e d), d min(d,sqrt(A)) [A>=64], d log(A) [A>=98304]}) on the compatible guarded intersection

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: a0f87b4b632f13d7858a47ae605f741be3278b98d8f5ba1614679cd1355c23dc

Omega(max{d^2/log(e d), d min(d,sqrt(A)) [only A>=64], d log(A) [only A>=98304]}), retaining the July source guard on the first term

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 160e43a98dfed4acd1ec8fb0315c0d61b4adf5fb54076f1d18a3afa90d54a994

The retained guarded ratio remains; no newly closed subregion or cost improvement is asserted.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: d4851670feb54c4fb8d1df26074e2be81da28390a1b511e55183ff2020dc5f04

O(min{d A^2 log(e d A),d^2 log(e d) log(4A)}), retaining each native branch guard

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: a840298a2bed299d4cb0f9011aa309807ffee2aa8695c6199a179f9d4b1ce115

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 2650b5559d44780683e81f539f1baba4b84462069a8c3f2ae7a655fe0ce8f0ea

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 53d3fa3c5ba80bc75cf95a26549dd9120d4d049414d62a58524a17312afa3e91

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 4e37783ad562a293bffb78fa32c08b157f082850700320ab1070814cbfb40bcc

SO_ZO_E01__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 6854a09192346578858c4a934b6df2eb907f8cef586aba9792795664832a638a

Any applicable positive-cost algorithm is dominated by zero cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 6e750454546b8573ad20102fe649a054a0ea03af251d51f55f87b2a5b074f50b

Native deterministic localization guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: aa0fba36207b1dfb830d50e99207723bfdff07ddfee0f621a25f1ada0c2764f9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 51b0c2324078b3f4453114cbca82e09925a62434ab1cac2f04866fcf20d16c12

SO_ZO_E01__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: f944eeb5bb30040e6edba34f72e7bc1587c81c17cd75551d601d6f1a430975bc

Disjoint from A<=1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: cff1a838ecee5cad7d35ad831f9aae5f4a5ba2362652b7db54a17dc48181cd98

A>=8

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: 3f2badf419c7f9f79efee83a2209e1b7322609068f980bc72f32b0c59c71ed2d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: 91c4f33bfebb6e4a43a9c030f3663ce4e7dc2714f65e01cc6271c57d5f650a3c

SO_ZO_E01__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: e284bccdedf38d062525a0d1b3f1dbab3035550c6725e6d9043586cd606da6fa

No active positive lower claim on the zero endpoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 462470619009aea93a42e43d6add997172a2e8367d37faa11cc380693ff4aed8

Retained nontrivial July source window.

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: aa506e7758039ae95089cddf5f8370144c891f85cab6dc62a21c7813746bce43

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: 85193dba0957a13c1033a96541c4fddfcaada85e081c435f44fa65120eb2f2e6

SO_ZO_E01__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 0b99e3f273083af8fd8b6a6c29bac394f7dfdf7a94728da894d5149bfd8be4cf

Different quantity ID; no transfer adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: ed8027370766a357fad538fc25abe54f808f2320bd48d4476e22169f50ea0f04

Distinct q2; retained smooth-subclass guard.

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: 328af1bb374cf8b28d5e53d85fce76824f11b943d3af153e267b784c7b2f0fc7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: 585eaefd845b615b59f44dc3e3daa168b482980b77b6e8d05aba33c233b18e23

SO_ZO_E01__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: f944eeb5bb30040e6edba34f72e7bc1587c81c17cd75551d601d6f1a430975bc

Disjoint from A<=1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 5e6fb74eb2259b00aa72ad0f6199abcfc57275c37a165f6ff1eb6292ba76ea99

A>=98304

#### Native item 6

Native pointer: /joint_analysis/comparisons/2/bound_uses/5; canonical SHA-256: cf99cc670fac90ae1846e50eb191f73be861a205bf5ea27066205fea607cc642

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/adopted_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/bound_id; canonical SHA-256: 1e4cb2aeb9db919a5cb9d0b181c1c4cab6ac311d089601d56bef5a9042edb3f6

SO_ZO_E01__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/reason; canonical SHA-256: e714445d63fccaaa23243316a2fb7b52041bc2f75e77f3247ddf1dcb5b0a1aa9

Retained zero-query center algorithm.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 7

Native pointer: /joint_analysis/comparisons/2/bound_uses/6; canonical SHA-256: 4cde0db98d76b99e1a19d13856ffe0ab6c323168a933e0106232e6940f07e9ba

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/adopted_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/bound_id; canonical SHA-256: 0b9b494e575e3718b55b00b87fb4094988b5dd30fbfb997ba738c4b9d990ef17

SO_ZO_E01__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/reason; canonical SHA-256: 9f315adf458d1fbb2af13f946f729a78899e41fb2d3a9778eb0b9721ab35d076

Retained nonnegative-cost lower certificate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 8

Native pointer: /joint_analysis/comparisons/2/bound_uses/7; canonical SHA-256: d1fd27d627b1494aff877ff277586b626340cb317c77282cb0acb3bc7dac28e2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/bound_id; canonical SHA-256: 29c3ff41867d52d86767fe0f709299914d78c94644d8a2f5290ee09e3f32e942

SO_ZO_E01__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/reason; canonical SHA-256: ba85dbe9d6d7f5344fe64a8ddf864a517f35761bb5c26f0e30cc17b943c90105

Strict positive-query region excludes this endpoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 9

Native pointer: /joint_analysis/comparisons/2/bound_uses/8; canonical SHA-256: 5e4032afd365ba6fba220e2d84b05a6dc9357efeb9ca95c11504a7c861d7408e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/bound_id; canonical SHA-256: 4fed4bb5fb50e132630c6ad9c724da2cedd9fd4d79b7da1336e77c7c77249682

SO_ZO_E01__deterministic__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/reason; canonical SHA-256: ba85dbe9d6d7f5344fe64a8ddf864a517f35761bb5c26f0e30cc17b943c90105

Strict positive-query region excludes this endpoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 10

Native pointer: /joint_analysis/comparisons/2/bound_uses/9; canonical SHA-256: c4271a8575d9b3613df1402a44a83c387232e88a36fcfae3c0ae539496d27b20

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/bound_id; canonical SHA-256: 109b0b4392439ae92d3f51969a606e4a2fc115912606c8243d0b978d29776529

SO_ZO_E01__deterministic__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/reason; canonical SHA-256: f944eeb5bb30040e6edba34f72e7bc1587c81c17cd75551d601d6f1a430975bc

Disjoint from A<=1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/validity_region; canonical SHA-256: 9a88ee3d6a85c8ea900e4dd748a275e8d32c7dc9a2553494a9fd4aaacbb4cd2b

Native R2 and A>=64

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 54efea3f79c18686049a67b8700ab1236a3ffccfda3ee3fa8e3b16994898568d

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: cc5b549212619d2837c2e8b5050da5d9c444cf7e0c42a867d3cc4d13a7b2cb18

A=1 is included.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 53ff0af57faddd9d7ddec07786d62053f554bc4bd66574ab964ecd5b07132659

The feasible center has objective gap at most LR; call counts are nonnegative.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/boundary_checks/2; canonical SHA-256: 574784bccd10b84d07a033523de46de4afccdbfa0d011ecbb33f16e18a01fb5c

No division by zero is used.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: 19fdc946a4ebcfb2ca21bd4aa776423ddf2ec498c147ae5ccbf5786457a80f84

not applicable: exact cost zero

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 288db1e792d284d5ac4888faa0600668e556e21badb3f69fa56aea2f2bbc75e5

None on this certified zero-query region.

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

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 16c91fb26d64dd0586aef3ca0ebecc4d59cc9e74ee7e73cd7894ddb184d761bc

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 3f72223a285399b3e1f8a71165d14d9ce01b43418ea9741e9eeab3034def6821

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: 35b826167be17831c048a92fb2cd1214c7be15fedec6d141e93d1557f635af32

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: b52ace3617a2694f3fd43a13ca34d12e53d8401302c19dca80ee7d256033fa38

R1 intersect native guards

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: b9c7f56e25e3e08b596022bb36e790258080b32af8decc0b50087a2b6ff90927

SO_ZO_E01__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: eb76f6e1fbda09085abe792ead91559db1d9e578faeb108e294cf1665a231819

Conditional native use under pointwise 2/3 success and fixed budget.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 4cd347b0185ff14c1f7cae107d4aa3714583cc95c93f739cbc4184dd59f44fa5

Native randomized two-point/localization guards.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 50f8328c8971e2cd55ddddd30048a6375630932fa97764b370961e1a6a3f25a4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: b52ace3617a2694f3fd43a13ca34d12e53d8401302c19dca80ee7d256033fa38

R1 intersect native guards

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 748af08626701be2e969b459261cfb09e59137d39833aa230fce151c8ddf829d

SO_ZO_E01__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: e80d43aa8283c0586143be12ebe26778574c3f5514594d323d1037233568400d

Redundant native branch retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 6e750454546b8573ad20102fe649a054a0ea03af251d51f55f87b2a5b074f50b

Native deterministic localization guard.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 4624c4068499029314731627484b49b238652681cd553c19fc84ea4f8f4baa8a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: b52ace3617a2694f3fd43a13ca34d12e53d8401302c19dca80ee7d256033fa38

R1 intersect native guards

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: ad6cdb72cb3bc8024fbc5e48eb87d1bc456f496507a8cf2ecb886c2397e11e60

SO_ZO_E01__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 7f788e7f368cb53f707d594f905f1b89c250bf666716f06d31fa258719ccb621

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 29752edcd4a7fa866faff0ef568ca1dc0a68b75bcc6a5909624ffdf893ffa241

ZO_PROOF_DET_SUBGRAD

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: f2f96ecc4f14e7d7ae3e3a5c9f6e1c7d5c400b11fd8c9e9454415aa162391858

Redundant deterministic native branch retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 848a1c80fbbe8f6c882e221ced6752e51648f25734b9603f2d50093a75ee24b4

A>=8; feasible ball-restricted probes.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: ed9e6711638df3aca2b8f21ee431333ee887d5fc20051b70ca13206646f8bf03

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: 03acf05475a6231ab462d783579c90d9311be4c159dc5db784b7eb8f25c1f0e0

R1 intersect native source guard

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: c66dc5d6937c5845c51a4228f56119db61de4418e1612c8257e68cdb977845cb

SO_ZO_E01__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: 8132a3ec9c633a15ce4d5104e4214b40b1c1fba2cfab7e8709b4f6c74971fb9b

Conditional native randomized lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 0e7f252cc3aab682af8178c182a5372371f84043e4bd8b60a20db5bc37bf2faf

d>=d_0, epsilon<=c LR; c universal.

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: dcec63bfb468c7555ff92ba40bdbe243cd76b625cdb2ca08c963b72bdcafd595

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: 2183f558c0fe14497d4050ab913bb0bf1d30f55a505c97db68209f561442486e

SO_ZO_E01__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: 0b99e3f273083af8fd8b6a6c29bac394f7dfdf7a94728da894d5149bfd8be4cf

Different quantity ID; no transfer adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: ed8027370766a357fad538fc25abe54f808f2320bd48d4476e22169f50ea0f04

Distinct q2; retained smooth-subclass guard.

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/bound_uses/5; canonical SHA-256: 671d80d9cb5ff2842a38868c98befa3b1e7ae9456bd4bc519df7d369ed735137

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/bound_id; canonical SHA-256: 737e6cbf953f3c73d6e2e21c94dfd4a9eba71aa19745ba7c8707b08c76d1b95d

SO_ZO_E01__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/reason; canonical SHA-256: 9eda840e6a9450fcfbb69a73e86baa9735b9d6e10b1c260ae3c89d4f3bd64957

d log A is no stronger than d A^2/log(e A^2).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/validity_region; canonical SHA-256: 5e6fb74eb2259b00aa72ad0f6199abcfc57275c37a165f6ff1eb6292ba76ea99

A>=98304

#### Native item 7

Native pointer: /joint_analysis/comparisons/3/bound_uses/6; canonical SHA-256: 8ffdcbad135057682e04db5227a935d241ff3b683c5114245b8bfa018b17f180

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/bound_id; canonical SHA-256: 24f60c818d1dfd1ca48eaacb0e6de83285b686375919325037df14be34e73cb0

SO_ZO_E01__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/reason; canonical SHA-256: 2825ff5357ff120fbd6af49a84298839baada40153642fa5600533ccdee178b5

R1 requires A>=8.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 8

Native pointer: /joint_analysis/comparisons/3/bound_uses/7; canonical SHA-256: 58bfab3e0134131f6fbd127b003341446c88970c03d01dca8f6110753747c99e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/bound_id; canonical SHA-256: c702c9264613cec20640c97bf35c33bc7b818c69ca163a0bf15002918f83599c

SO_ZO_E01__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/reason; canonical SHA-256: 2825ff5357ff120fbd6af49a84298839baada40153642fa5600533ccdee178b5

R1 requires A>=8.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 9

Native pointer: /joint_analysis/comparisons/3/bound_uses/8; canonical SHA-256: 8e21e944d7879944042fbac8370fbe55a48c7f5ef13d263008b50b70ee0f52ec

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/bound_id; canonical SHA-256: 009dab73992997d1a59ed3330938b8601737e8f7846a527550b9b4c04905360a

SO_ZO_E01__randomized__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/reason; canonical SHA-256: c7b438b78445325d5716e7f7e4c7f708dd5e011f4cee0fd4b2743f63a665cc74

R1 implies d>=64.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 10

Native pointer: /joint_analysis/comparisons/3/bound_uses/9; canonical SHA-256: 4f29626d9adcdf7ce51a905d760983907f34ce4400b3bf8eefb814331fa99b50

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/bound_id; canonical SHA-256: d1035bd08e969a0de5da5cbf458056ccaff2b9d1c6bc08cb4e759ba6ad6c83d6

SO_ZO_E01__randomized__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/reason; canonical SHA-256: c7b438b78445325d5716e7f7e4c7f708dd5e011f4cee0fd4b2743f63a665cc74

R1 implies d>=64.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 11

Native pointer: /joint_analysis/comparisons/3/bound_uses/10; canonical SHA-256: 341f809a75ec7d7efc30933041fd26ff1f462ca8e35e83e244ba80e69ec8f07e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/bound_id; canonical SHA-256: 4e5284261539c79664ee5eede28cf229c0111b5926085deb886b6ba64745277c

SO_ZO_E01__randomized__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/reason; canonical SHA-256: a74a0097def7eccc6569033a22d80d4b0dcf2caa5b0381c1a06989f34bd616f8

R2 is disjoint from R1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/validity_region; canonical SHA-256: 9a88ee3d6a85c8ea900e4dd748a275e8d32c7dc9a2553494a9fd4aaacbb4cd2b

Native R2 and A>=64

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: a440891114bcb86d2b97088c85e0bbc9306f1714e6e95cd431d206e8890e908d

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: f01b5235d9203bed7567d7b92abd328e696a4f6fb9ce9d8121ce54a1ebb8a802

A^2=d belongs to R1.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: bb9e0f79d9d5f7867cf5e50304e30ffa7c1ebd5f365a7f59aac080aa4c21dae3

The deterministic subgradient branch cannot improve the native O(d A^2) rate here.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/boundary_checks/2; canonical SHA-256: dbe924b2046fb85cfa2587053e0b50af803c686311fb54108f4c1f7f2479a618

The guarded precision lower is dominated because log(A) log(e A^2)=O(A^2).

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 523d40d4fb59d13ed36014053cd5401714dcf72de55dd5a8f57bf16ddb16fe1a

O(log(e A^2)) on the compatible guarded intersection

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 331f81ef9ff18f66c463a32ce6c57cd118654ba9fc8e18a5cc6e0150a3b7e523

Omega(d A^2/log(e A^2)), under the retained source guard

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: c273ec010defec05698e152bfed6fe6fe7228969b329f26a28e5cade1aa2e5c5

Retained logarithmic-factor bracket only; no global-optimality claim.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: 94e72b2355c4019ba8aa7532c8e6abecc7cf3f68aeff79f55e391d99e0e4bb29

O(d A^2), retaining original branch/guarantee guards

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: 855616d693eda50f5898ffb3cea14eb80ca3ac2d8f0ce38b9c485a87f646bfdc

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: 1d1878f148b481628c3cc0aca19ded9caf42eb77b9c842b433b9ec3bca4a7237

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: 3c497549417ad014fa7df4dcaec965470f9a8f4b4bb008b86f73ec6214990f88

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: 847ab7023234e245ac39fee0876c6599a80c59600a599994338d167bebc33a5e

R2 intersect native guards

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: b9c7f56e25e3e08b596022bb36e790258080b32af8decc0b50087a2b6ff90927

SO_ZO_E01__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 97c9646cc2c0bb50ab435177ac8582ebdba77928338065229773b3cd6a5e2b16

Conditional native use.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 4cd347b0185ff14c1f7cae107d4aa3714583cc95c93f739cbc4184dd59f44fa5

Native randomized two-point/localization guards.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: 356abee04cb7060f3e986b48eec1e1ae20f70a31d1b56f3783c6268143fe5182

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: 847ab7023234e245ac39fee0876c6599a80c59600a599994338d167bebc33a5e

R2 intersect native guards

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: 748af08626701be2e969b459261cfb09e59137d39833aa230fce151c8ddf829d

SO_ZO_E01__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: e80d43aa8283c0586143be12ebe26778574c3f5514594d323d1037233568400d

Redundant native branch retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: 6e750454546b8573ad20102fe649a054a0ea03af251d51f55f87b2a5b074f50b

Native deterministic localization guard.

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: 5c711b9552493904c0161b7b4e0b043621c99462ea12dc0b7c6c1ea01b53836e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: 847ab7023234e245ac39fee0876c6599a80c59600a599994338d167bebc33a5e

R2 intersect native guards

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: ad6cdb72cb3bc8024fbc5e48eb87d1bc456f496507a8cf2ecb886c2397e11e60

SO_ZO_E01__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: 7f788e7f368cb53f707d594f905f1b89c250bf666716f06d31fa258719ccb621

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 29752edcd4a7fa866faff0ef568ca1dc0a68b75bcc6a5909624ffdf893ffa241

ZO_PROOF_DET_SUBGRAD

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: f2f96ecc4f14e7d7ae3e3a5c9f6e1c7d5c400b11fd8c9e9454415aa162391858

Redundant deterministic native branch retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: 848a1c80fbbe8f6c882e221ced6752e51648f25734b9603f2d50093a75ee24b4

A>=8; feasible ball-restricted probes.

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/bound_uses/3; canonical SHA-256: 38f3170ce2f1624e6e65738cffdfd4ea7c00dbf4cc4b7ec482d0e77a8793b5e9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/adopted_region; canonical SHA-256: 451b65d81a55fc2295f89a8fb1405b89c71cf1ad366e05d78c3e0d404f158603

R2 intersect native source guard

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/bound_id; canonical SHA-256: c66dc5d6937c5845c51a4228f56119db61de4418e1612c8257e68cdb977845cb

SO_ZO_E01__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/reason; canonical SHA-256: 8132a3ec9c633a15ce4d5104e4214b40b1c1fba2cfab7e8709b4f6c74971fb9b

Conditional native randomized lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/validity_region; canonical SHA-256: 0e7f252cc3aab682af8178c182a5372371f84043e4bd8b60a20db5bc37bf2faf

d>=d_0, epsilon<=c LR; c universal.

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/bound_uses/4; canonical SHA-256: dcec63bfb468c7555ff92ba40bdbe243cd76b625cdb2ca08c963b72bdcafd595

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/bound_id; canonical SHA-256: 2183f558c0fe14497d4050ab913bb0bf1d30f55a505c97db68209f561442486e

SO_ZO_E01__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/reason; canonical SHA-256: 0b99e3f273083af8fd8b6a6c29bac394f7dfdf7a94728da894d5149bfd8be4cf

Different quantity ID; no transfer adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/validity_region; canonical SHA-256: ed8027370766a357fad538fc25abe54f808f2320bd48d4476e22169f50ea0f04

Distinct q2; retained smooth-subclass guard.

#### Native item 6

Native pointer: /joint_analysis/comparisons/4/bound_uses/5; canonical SHA-256: 4fcbc590cd426675ceb0e3018d06b241f833e21bb357b9b3cdccc472bc18a0b2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/adopted_region; canonical SHA-256: 7810eb8677a1685cd8c3f372c0fac1dd49b22fdb2668c143591e95a76f31bd61

R2 AND A>=98304

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/bound_id; canonical SHA-256: 737e6cbf953f3c73d6e2e21c94dfd4a9eba71aa19745ba7c8707b08c76d1b95d

SO_ZO_E01__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/mapping_proof_refs; canonical SHA-256: e6fec3f7796e10d8ba70af3b1071bff78a3b8434f5317fb6e3fb2df5c9ef8f6d

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/reason; canonical SHA-256: 7ae90a56a7a315485cbe4aa49ab117457db76363ea552e7b155bba4cea438472

Conditional native precision lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/validity_region; canonical SHA-256: 5e6fb74eb2259b00aa72ad0f6199abcfc57275c37a165f6ff1eb6292ba76ea99

A>=98304

#### Native item 7

Native pointer: /joint_analysis/comparisons/4/bound_uses/6; canonical SHA-256: 75f7119636a523503b9599ebb3ffac3afa2aa0ad6c0d19ec08f47f7e53a33129

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/bound_id; canonical SHA-256: 24f60c818d1dfd1ca48eaacb0e6de83285b686375919325037df14be34e73cb0

SO_ZO_E01__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/reason; canonical SHA-256: 032cfa98d61c2be3d198f0828b2ac2b230bbca25286d1040c9c0bd2bfd732a8c

Endpoint c3 is outside the nontrivial R2 source-applicability intersection.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 8

Native pointer: /joint_analysis/comparisons/4/bound_uses/7; canonical SHA-256: 6370ea1cfb8bf0a1d32c7fda439a25076b99d4235369df3b66d69765e89ebf7b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/bound_id; canonical SHA-256: c702c9264613cec20640c97bf35c33bc7b818c69ca163a0bf15002918f83599c

SO_ZO_E01__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/reason; canonical SHA-256: 032cfa98d61c2be3d198f0828b2ac2b230bbca25286d1040c9c0bd2bfd732a8c

Endpoint c3 is outside the nontrivial R2 source-applicability intersection.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 9

Native pointer: /joint_analysis/comparisons/4/bound_uses/8; canonical SHA-256: 250b323d5362c61ea2daa6cb4d75561fb941df433bf004bc13045c1aa586e1d6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/bound_id; canonical SHA-256: 009dab73992997d1a59ed3330938b8601737e8f7846a527550b9b4c04905360a

SO_ZO_E01__randomized__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/reason; canonical SHA-256: b8d21cfa3912db78ab6cbf813a6d511db9f33e4c29dad826b217abfb49be1168

On d=1, localization already has O(log(4A)) cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 10

Native pointer: /joint_analysis/comparisons/4/bound_uses/9; canonical SHA-256: d8ccb1a58e375680f86f09e976c7e4b7068a66d98c89c5485317d865529a9ca0

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/bound_id; canonical SHA-256: d1035bd08e969a0de5da5cbf458056ccaff2b9d1c6bc08cb4e759ba6ad6c83d6

SO_ZO_E01__randomized__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/reason; canonical SHA-256: 735dc5f62daa8bd69c1a815eafde2eff0e236beb24a7ba6895039be432ca6006

b6 covers the large-A logarithmic rate; below its fixed threshold log(4A) is bounded and the retained lower is Omega(1).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 11

Native pointer: /joint_analysis/comparisons/4/bound_uses/10; canonical SHA-256: ae9c49c51e0e2fbeb629362fd30afaaf4e671ac22e5bd38fae6e7f3349b7aba9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/adopted_region; canonical SHA-256: cb8beeef82331e805732098517d9109335b3d2b397ae69ab07dbfbeed6fb5b02

R2 AND A>=64

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/bound_id; canonical SHA-256: 4e5284261539c79664ee5eede28cf229c0111b5926085deb886b6ba64745277c

SO_ZO_E01__randomized__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/mapping_proof_refs; canonical SHA-256: b6b614de1cc1e62370415f950d585eb48d2106a76b076be1ee73061e83f64e52

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/mapping_proof_refs/0; canonical SHA-256: 71a4e2e3071d17a19caa3068c71a150f2b37f9f277b2105d06cceb6fd5cd20d8

ZO_PROOF_SMOOTH_SUBCLASS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/reason; canonical SHA-256: 4345bbec92274b31a363c0a3e6e719e3132245ab83b2f0c8c7d216639e2a392e

Conditional native smooth-subclass lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/validity_region; canonical SHA-256: 9a88ee3d6a85c8ea900e4dd748a275e8d32c7dc9a2553494a9fd4aaacbb4cd2b

Native R2 and A>=64

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: 77c2bef1d2115bf1e886ec754f2e5a8aaeeed268626dfa6c05977d3cf9c90a64

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: cd519025711e5140689469509e6d25235d4e52c0868a64b28b967d054e51865b

A=64 and A=98304 are included calibrated activation thresholds.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/boundary_checks/1; canonical SHA-256: 910dcc3f2b0ecff4a8e6e78453a03663086fd9825be1a23be7d340c7c440b691

Smooth saturation is at A of order d^2; the exact transferred inequality switches at A=2d^2.

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/boundary_checks/2; canonical SHA-256: 1fae7cb8f78a51e7a5732e3b9563651e155fb3c2b9093f55b84707d38b8719f6

The upper crossover satisfies A^2 of order d log(e d) log(4A), up to rate constants; the guarded minimum avoids an unsupported exact split.

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/boundary_checks/3; canonical SHA-256: bbc39cc6547282eb3195c4e0eb9114eb01b7bb8ef31a999152256231610fbe6d

The precision lower can dominate again when log A exceeds a scale of order d after smooth saturation.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: a4319b73b2c2adc8814fdd6d728b93e237536fecdca26c12130730071fcabdcd

O(min{d A^2,d^2 log(e d) log(4A)}/max{d^2/log(e d), d min(d,sqrt(A)) [A>=64], d log(A) [A>=98304]}) on the compatible guarded intersection

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: a0f87b4b632f13d7858a47ae605f741be3278b98d8f5ba1614679cd1355c23dc

Omega(max{d^2/log(e d), d min(d,sqrt(A)) [only A>=64], d log(A) [only A>=98304]}), retaining the July source guard on the first term

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: 48f72c58239a9347f95f8a382246d3463dd57bdc33d842cd19f347016a904afc

The retained guarded ratio remains; no newly closed subregion is asserted.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: 3f4f93c49a63ebcda86a3a066b5077a913249b21ebbc011f8b4c817331ad7e4c

O(min{d A^2,d^2 log(e d) log(4A)}), retaining each native branch guard

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: 6c578ca2acd969e34321d8039463068104e7b888adf3d5c7d8c9ff2464948bed

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: 03fe29d9c0e53216c56ec0992a31529ceb26d9a9a8d7db0e30c106ea23e411c9

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: 5879829e00681cdaac11c52c1775c531be15f80a1ffe56b9058ab7b0c37fa055

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: b9c7f56e25e3e08b596022bb36e790258080b32af8decc0b50087a2b6ff90927

SO_ZO_E01__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: 6854a09192346578858c4a934b6df2eb907f8cef586aba9792795664832a638a

Any applicable positive-cost algorithm is dominated by zero cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: 2bdf80b9cc2b06876c5689e7dbc617873e29eb95b59d61d4cdad124a91f8f146

Native two-point/localization guards.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: fde40a930181881d6649c09bb6eb37a9c9211528636dad6979fdb461bfa733d2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: 748af08626701be2e969b459261cfb09e59137d39833aa230fce151c8ddf829d

SO_ZO_E01__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: 6854a09192346578858c4a934b6df2eb907f8cef586aba9792795664832a638a

Any applicable positive-cost algorithm is dominated by zero cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: 6d04d8354585ae9e63e63353ce1c2f269031c454a31bb12eaa63bb207c16aefe

Native localization guard.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: 989cace03a41101f56a68d7353ee4829203244563b74a87846274f0631c11f81

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: ad6cdb72cb3bc8024fbc5e48eb87d1bc456f496507a8cf2ecb886c2397e11e60

SO_ZO_E01__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: f944eeb5bb30040e6edba34f72e7bc1587c81c17cd75551d601d6f1a430975bc

Disjoint from A<=1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: cff1a838ecee5cad7d35ad831f9aae5f4a5ba2362652b7db54a17dc48181cd98

A>=8

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/bound_uses/3; canonical SHA-256: 376fcd403c9a4e2ec03acedae45e72975131117dc0132ad98746682bcb0f0833

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/bound_id; canonical SHA-256: c66dc5d6937c5845c51a4228f56119db61de4418e1612c8257e68cdb977845cb

SO_ZO_E01__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/reason; canonical SHA-256: e284bccdedf38d062525a0d1b3f1dbab3035550c6725e6d9043586cd606da6fa

No active positive lower claim on the zero endpoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/validity_region; canonical SHA-256: 462470619009aea93a42e43d6add997172a2e8367d37faa11cc380693ff4aed8

Retained nontrivial July source window.

#### Native item 5

Native pointer: /joint_analysis/comparisons/5/bound_uses/4; canonical SHA-256: dcec63bfb468c7555ff92ba40bdbe243cd76b625cdb2ca08c963b72bdcafd595

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/bound_id; canonical SHA-256: 2183f558c0fe14497d4050ab913bb0bf1d30f55a505c97db68209f561442486e

SO_ZO_E01__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/reason; canonical SHA-256: 0b99e3f273083af8fd8b6a6c29bac394f7dfdf7a94728da894d5149bfd8be4cf

Different quantity ID; no transfer adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/validity_region; canonical SHA-256: ed8027370766a357fad538fc25abe54f808f2320bd48d4476e22169f50ea0f04

Distinct q2; retained smooth-subclass guard.

#### Native item 6

Native pointer: /joint_analysis/comparisons/5/bound_uses/5; canonical SHA-256: d5d0c3f5c35f19d73560d931cc40814de2312fa9c67a4300acbd3b9f073bd73f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/bound_id; canonical SHA-256: 737e6cbf953f3c73d6e2e21c94dfd4a9eba71aa19745ba7c8707b08c76d1b95d

SO_ZO_E01__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/reason; canonical SHA-256: f944eeb5bb30040e6edba34f72e7bc1587c81c17cd75551d601d6f1a430975bc

Disjoint from A<=1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/validity_region; canonical SHA-256: 5e6fb74eb2259b00aa72ad0f6199abcfc57275c37a165f6ff1eb6292ba76ea99

A>=98304

#### Native item 7

Native pointer: /joint_analysis/comparisons/5/bound_uses/6; canonical SHA-256: 39f305872f9083c72c3f56d308ad2d6a15bca282131d465732ed6a971ac89148

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/adopted_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/bound_id; canonical SHA-256: 24f60c818d1dfd1ca48eaacb0e6de83285b686375919325037df14be34e73cb0

SO_ZO_E01__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/mapping_proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/reason; canonical SHA-256: f41c28d24926958531dab657671906bea5e71ab7dcbe7c193b2f80fc06245a80

Retained deterministic center algorithm succeeds surely.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 8

Native pointer: /joint_analysis/comparisons/5/bound_uses/7; canonical SHA-256: 2b5fae520041517cd590e84d291685fbbf446f14972e33d9eaf8aeaa2b176b15

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/adopted_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/bound_id; canonical SHA-256: c702c9264613cec20640c97bf35c33bc7b818c69ca163a0bf15002918f83599c

SO_ZO_E01__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/mapping_proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/reason; canonical SHA-256: 9f315adf458d1fbb2af13f946f729a78899e41fb2d3a9778eb0b9721ab35d076

Retained nonnegative-cost lower certificate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 9

Native pointer: /joint_analysis/comparisons/5/bound_uses/8; canonical SHA-256: edf63276c27dc2b3646acbf06097ef95a871be18b3f625fbc74f720bb1d46d4d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/bound_id; canonical SHA-256: 009dab73992997d1a59ed3330938b8601737e8f7846a527550b9b4c04905360a

SO_ZO_E01__randomized__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/reason; canonical SHA-256: ba85dbe9d6d7f5344fe64a8ddf864a517f35761bb5c26f0e30cc17b943c90105

Strict positive-query region excludes this endpoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/8/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 10

Native pointer: /joint_analysis/comparisons/5/bound_uses/9; canonical SHA-256: 571106caf99ea0b2c1e22db7cde1322aa560fd242373ec72e75864f655f9be5b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/9/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/9/bound_id; canonical SHA-256: d1035bd08e969a0de5da5cbf458056ccaff2b9d1c6bc08cb4e759ba6ad6c83d6

SO_ZO_E01__randomized__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/9/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/9/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/9/reason; canonical SHA-256: ba85dbe9d6d7f5344fe64a8ddf864a517f35761bb5c26f0e30cc17b943c90105

Strict positive-query region excludes this endpoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/9/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 11

Native pointer: /joint_analysis/comparisons/5/bound_uses/10; canonical SHA-256: feb148db504edd121ed551a82e0b4d5bf9427ee3dab9a46205d367c65fd8c196

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/10/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/10/bound_id; canonical SHA-256: 4e5284261539c79664ee5eede28cf229c0111b5926085deb886b6ba64745277c

SO_ZO_E01__randomized__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/10/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/10/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/10/reason; canonical SHA-256: f944eeb5bb30040e6edba34f72e7bc1587c81c17cd75551d601d6f1a430975bc

Disjoint from A<=1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/10/validity_region; canonical SHA-256: 9a88ee3d6a85c8ea900e4dd748a275e8d32c7dc9a2553494a9fd4aaacbb4cd2b

Native R2 and A>=64

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: 5712c8ac21243f97092fcf9847273646169e0507ae39836645c55b4f771e773b

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: cc5b549212619d2837c2e8b5050da5d9c444cf7e0c42a867d3cc4d13a7b2cb18

A=1 is included.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/boundary_checks/1; canonical SHA-256: 3189f1d2eae9102feed3a242f186aa878261f4d44d7861d9445d822b948179bd

The center has gap at most LR deterministically, hence also under the randomized guarantee.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/boundary_checks/2; canonical SHA-256: 8822eac7b104d01941213c58823ccd07e705fa12048fd70fed2fd5952d07325f

No multiplicative ratio is defined at zero cost.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: 19fdc946a4ebcfb2ca21bd4aa776423ddf2ec498c147ae5ccbf5786457a80f84

not applicable: exact cost zero

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: 288db1e792d284d5ac4888faa0600668e556e21badb3f69fa56aea2f2bbc75e5

None on this certified zero-query region.

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native item 7

Native pointer: /joint_analysis/comparisons/6; canonical SHA-256: 3436137c9a35a48a1d5cbcbbd2d1325c69df7a9398966416eca3bf2c09644af1

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/6/bound_uses; canonical SHA-256: 2a4e0d826b0444bd1163b15b18ccb8bb481f99e83f90f77b8fb1855b494a4914

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0; canonical SHA-256: abf440ba3fee55dad93419f95965f0f3a20dc0aafb5928ccdcbf7a053f204f64

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/bound_id; canonical SHA-256: 4e37783ad562a293bffb78fa32c08b157f082850700320ab1070814cbfb40bcc

SO_ZO_E01__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/reason; canonical SHA-256: 578160ac1d5dbe245767a9fea98acea91b5ee424305eb54f0831f759c0109da7

At d=1, the retained ternary search already has O(log(4A)) cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/validity_region; canonical SHA-256: 6d04d8354585ae9e63e63353ce1c2f269031c454a31bb12eaa63bb207c16aefe

Native localization guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/1; canonical SHA-256: d117ae2c39584e9a63608f2190a6be9de63315b36222dacc568340b8ce9629dd

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/bound_id; canonical SHA-256: 51b0c2324078b3f4453114cbca82e09925a62434ab1cac2f04866fcf20d16c12

SO_ZO_E01__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/reason; canonical SHA-256: 44c730ddd77feadafb9baed47516f8e200378f4ac0a44c948c7f407f1b0eab5a

Its localization branch has the same logarithmic slice rate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/validity_region; canonical SHA-256: cff1a838ecee5cad7d35ad831f9aae5f4a5ba2362652b7db54a17dc48181cd98

A>=8

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/bound_uses/2; canonical SHA-256: c543c1a8147335ee3d3c6ce097ad84db05c31581051fb85e9c58fb78015f3092

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/bound_id; canonical SHA-256: 91c4f33bfebb6e4a43a9c030f3663ce4e7dc2714f65e01cc6271c57d5f650a3c

SO_ZO_E01__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/reason; canonical SHA-256: 1a6d21133bcc50256fee1950130c58ba24a159a57ed5210b47475831d17358f2

On any valid d=1 overlap, s=1 gives only a constant lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/validity_region; canonical SHA-256: 0e7f252cc3aab682af8178c182a5372371f84043e4bd8b60a20db5bc37bf2faf

d>=d_0, epsilon<=c LR; c universal.

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/bound_uses/3; canonical SHA-256: aa506e7758039ae95089cddf5f8370144c891f85cab6dc62a21c7813746bce43

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/bound_id; canonical SHA-256: 85193dba0957a13c1033a96541c4fddfcaada85e081c435f44fa65120eb2f2e6

SO_ZO_E01__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/reason; canonical SHA-256: 0b99e3f273083af8fd8b6a6c29bac394f7dfdf7a94728da894d5149bfd8be4cf

Different quantity ID; no transfer adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/validity_region; canonical SHA-256: ed8027370766a357fad538fc25abe54f808f2320bd48d4476e22169f50ea0f04

Distinct q2; retained smooth-subclass guard.

#### Native item 5

Native pointer: /joint_analysis/comparisons/6/bound_uses/4; canonical SHA-256: 97e6897fb101c9d0685a731ade8fda3c3d1aea889291f6c2569f3e751c2b965b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/bound_id; canonical SHA-256: 585eaefd845b615b59f44dc3e3daa168b482980b77b6e8d05aba33c233b18e23

SO_ZO_E01__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/reason; canonical SHA-256: 14091c116d32897aba592bde4d6a73ff318f1fc6bd6c9ac1b43e736c4b2ecf67

Subsumed by the retained logarithmic slice lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/validity_region; canonical SHA-256: 5e6fb74eb2259b00aa72ad0f6199abcfc57275c37a165f6ff1eb6292ba76ea99

A>=98304

#### Native item 6

Native pointer: /joint_analysis/comparisons/6/bound_uses/5; canonical SHA-256: 5139c76b37bee7e1531b7388ac604775ae1d0915b8525bda0f020671207256f1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/bound_id; canonical SHA-256: 1e4cb2aeb9db919a5cb9d0b181c1c4cab6ac311d089601d56bef5a9042edb3f6

SO_ZO_E01__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/reason; canonical SHA-256: db2d0d67192589e6dff6efa975b5509d94027aa61bbad0122f6f2016fefa6f30

The slice is strict A>1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 7

Native pointer: /joint_analysis/comparisons/6/bound_uses/6; canonical SHA-256: 55f63ba0fec5d57b35534e63b25cecb51118f7249c460a93e3bc67c580935828

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/bound_id; canonical SHA-256: 0b9b494e575e3718b55b00b87fb4094988b5dd30fbfb997ba738c4b9d990ef17

SO_ZO_E01__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/reason; canonical SHA-256: db2d0d67192589e6dff6efa975b5509d94027aa61bbad0122f6f2016fefa6f30

The slice is strict A>1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 8

Native pointer: /joint_analysis/comparisons/6/bound_uses/7; canonical SHA-256: 8c0a6d6d97f6b80921be4eef1452a34f7112b7f84d9cbebacb09a518667f4091

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/adopted_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/bound_id; canonical SHA-256: 29c3ff41867d52d86767fe0f709299914d78c94644d8a2f5290ee09e3f32e942

SO_ZO_E01__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/mapping_proof_refs; canonical SHA-256: 85af83b6220c98da3cbcfe06e0d12e40ea455247aa52b9eeceb98b0fc87ebb22

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: f9f6aa4c790d095f8ab63c10f8a9d57a7e5d6c296cf91292be357b1aac39a948

ZO_PROOF_UNIVARIATE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/reason; canonical SHA-256: cb512b5679cd0b318a04044c325ebf94a27dc9736c77a7347df9da564a9cd348

Conditional native ternary-search upper.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 9

Native pointer: /joint_analysis/comparisons/6/bound_uses/8; canonical SHA-256: 90617ed9679eb501d6cfa5825d53e62acd524e07627891055342e4d9cce32cab

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/adopted_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/bound_id; canonical SHA-256: 4fed4bb5fb50e132630c6ad9c724da2cedd9fd4d79b7da1336e77c7c77249682

SO_ZO_E01__deterministic__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/mapping_proof_refs; canonical SHA-256: f1f0398ddbb9756304a1417e49dbe08a767db10fff10302f2ad087a4d1f41626

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/mapping_proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/mapping_proof_refs/1; canonical SHA-256: f9f6aa4c790d095f8ab63c10f8a9d57a7e5d6c296cf91292be357b1aac39a948

ZO_PROOF_UNIVARIATE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/reason; canonical SHA-256: 50d1c5bf2d6e474385757ccaa9b454fc4f4e72735dd7c7a5ab4d7fb995980283

Conditional native combined logarithmic/nontriviality lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/8/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 10

Native pointer: /joint_analysis/comparisons/6/bound_uses/9; canonical SHA-256: bfdd35b1d318057ef805ee27a100fce9b1ef6bb5ca064fa0b6af0369c06ffdc2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/9/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/9/bound_id; canonical SHA-256: 109b0b4392439ae92d3f51969a606e4a2fc115912606c8243d0b978d29776529

SO_ZO_E01__deterministic__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/9/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/9/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/9/reason; canonical SHA-256: 0c93e24e38bce74bab0094d0b0336e8e7bac7d8620d69e955ccb4334b1e5ce88

On any d=1 overlap, it gives only a constant lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/9/validity_region; canonical SHA-256: 9a88ee3d6a85c8ea900e4dd748a275e8d32c7dc9a2553494a9fd4aaacbb4cd2b

Native R2 and A>=64

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/6/boundary_checks; canonical SHA-256: 6ee33e59a2bdc85f358f5b271b758a9a3efcea3e5bb033a11a8bf39cad1a2d6d

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/boundary_checks/0; canonical SHA-256: c1fed6708c5a39714284485fa1012e267546a8832239c7fd6a45fed7c4f308a0

A=1 is excluded and belongs to c3.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/boundary_checks/1; canonical SHA-256: 5f62bca8a1f14b0f3644f3b662ebb772546aaf67419db57931795346b15dfdf5

The fixed cap is 2 ceil(log(A)/log(3/2)); the feasible midpoint needs no query.

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/boundary_checks/2; canonical SHA-256: 5fb8e47063832b107f08b7532c222939c2184ca9dbcd026fa8f273a084fcde0a

The retained source logarithmic lower activates at A>=98304. Below that fixed threshold, disjoint success sets for f_+(x)=Lx and f_-(x)=-Lx exclude zero-query 2/3 success, providing the retained uniform constant lower.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/6/comparison_id; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/6/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/6/fixed_parameters; canonical SHA-256: 301acb4f5004c0881664b935f257cdfd789aaa7fe2132313e9fc532a773b49ad

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/fixed_parameters/0; canonical SHA-256: dacec2e8665d5c3ad69a6a1ae1b65197a76efc3794d2c551fd6118cb92f2ea21

d=1

#### Native field: gap

Native pointer: /joint_analysis/comparisons/6/gap; canonical SHA-256: 130c5e78cbaacb2af30fa4de81b23e8ae42f27df8cbbf58339b0ae17f4acc57b

O(1)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/6/lower_envelope; canonical SHA-256: 4aaa9467fc7f8402522fd6a2921cdfee025faa279cb472279eb2a67d7b4a96dc

Omega(log(4A))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/6/remaining_gap; canonical SHA-256: c72ad85ff2160a40eb09ebb5256d4d351530346ea051701098c65e423b9b4131

Constant-factor bracket on this slice; no higher-dimensional conclusion.

#### Native field: role

Native pointer: /joint_analysis/comparisons/6/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/6/slice; canonical SHA-256: 9fe4f63138aa7c585d771a9cfe634339f0662e266ceaeb6353bf6364b63cffee

d=1, A>1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/6/upper_envelope; canonical SHA-256: 73efc267726e7fbe9aa57150f7772b4e44587018f6efa25c83f040bc11f720a4

O(log(4A))

#### Native item 8

Native pointer: /joint_analysis/comparisons/7; canonical SHA-256: 8cb4a8eada7a1609d4eed19d240dcb4889c57bf2d1075426acaa658277876cd6

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/7/bound_uses; canonical SHA-256: 7ab4231313da1c432c77441058dad531aa62139243ced71cb9c405adc0375c06

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/0; canonical SHA-256: aa1f90d0e4357595d82649492cb1bdcb02f5d4c32dba4bca1dd025797ef94de8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/bound_id; canonical SHA-256: b9c7f56e25e3e08b596022bb36e790258080b32af8decc0b50087a2b6ff90927

SO_ZO_E01__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/reason; canonical SHA-256: 15d103ab80844d49b7367711be5eda7b6a192cd08dfadd2fc092697f1b2131b9

On d=1, its minimum does not improve the retained logarithmic rate asymptotically.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/validity_region; canonical SHA-256: 2bdf80b9cc2b06876c5689e7dbc617873e29eb95b59d61d4cdad124a91f8f146

Native two-point/localization guards.

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/bound_uses/1; canonical SHA-256: 36fd170a8221f0505b87325e232e75efd8bc033626d557196b3ce1cf46ea5214

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/bound_id; canonical SHA-256: 748af08626701be2e969b459261cfb09e59137d39833aa230fce151c8ddf829d

SO_ZO_E01__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/reason; canonical SHA-256: c05f05d7c6ac78863ae4cf7e16df68e193e4814212153a1de8d3d0af97cebfe5

Same logarithmic slice rate as the active upper.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/validity_region; canonical SHA-256: 6d04d8354585ae9e63e63353ce1c2f269031c454a31bb12eaa63bb207c16aefe

Native localization guard.

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/bound_uses/2; canonical SHA-256: b57966c79dfbbe22fd121a593433fb631b38aadeb1177e4cede9a6de84712bcf

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/bound_id; canonical SHA-256: ad6cdb72cb3bc8024fbc5e48eb87d1bc456f496507a8cf2ecb886c2397e11e60

SO_ZO_E01__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/reason; canonical SHA-256: 44c730ddd77feadafb9baed47516f8e200378f4ac0a44c948c7f407f1b0eab5a

Its localization branch has the same logarithmic slice rate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/validity_region; canonical SHA-256: cff1a838ecee5cad7d35ad831f9aae5f4a5ba2362652b7db54a17dc48181cd98

A>=8

#### Native item 4

Native pointer: /joint_analysis/comparisons/7/bound_uses/3; canonical SHA-256: 0e2c4274164b3428364a0ede9a261cfa5abd2291e8698a3d216388b462f8d7c4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/bound_id; canonical SHA-256: c66dc5d6937c5845c51a4228f56119db61de4418e1612c8257e68cdb977845cb

SO_ZO_E01__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/reason; canonical SHA-256: 1a6d21133bcc50256fee1950130c58ba24a159a57ed5210b47475831d17358f2

On any valid d=1 overlap, s=1 gives only a constant lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/validity_region; canonical SHA-256: 0e7f252cc3aab682af8178c182a5372371f84043e4bd8b60a20db5bc37bf2faf

d>=d_0, epsilon<=c LR; c universal.

#### Native item 5

Native pointer: /joint_analysis/comparisons/7/bound_uses/4; canonical SHA-256: dcec63bfb468c7555ff92ba40bdbe243cd76b625cdb2ca08c963b72bdcafd595

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/bound_id; canonical SHA-256: 2183f558c0fe14497d4050ab913bb0bf1d30f55a505c97db68209f561442486e

SO_ZO_E01__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/reason; canonical SHA-256: 0b99e3f273083af8fd8b6a6c29bac394f7dfdf7a94728da894d5149bfd8be4cf

Different quantity ID; no transfer adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/validity_region; canonical SHA-256: ed8027370766a357fad538fc25abe54f808f2320bd48d4476e22169f50ea0f04

Distinct q2; retained smooth-subclass guard.

#### Native item 6

Native pointer: /joint_analysis/comparisons/7/bound_uses/5; canonical SHA-256: 884db501ac9be949d561edddda71a53a3127a878535013a58ce8b9e7b7736c9e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/bound_id; canonical SHA-256: 737e6cbf953f3c73d6e2e21c94dfd4a9eba71aa19745ba7c8707b08c76d1b95d

SO_ZO_E01__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/reason; canonical SHA-256: 14091c116d32897aba592bde4d6a73ff318f1fc6bd6c9ac1b43e736c4b2ecf67

Subsumed by the retained logarithmic slice lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/validity_region; canonical SHA-256: 5e6fb74eb2259b00aa72ad0f6199abcfc57275c37a165f6ff1eb6292ba76ea99

A>=98304

#### Native item 7

Native pointer: /joint_analysis/comparisons/7/bound_uses/6; canonical SHA-256: cbc53e8c674bfb497555641b2d41e6136f0bf6d9f905ae65ec103158eef6cdef

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/bound_id; canonical SHA-256: 24f60c818d1dfd1ca48eaacb0e6de83285b686375919325037df14be34e73cb0

SO_ZO_E01__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/reason; canonical SHA-256: db2d0d67192589e6dff6efa975b5509d94027aa61bbad0122f6f2016fefa6f30

The slice is strict A>1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 8

Native pointer: /joint_analysis/comparisons/7/bound_uses/7; canonical SHA-256: dd43c30f017aa667c55c0114442d033918329a0def66160aeaf567a0cfc45bc8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/bound_id; canonical SHA-256: c702c9264613cec20640c97bf35c33bc7b818c69ca163a0bf15002918f83599c

SO_ZO_E01__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/reason; canonical SHA-256: db2d0d67192589e6dff6efa975b5509d94027aa61bbad0122f6f2016fefa6f30

The slice is strict A>1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/7/validity_region; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 9

Native pointer: /joint_analysis/comparisons/7/bound_uses/8; canonical SHA-256: 4a4cf5af8abc5e816c6b3224dfbba23c4e269aa65e4ea5b5c9ddab0aa7746a13

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/adopted_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/bound_id; canonical SHA-256: 009dab73992997d1a59ed3330938b8601737e8f7846a527550b9b4c04905360a

SO_ZO_E01__randomized__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/mapping_proof_refs; canonical SHA-256: 85af83b6220c98da3cbcfe06e0d12e40ea455247aa52b9eeceb98b0fc87ebb22

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/mapping_proof_refs/0; canonical SHA-256: f9f6aa4c790d095f8ab63c10f8a9d57a7e5d6c296cf91292be357b1aac39a948

ZO_PROOF_UNIVARIATE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/reason; canonical SHA-256: d66bd351523591d2e95985451792b00b19a800a8af2a12a3048ce5e5ab052f83

Retained deterministic upper succeeds with probability one.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/8/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 10

Native pointer: /joint_analysis/comparisons/7/bound_uses/9; canonical SHA-256: 294425a602ca1e76e404d296a26a8219436622c1664b6edf6d7a13f5d85a3303

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/9/adopted_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/9/bound_id; canonical SHA-256: d1035bd08e969a0de5da5cbf458056ccaff2b9d1c6bc08cb4e759ba6ad6c83d6

SO_ZO_E01__randomized__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/9/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/9/mapping_proof_refs; canonical SHA-256: f1f0398ddbb9756304a1417e49dbe08a767db10fff10302f2ad087a4d1f41626

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/9/mapping_proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/bound_uses/9/mapping_proof_refs/1; canonical SHA-256: f9f6aa4c790d095f8ab63c10f8a9d57a7e5d6c296cf91292be357b1aac39a948

ZO_PROOF_UNIVARIATE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/9/reason; canonical SHA-256: 8b63f36a56287fea32e37e8e71375cf096b675b0270aaf3eef9450eb32a18440

Conditional native lower for pointwise 2/3 success.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/9/validity_region; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 11

Native pointer: /joint_analysis/comparisons/7/bound_uses/10; canonical SHA-256: 41e9bfcaff5bd01a08cbec9158dedd81b21e4f63444e78213fec1c316347c222

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/10/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/10/bound_id; canonical SHA-256: 4e5284261539c79664ee5eede28cf229c0111b5926085deb886b6ba64745277c

SO_ZO_E01__randomized__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/10/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/10/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/10/reason; canonical SHA-256: 0c93e24e38bce74bab0094d0b0336e8e7bac7d8620d69e955ccb4334b1e5ce88

On any d=1 overlap, it gives only a constant lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/10/validity_region; canonical SHA-256: 9a88ee3d6a85c8ea900e4dd748a275e8d32c7dc9a2553494a9fd4aaacbb4cd2b

Native R2 and A>=64

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/7/boundary_checks; canonical SHA-256: 71a5d906d5e41fae4e96b46a33bab81a8a0a9f5d4f23d564dead45da49d2b441

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/boundary_checks/0; canonical SHA-256: c1fed6708c5a39714284485fa1012e267546a8832239c7fd6a45fed7c4f308a0

A=1 is excluded and belongs to c3.

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/boundary_checks/1; canonical SHA-256: eb9c900e244049d6381eb75b2364c85231d8619409e54366824555f48ccc0391

The deterministic ternary-search cap is fixed on every execution path, preserving the randomized view's budget convention.

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/boundary_checks/2; canonical SHA-256: b93ba66771b3e75da8ab878ee426d23d612c2d16c52cee55f0b7c7d5f7d1b6cc

A common zero-query output distribution cannot put probability >=2/3 in both disjoint affine success sets when A>1; the retained large-A logarithmic source bound handles A>=98304.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/7/comparison_id; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/7/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/7/fixed_parameters; canonical SHA-256: 301acb4f5004c0881664b935f257cdfd789aaa7fe2132313e9fc532a773b49ad

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/fixed_parameters/0; canonical SHA-256: dacec2e8665d5c3ad69a6a1ae1b65197a76efc3794d2c551fd6118cb92f2ea21

d=1

#### Native field: gap

Native pointer: /joint_analysis/comparisons/7/gap; canonical SHA-256: 130c5e78cbaacb2af30fa4de81b23e8ae42f27df8cbbf58339b0ae17f4acc57b

O(1)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/7/lower_envelope; canonical SHA-256: 4aaa9467fc7f8402522fd6a2921cdfee025faa279cb472279eb2a67d7b4a96dc

Omega(log(4A))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/7/remaining_gap; canonical SHA-256: c72ad85ff2160a40eb09ebb5256d4d351530346ea051701098c65e423b9b4131

Constant-factor bracket on this slice; no higher-dimensional conclusion.

#### Native field: role

Native pointer: /joint_analysis/comparisons/7/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/7/slice; canonical SHA-256: 9fe4f63138aa7c585d771a9cfe634339f0662e266ceaeb6353bf6364b63cffee

d=1, A>1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/7/upper_envelope; canonical SHA-256: 73efc267726e7fbe9aa57150f7772b4e44587018f6efa25c83f040bc11f720a4

O(log(4A))

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 7481f43ee5d9ceaaf53aa3a802d476e1e61a23e36e9e1fe370dc0b9b375d9f73

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: e03ec5bf2e8816ecabf16c53eb66725e1f90be2ee9f365ecddcaf04440e8351e

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 56d0aab90383195ea250939a8db7bdca10546094f47749d1fac9a378505423c8

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

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 71612f8ad6cdd66a11dfd5b262ddae09d50f5504d9d7396ef6b3b25a44ecc6a5

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: db802e52a2c73fa02997de9652ace8cdee849e3fa86278a89f3b09528833de32

Exact cost zero, including A=1.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: e2061bb3fa23199c3f5c285602b24e78c6bb95faf823dd2ce9f8fb1d8c7b4e78

d>=1 AND 0<A<=1

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: b56d468e4b8d7ae1cb49f4641d1a2659073d638e1cba68956ac88889990b25cb

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: d3d795aa120c03a78e11f42d5835db9d8e4ff6e657fe97f13332eaa1f73c7370

univariate

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: f1f0398ddbb9756304a1417e49dbe08a767db10fff10302f2ad087a4d1f41626

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/1; canonical SHA-256: f9f6aa4c790d095f8ab63c10f8a9d57a7e5d6c296cf91292be357b1aac39a948

ZO_PROOF_UNIVARIATE

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: c5848aeecb1517d72da341b5a00b48a83ecef56c8e4a988ef593a33c103018d8

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 849b9a91bcef7ac6d1b2a119d20e87e72462f9bd5659f1fc01edb3144b7d19e4

Secondary fixed-dimension slice. Any R2 overlap allowed by the retained source thresholds is rate-compatible; no numerical value of d_0 is inferred.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 77e983e03806e4dc7556ece54d31b762cdaaf8490a80da8fb7fafc759dfbd022

d=1 AND A>1

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 4fc7be39b4ee930fb1709825f6722c6695c69eb97bf614b69e74f7ddcc65c8ad

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 5521d24b8cf3e07b14fc0809677f011541551f586aa45b3c2b902d3c3f1ead0f

R1

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: bc63bd6e8d4b3896308a1fb37f3e265f44f8969763bd3499f9a843641d312296

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/1; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 937a3c759af539caa8428a6632423ed295f23b5979d437c0f6e95c0e8596ad6f

Retain all bound-specific source guards. Equality A^2=d belongs here.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 568a05ed697c0b663ab2d8b119db5c1f35a28b84e949daff575f4abb74268c9e

d>=2 AND A>1 AND d>=d_0 AND A>=C AND C>=8 AND A^2<=d

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

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: 0bff82db3a3208815c545916ccbffbbd9db10fb837cfc287b3ed3abd678be714

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: 85bd79b38a3e0897c5ad9341ccbc1f3849bf83273bb68ba12783fae76a287669

R2

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 1e5c2cca0cea0f966871731a63b761ee8f9dea6f35d0aa8c3fd8109ff458e266

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/1; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: 26fb7d7916920f5b4e33c81afaedc206419b31ee0bfbf563f4b860602c326190

Brackets remain conditional on native applicability/claim guards; this cell does not extend any theorem.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 5bf70371b5475b5e762cb1e69d2cf8efe839125a91c8382c03171e0886889b77

d>=2 AND A>1 AND d>=d_0 AND A>=C AND A^2>d

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

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: 8cd555525f52078fb647d7a5c522db3a5cf110dc2dc383296a4a49ee5ddf31bc

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: ef9670ac75858f70360100ba43d68692b8a287ac8864f9cf3f34c50c91bff22b

residual

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: 04da513d0a997b25bad14046caab8e9c7df3cae65ecdb86dc8d72d525339388f

No complete bracket assembled. Small dimensions and intermediate accuracy outside registered windows are unassessed, not proved open.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: 0c7efcfe0023aefe77785e28f68358a9b7d55f8af6ec14fb7a464ef591ea374a

d>=2 AND A>1 AND NOT[(d>=d_0 AND A>=C AND C>=8 AND A^2<=d) OR (d>=d_0 AND A>=C AND A^2>d)]

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 718803b94b4fb410ba421cd3193fac62cb3cce2894bdff2048717cdfc3b14c8f

Split A<=1 from A>1, then d=1 from d>=2. On d>=2,A>1, R1 and R2 are disjoint by A^2<=d versus A^2>d; their logical complement is the residual cell. Thus every target pair is accounted for, including explicitly unassessed parameters. Source-guard intersections remain necessary within recorded cells; comparison labels do not certify broader applicability.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 88426ab8daf601d125a6dcc5ba243368a2db441324d603bae52f72570528fba2

The residual cell and any portions excluded by retained bound-specific source guards. No scientific assessment of this complement is claimed.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 8db63a02cbae5d8e04e8c5ca92e02fb4a070b455b7add0942a349275569d945f

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: ce7e2d53312668a1f9cb9a03553d4ff909adc5d75d6e15af9bddc34b07dbf32f

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 8cdcbbcbff625d2f6327ece66ead3184de2b407343965d01fdad693ae5f7c3ca

Only the analysis representation changes. Existing q1 tracked parameters suffice; q2 identities remain excluded. No normalization or native scientific patch is required.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 13a31168910945e74304b2c2644c3fe127ff47c56bb706a4be6a706639cc67ea

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/0/comparison_ids/2; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/impact/0/comparison_ids/3; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/impact/0/comparison_ids/4; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/impact/0/comparison_ids/5; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/impact/0/comparison_ids/6; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native item 8

Native pointer: /joint_analysis/impact/0/comparison_ids/7; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: fa718ef71ff34bb914b38f26ed298bddd1df0e5e0ec7f7ccc24b4ef0a902d4cf

E01_JOINT_ANNOTATION_V1

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 43ef7f8cb6c1deee6a0d1153bdb20aeb00a2531213b58dca2acfabef4c76f98c

none in oracle cost; interpretation only

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 7a335f0b88cac619de9d74f13bc1d6f91754f7beffa35a0701c30f17dcc50ffd

Identical scientific brackets with explicit joint target, candidate dispositions, secondary slices, endpoint checks and unassessed complement.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 7e057b5379a0bd7b8ce304b0dce0c7341bbd460d9a2663e4e21f327f5b03df27

Eight native scientific brackets with an unresolved joint-analysis template.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 823ee80dba0d68d62c40d8170955e486aef49f47482dbe9a9f5587450706da6b

All eight native comparisons, scientific rows, active references, guards, envelopes and statuses.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 6f98f70d9f8056f91db4d283475b67d66e5652a9a43dd690f57a4f2c9dfcefe3

Full fixed target domain; each native bound remains restricted to its original guard.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 2884fbc50874f8251c646f741e3b3e1f64812b4103b69290ac66fd84c2c32390

A=d^2 and A=exp(d^2) are joint parameter sequences; d=1 is a secondary slice.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 5c7e4de6c6630e3f03e331ef5dbd38166a556958d2fa361d1de428bcd65e609a

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: a012e470ea16be885f20dfbef089c06f9eb671a5ff11d31239476cf0a58f777a

The source supports existing claims or an equal Euclidean nonsmooth rate, yielding no new bracket delta.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: f9da32718ee2f0de6e4ea227caf2ccb4fc8691fa81edb7f2316d7f6a0fc09686

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/impact/1/comparison_ids/3; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: e2baa54a944f965b08af30405dc8bd3b7fab942db4ef8bfcedeb81aa0fb0056b

E01_DORN_2610_EXISTING_ENVELOPE

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 0063dcfbe80c5e4bda424d8d9a7a5e584d6d75e2bd54a57feeae535880a2f075

unchanged

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: dff6f5b287a89023317a63dcf6376186216a130aebd66102d5c7139a1f328963

Retained R1 brackets and guarded R2 maximum of d^2/log(ed), d min(d,sqrt A) at A>=64, and d log A at A>=98304.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 45e88ccaef07c404bdcadee5e46890208fdd9e843f534de45b09e8630c618615

All registered main-rate comparisons.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 3b9ce608aaa38790facdda4e840d26de17337fae3b0d93f3cb650c315bafda88

Original source and native applicability intersections, with calibrated activation thresholds retained.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 4b40c3185617030ae13635e6f0c1e242bb01344603d0597662432a2997730b18

At A=d^2 the smooth lower is already active; Theorem 3.3 retains d s/log(e s).

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 94aefb35cc5452f5cdd181d5fe274cfc07392453eb6b1e8f4b3fe14e719dd9c6

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 1f3fce63604eb8d2ab620bfddf831c54e128e98efad157e20504b1bc57deea7c

On R1, log(e A^2)=O(A^(3/2)) makes d sqrt A no stronger than d A^2/log(e A^2). On R2 use the registered smooth lower at A>=64 and the coarse d^2/log(ed) lower below 64. Its smooth upper does not cover the target class.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: e3a3da5cfd59563ac6b3a1110cb89c92fe5d03789eb047f1bfdd6d412c1e9417

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 2c5a6559ff808737e396ce72c55d474d750b37ed75bf2e5f48c45032717b7c67

E01_SMOOTH_2609_18230V2

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: a213e61707166129d011ad90cfc65a19474c33371279257b0b78878cd1de8af9

none on registered comparisons

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 0063dcfbe80c5e4bda424d8d9a7a5e584d6d75e2bd54a57feeae535880a2f075

unchanged

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 2b41ae5e5ece661d835e0a8fc942f6bf0a900b73820385e96fc25e6e0e0fa9d4

Existing deterministic R1 and R2 guarded brackets.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 459f7e0665fb0e35643083110871ba8a91081f8587a0f3c67c8cbaa78f877bf4

Both deterministic main-rate comparisons; no randomized lower is inferred.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 94a6564792140dd6487ffb75eba91d83ccd9ba8c29bd1c0a99e96b13e595d1b8

Source deterministic smooth subclass with its own dimension/accuracy thresholds; beta_h=2L/(3R), Q=2A/3.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 7bdad9207c077c9856a90b2b0be355625f3dc0bc9cc09b551656e600f1b8267a

The candidate is at most d min(sqrt A,d); for 1<A<64 it is O(d).

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: c111773a6ed017c8da14c35bbfadb3d0e57babd2122f6a7788edddced598527e

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: c110b95459b17b5e65cf9f8b74c94e88ae7a9aaf17ae55a94c521e069bc56ef7

The extra cap only weakens the preceding dominated candidate. Restricted upper bounds and deterministic lower bounds give no stronger nonsmooth randomized target rate.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: e3a3da5cfd59563ac6b3a1110cb89c92fe5d03789eb047f1bfdd6d412c1e9417

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 03cc845ba529f3ac1ce7f3f4f15510145baf16ec9a21a2d4ef73400dd49a6735

E01_STRONGLY_SMOOTH_2609_18728V2

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: a213e61707166129d011ad90cfc65a19474c33371279257b0b78878cd1de8af9

none on registered comparisons

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 0063dcfbe80c5e4bda424d8d9a7a5e584d6d75e2bd54a57feeae535880a2f075

unchanged

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: 2b41ae5e5ece661d835e0a8fc942f6bf0a900b73820385e96fc25e6e0e0fa9d4

Existing deterministic R1 and R2 guarded brackets.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: ca8aec01edef35d06689b741991e9a17ed75d43daf29a2b7bc9bd689fb09978e

Both deterministic main-rate comparisons.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: bf7de53ebab6f654a4020c8df62afa4a1e3e0a2112e06b2cd54623d9a76e9fe1

Source deterministic smooth strongly convex subclass under its own thresholds; Q=2A/3. kappa is a subclass choice, not a target parameter.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 28bc91f3cb5b18281f5f2eef6adf2a829fdc1b07eea25dc3e4a999b8b8aae859

min(sqrt Q,sqrt kappa,D_d)<=min(sqrt Q,D_d), D_d=(d/log(ed))^(1/3).

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: 5335916f9d53735963314322b2c03206ff901fd84936a674fcb609c291d7fdc7

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 82ad21831e5823d21add25baf8dbc12b0bbe0afc6c9339aedbb1202444ba4cfb

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 13a31168910945e74304b2c2644c3fe127ff47c56bb706a4be6a706639cc67ea

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/4/comparison_ids/2; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/impact/4/comparison_ids/3; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/impact/4/comparison_ids/4; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/impact/4/comparison_ids/5; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/impact/4/comparison_ids/6; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native item 8

Native pointer: /joint_analysis/impact/4/comparison_ids/7; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: ea919fc68328e76fa42db3ca20b2e3eae2bfe28b45de0ae1b43e920298628969

curated_feedback_SO_ZO_E01_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: c1bc8ce079ce281ff9852dd72f30cfc5628caf907ff83723297ed87304f41a18

For each existing q1 quantity and its own view/guarantee, minimize the fixed worst-case number of exact scalar values over arbitrary adaptive algorithms. Deterministic correctness and randomized pointwise private-seed success >=2/3 remain separate. Domain: integer d>=1, L,R,epsilon>0, equivalently d>=1 and A>0. Queries and output lie in B_2(0,R); no regularity outside it is assumed. The invertible scaling h(y)=f(Ry)/(LR) gives unit radius, unit Lipschitz modulus and tolerance 1/A with one scalar call per query and unchanged guarantees. Thus d and A vary jointly without hiding dimension or precision in constants. Proof thresholds are universal fixed constants. Distinct q2 identities are outside adoption. All retained asymptotic envelopes below retain their native applicability and claim guards.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: 8c05de8562d4d252e6c473d85a64c86a0d53edf1b0349d5a62e929ebf0f9f312

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 27f13269515265b1342c5f746170f0138e34ac988e3697d1c69e363782cc4706

The exact previously adopted science is conditionally retained. Correct only open-cell closure-publication metadata to the current explicit unassessed convention; no bound, guard, comparison, scientific contract or summary changes. Grouped cross-ID opportunities remain unassessed pending work, without any adopted reduction. This is presentation restructuring, not a new theorem or blind research.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: 13a31168910945e74304b2c2644c3fe127ff47c56bb706a4be6a706639cc67ea

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/5/comparison_ids/2; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/impact/5/comparison_ids/3; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/impact/5/comparison_ids/4; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/impact/5/comparison_ids/5; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/impact/5/comparison_ids/6; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native item 8

Native pointer: /joint_analysis/impact/5/comparison_ids/7; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: 99817b6917cc2e32ecf455321060c96fd88cbaaa4edaf45972c662f214f80623

curated_feedback_SO_ZO_E01_20261116_42b1a1bbfb

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/5/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/5/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/5/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: c1bc8ce079ce281ff9852dd72f30cfc5628caf907ff83723297ed87304f41a18

For each existing q1 quantity and its own view/guarantee, minimize the fixed worst-case number of exact scalar values over arbitrary adaptive algorithms. Deterministic correctness and randomized pointwise private-seed success >=2/3 remain separate. Domain: integer d>=1, L,R,epsilon>0, equivalently d>=1 and A>0. Queries and output lie in B_2(0,R); no regularity outside it is assumed. The invertible scaling h(y)=f(Ry)/(LR) gives unit radius, unit Lipschitz modulus and tolerance 1/A with one scalar call per query and unchanged guarantees. Thus d and A vary jointly without hiding dimension or precision in constants. Proof thresholds are universal fixed constants. Distinct q2 identities are outside adoption. All retained asymptotic envelopes below retain their native applicability and claim guards.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 9362fbc0e1820dc6d71841ba0be17523a20e63d759a649a64caa6dedb7de70e9

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 8fdb40fce4b3a5621b15149fb467d89cc88ea9bc9904cc202a62586fe1db9e27

Assemble and verify brackets on the explicit residual domain, including source-guard complements, before claiming scientific assessment there.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: cee9c53382cbe0b9959aa528fa81c37e76dd2dfc2ab02445f59b0f70598139d2

Literature outside the three recorded queries and fresh authentication of unchanged baseline external premises were not undertaken; these are scope limits, not evidence that stronger bounds are absent.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 82282b3d7aedac39e42fbb2d791ec6a62a242ba196d87604c437b08a29f61aa6

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E01__deterministic__b4 to SO_ZO_E01__deterministic__c1, SO_ZO_E01__deterministic__c2, SO_ZO_E01__deterministic__c3, SO_ZO_E01__deterministic__c4; no transfer is adopted by this metadata inventory.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: a0a065e6900eed6c721966cc79dd0108d9ebb80c6213cf7b86beca80e580aa9c

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E01__randomized__b5 to SO_ZO_E01__randomized__c1, SO_ZO_E01__randomized__c2, SO_ZO_E01__randomized__c3, SO_ZO_E01__randomized__c4; no transfer is adopted by this metadata inventory.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 72f2ca3a64faa50eae426395d784c5c5373723add830b5cc36834de982cb7d7a

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: b324d6cb1fc3d1ab01907adbe7ca0c3bce55fd0ac5003e0aa3e7d27d043907ff

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 4e37783ad562a293bffb78fa32c08b157f082850700320ab1070814cbfb40bcc

SO_ZO_E01__deterministic__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: d26972f2dada92df66138314b11b1f344e342d782ddb7f5a0e445894b54d4956

Unchanged view, guarantee, q1, resource and guards; no fresh certification.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 07e73b3b6e04b56c81645a46eace11fee6420eff52f96141ea3f94ecc8f59c20

Frozen source statement retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 9dac8e5e525abe8424f5158911212202561666282ad27c96401652ed050d1864

/bounds/0; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: afe187f3be4db81d4b193c8a2c5076055a0f310fb0d5c7839d30f66b59332f42

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 2

Native pointer: /joint_analysis/provenance/0/source_refs/1; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 6d04d8354585ae9e63e63353ce1c2f269031c454a31bb12eaa63bb207c16aefe

Native localization guard.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: b79f0acd0aede40222adc6505a41a754efd6561cd74111e3e7afcf9cfe15ba3c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 51b0c2324078b3f4453114cbca82e09925a62434ab1cac2f04866fcf20d16c12

SO_ZO_E01__deterministic__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 33a7e301929e826d3699f83921f82de7e7be2e001030ce821b0bdb8d3a0715ad

Unchanged view, guarantee, q1, resource and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 7f788e7f368cb53f707d594f905f1b89c250bf666716f06d31fa258719ccb621

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 29752edcd4a7fa866faff0ef568ca1dc0a68b75bcc6a5909624ffdf893ffa241

ZO_PROOF_DET_SUBGRAD

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 29cc6cafaea1818c562150ec86c830f57f72207a715eac238698b20bfda69a09

Frozen derivation retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 05cba6aaeca3c4f3ba91a7b80ccf081b1e73486f4a450d7f98024a262b24bef7

/bounds/1; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: afe187f3be4db81d4b193c8a2c5076055a0f310fb0d5c7839d30f66b59332f42

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 2

Native pointer: /joint_analysis/provenance/1/source_refs/1; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 882e59eee049ab9e842a89469ef50661d9b73bdc39207731dccbce68e859a821

A>=8; feasible probes.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: a4876ea210dd48437a719a127dc588ac10da15f10886e29c159d6600ab9a0ac5

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 91c4f33bfebb6e4a43a9c030f3663ce4e7dc2714f65e01cc6271c57d5f650a3c

SO_ZO_E01__deterministic__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: b9590e60d11c2d22c363cbba7ad98a0404e23716429b423c61ddd52e36c23f6f

Unchanged lower scope, q1, resource and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 07e73b3b6e04b56c81645a46eace11fee6420eff52f96141ea3f94ecc8f59c20

Frozen source statement retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 7fca5544eac45027cee65d438b55e828ac4260589aa1c2da0464890841da4d1a

/bounds/2; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 8516f076d8160f0b10b9db08a587b15a99445ecb1c2a870a91f1b4cda99adc00

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 0e7f252cc3aab682af8178c182a5372371f84043e4bd8b60a20db5bc37bf2faf

d>=d_0, epsilon<=c LR; c universal.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: aa831036f9acfef64c0963e317fa8ffeb0b7fe37f78b7078d76454369320e70b

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: 585eaefd845b615b59f44dc3e3daa168b482980b77b6e8d05aba33c233b18e23

SO_ZO_E01__deterministic__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 604f3d4829bcda8792fd18e09b6ab557de18134460d030c3e8f57f2607f2e541

No new transfer or envelope adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: e6fec3f7796e10d8ba70af3b1071bff78a3b8434f5317fb6e3fb2df5c9ef8f6d

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: ec29979b549dc2c7ec9ad1a7e0991f1278bf743f80af65d04d592c2d30c132fc

Frozen subclass transfer retained.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 45a45e7abdca201b7ae516642d11ac378e76a5ad0c605160cdc377269df10802

/bounds/4; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/3/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 5e6fb74eb2259b00aa72ad0f6199abcfc57275c37a165f6ff1eb6292ba76ea99

A>=98304

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 5b057d17f6b9b3fffbbac47db5840e105d9bcdf7ee5c03c5b02412540cc0dc60

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: 1e4cb2aeb9db919a5cb9d0b181c1c4cab6ac311d089601d56bef5a9042edb3f6

SO_ZO_E01__deterministic__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: 9fcb7b328db23b2dc571395753ac125ab990b444d3cf477c2ed5bd1004fef243

Unchanged zero-query upper.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 1d6c42a3e2752c771b481b322641a82cd8a434929bd4f16c792914d7a346b3b6

Frozen center certificate.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: 8b694185e8cb2f1ef4326dc6cf2a91aa2428eaaf72adf5168499ae2bd906e17e

/bounds/5; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: 49eb4b4564d9b501019515b9d8f84c485ee43f070977d6404211d62c06170802

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: 0b9b494e575e3718b55b00b87fb4094988b5dd30fbfb997ba738c4b9d990ef17

SO_ZO_E01__deterministic__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 6456f4f6fd6c3acdc31800cadff15a91075f1fdae539c87652d66e718d020f28

Unchanged zero lower.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: cb97b6e53be5796be3c1543fe64495fb7383860dd3558539e14ac17cc59ccaf1

Frozen nonnegative-cost certificate.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: adc3b293548e4ce46a3aa06e0db554cdd0deaa0672129c817079ac4af35e1c70

/bounds/6; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: 26ac900d549a2ff15442a1c911bb8d614baa845b44b246272d5954f3989f984c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: b9c7f56e25e3e08b596022bb36e790258080b32af8decc0b50087a2b6ff90927

SO_ZO_E01__randomized__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: dd5d9976a0310857bd8d0720dd66733b19ca69defad7d351178f9baaf75b16a1

Unchanged randomized q1, fixed budget and success convention.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: 8dd92640cc4779637f589f98334bd50b5b5885c563f304df1a78080af40702ae

Frozen two-point/localization envelope retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: d8dfdec09e315bf46c223927f9263249954d29c44333a9d2095af2fa53876f8f

/bounds/7; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: c1224ed93ea280c1dd1a190faa729a304dee2d8a6ac1b577f02fbf6f10871b80

#### Native item 1

Native pointer: /joint_analysis/provenance/6/source_refs/0; canonical SHA-256: 7ec8d4ed8f91c132a1de87534a55d39252f47d06682b98ca5b170368ee0a8388

SO_SRC_072506cc03b2f8a7

#### Native item 2

Native pointer: /joint_analysis/provenance/6/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 3

Native pointer: /joint_analysis/provenance/6/source_refs/2; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 5d6a959d05876645d83d20fe2969c93bd452244b8c6583c165d112a1330ec799

Native branch and guarantee guards.

#### Native item 8

Native pointer: /joint_analysis/provenance/7; canonical SHA-256: bc812691a8beaa89e5afa10b4b15cb790fc4d05a9237581f1f5feb249dc2119e

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/7/bound_id; canonical SHA-256: 748af08626701be2e969b459261cfb09e59137d39833aa230fce151c8ddf829d

SO_ZO_E01__randomized__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/7/mapping; canonical SHA-256: e6321dcb4f550db695211beaec24f748e885b3771f0ff290bbedc096477d9a53

Unchanged deterministic algorithm admitted in randomized view.

#### Native field: origin

Native pointer: /joint_analysis/provenance/7/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/7/source_domain; canonical SHA-256: fb1ef7f24377767ce530b60a242dedf14cb78f9e8b785d636015f4e2c0ad4a79

Frozen localization statement retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/7/source_locator; canonical SHA-256: 199870bff58061504ccbce88313846d18a0fa7535dc6c75120ba42ded2606450

/bounds/8; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/7/source_refs; canonical SHA-256: afe187f3be4db81d4b193c8a2c5076055a0f310fb0d5c7839d30f66b59332f42

#### Native item 1

Native pointer: /joint_analysis/provenance/7/source_refs/0; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 2

Native pointer: /joint_analysis/provenance/7/source_refs/1; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/7/target_domain; canonical SHA-256: 6d04d8354585ae9e63e63353ce1c2f269031c454a31bb12eaa63bb207c16aefe

Native localization guard.

#### Native item 9

Native pointer: /joint_analysis/provenance/8; canonical SHA-256: 6f7d7b24149bb73efc081d1775e722195c48035d0604faef780d7f2ed5bc4652

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/8/bound_id; canonical SHA-256: ad6cdb72cb3bc8024fbc5e48eb87d1bc456f496507a8cf2ecb886c2397e11e60

SO_ZO_E01__randomized__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/8/mapping; canonical SHA-256: 39cde189dadd0c2596463f075ec617397c574e91a3a149a4bcb0dbedf01754a0

Unchanged deterministic branch in randomized view.

#### Native field: origin

Native pointer: /joint_analysis/provenance/8/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/8/proof_refs; canonical SHA-256: 7f788e7f368cb53f707d594f905f1b89c250bf666716f06d31fa258719ccb621

#### Native item 1

Native pointer: /joint_analysis/provenance/8/proof_refs/0; canonical SHA-256: 29752edcd4a7fa866faff0ef568ca1dc0a68b75bcc6a5909624ffdf893ffa241

ZO_PROOF_DET_SUBGRAD

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/8/source_domain; canonical SHA-256: 29cc6cafaea1818c562150ec86c830f57f72207a715eac238698b20bfda69a09

Frozen derivation retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/8/source_locator; canonical SHA-256: c4c1d3f0f7cb64494006502cd8a3f7250c2871d1f0c9f81ac4f9d76fbf2e739f

/bounds/9; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/8/source_refs; canonical SHA-256: afe187f3be4db81d4b193c8a2c5076055a0f310fb0d5c7839d30f66b59332f42

#### Native item 1

Native pointer: /joint_analysis/provenance/8/source_refs/0; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 2

Native pointer: /joint_analysis/provenance/8/source_refs/1; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/8/target_domain; canonical SHA-256: 882e59eee049ab9e842a89469ef50661d9b73bdc39207731dccbce68e859a821

A>=8; feasible probes.

#### Native item 10

Native pointer: /joint_analysis/provenance/9; canonical SHA-256: 14dc21d669e64ff6a4fb96a26f63f72f96210bbd233e2825fd19787ac33790a7

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/9/bound_id; canonical SHA-256: c66dc5d6937c5845c51a4228f56119db61de4418e1612c8257e68cdb977845cb

SO_ZO_E01__randomized__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/9/mapping; canonical SHA-256: 50e353b8762f5149dd6d395224c877ea31b5f8ac98909ac9bea688d05ad08ab5

Unchanged randomized lower scope, q1 and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/9/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/9/source_domain; canonical SHA-256: 07e73b3b6e04b56c81645a46eace11fee6420eff52f96141ea3f94ecc8f59c20

Frozen source statement retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/9/source_locator; canonical SHA-256: 964caf17e1936e922f9464e9be3d72aa2bd6bf8c3641a9054af2220e0ceba838

/bounds/10; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/9/source_refs; canonical SHA-256: 8516f076d8160f0b10b9db08a587b15a99445ecb1c2a870a91f1b4cda99adc00

#### Native item 1

Native pointer: /joint_analysis/provenance/9/source_refs/0; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/9/target_domain; canonical SHA-256: 0e7f252cc3aab682af8178c182a5372371f84043e4bd8b60a20db5bc37bf2faf

d>=d_0, epsilon<=c LR; c universal.

#### Native item 11

Native pointer: /joint_analysis/provenance/10; canonical SHA-256: 2f21886d6d9eeed704dd10ddc7a516450e5edd8023ec96d7d3120e322b17078c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/10/bound_id; canonical SHA-256: 737e6cbf953f3c73d6e2e21c94dfd4a9eba71aa19745ba7c8707b08c76d1b95d

SO_ZO_E01__randomized__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/10/mapping; canonical SHA-256: 604f3d4829bcda8792fd18e09b6ab557de18134460d030c3e8f57f2607f2e541

No new transfer or envelope adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/10/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/10/proof_refs; canonical SHA-256: e6fec3f7796e10d8ba70af3b1071bff78a3b8434f5317fb6e3fb2df5c9ef8f6d

#### Native item 1

Native pointer: /joint_analysis/provenance/10/proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/10/source_domain; canonical SHA-256: ec29979b549dc2c7ec9ad1a7e0991f1278bf743f80af65d04d592c2d30c132fc

Frozen subclass transfer retained.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/10/source_locator; canonical SHA-256: f6ca59065df7a4fc7fcfc9d5bd86b5fc65b7213d575c0f3b31bdb97ad4279b3c

/bounds/12; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/10/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/10/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/10/target_domain; canonical SHA-256: 5e6fb74eb2259b00aa72ad0f6199abcfc57275c37a165f6ff1eb6292ba76ea99

A>=98304

#### Native item 12

Native pointer: /joint_analysis/provenance/11; canonical SHA-256: eceaeeebf24551c89e27055c4e5380a22cd9f6c15cdc9f6d13a7bea3d12e7b6c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/11/bound_id; canonical SHA-256: 24f60c818d1dfd1ca48eaacb0e6de83285b686375919325037df14be34e73cb0

SO_ZO_E01__randomized__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/11/mapping; canonical SHA-256: c9ae4d0b6da06a35185697b5d95d402a1f1936df5192b050f2437f1274959509

Unchanged sure-success zero-query upper.

#### Native field: origin

Native pointer: /joint_analysis/provenance/11/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/11/proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/provenance/11/proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/11/source_domain; canonical SHA-256: 1d6c42a3e2752c771b481b322641a82cd8a434929bd4f16c792914d7a346b3b6

Frozen center certificate.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/11/source_locator; canonical SHA-256: efa92cf8741f1940d4a9d6f3573c7c748d90d07de7aaecfb6f080480411e0036

/bounds/13; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/11/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/11/target_domain; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 13

Native pointer: /joint_analysis/provenance/12; canonical SHA-256: 6e0abab7f492aac5148b1ca03558d8997f9460a68fce42c0fcbed78027a49785

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/12/bound_id; canonical SHA-256: c702c9264613cec20640c97bf35c33bc7b818c69ca163a0bf15002918f83599c

SO_ZO_E01__randomized__b8

#### Native field: mapping

Native pointer: /joint_analysis/provenance/12/mapping; canonical SHA-256: 6456f4f6fd6c3acdc31800cadff15a91075f1fdae539c87652d66e718d020f28

Unchanged zero lower.

#### Native field: origin

Native pointer: /joint_analysis/provenance/12/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/12/proof_refs; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /joint_analysis/provenance/12/proof_refs/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/12/source_domain; canonical SHA-256: cb97b6e53be5796be3c1543fe64495fb7383860dd3558539e14ac17cc59ccaf1

Frozen nonnegative-cost certificate.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/12/source_locator; canonical SHA-256: 4fb533da832b89a598ad4499e7a7ab005c939f5d4c1c5936efa4e78e0bebd7e0

/bounds/14; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/12/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/12/target_domain; canonical SHA-256: 6e399084d7309b2f8e6bc9d827b6ed826ea150b340964b78beacc3cd7aeb2d94

A<=1

#### Native item 14

Native pointer: /joint_analysis/provenance/13; canonical SHA-256: f3fae291ea2939325a9311f03d3b9b3d6c710360e7c5a5f4898300c51e151c10

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/13/bound_id; canonical SHA-256: 29c3ff41867d52d86767fe0f709299914d78c94644d8a2f5290ee09e3f32e942

SO_ZO_E01__deterministic__b8

#### Native field: mapping

Native pointer: /joint_analysis/provenance/13/mapping; canonical SHA-256: e92b486cb6dbdfe5d269b35a1b8cc71e9d81938b2e56f7115d0158719a4234ba

Unchanged deterministic slice upper.

#### Native field: origin

Native pointer: /joint_analysis/provenance/13/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/13/proof_refs; canonical SHA-256: 85af83b6220c98da3cbcfe06e0d12e40ea455247aa52b9eeceb98b0fc87ebb22

#### Native item 1

Native pointer: /joint_analysis/provenance/13/proof_refs/0; canonical SHA-256: f9f6aa4c790d095f8ab63c10f8a9d57a7e5d6c296cf91292be357b1aac39a948

ZO_PROOF_UNIVARIATE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/13/source_domain; canonical SHA-256: 192a8f5194f67f732443909a5c5e68c6482d24a333ed8e6e34c42658ac7a172f

Frozen ternary-search derivation.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/13/source_locator; canonical SHA-256: ff0a9b83968ca420701ebf5d035a19bdc5040784b2f9d7eeb43bf1f73a5ab71d

/bounds/15; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/13/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/13/target_domain; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 15

Native pointer: /joint_analysis/provenance/14; canonical SHA-256: 3d6479e44e95f21998235885dc276614f1434c29dad6e39fcb25edfe1e51cecc

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/14/bound_id; canonical SHA-256: 4fed4bb5fb50e132630c6ad9c724da2cedd9fd4d79b7da1336e77c7c77249682

SO_ZO_E01__deterministic__b9

#### Native field: mapping

Native pointer: /joint_analysis/provenance/14/mapping; canonical SHA-256: 1fd024fa9d9daca10b9bab0bd9546df387380219ce2f2cf4f40c61fd65fde867

Unchanged deterministic slice lower.

#### Native field: origin

Native pointer: /joint_analysis/provenance/14/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/14/proof_refs; canonical SHA-256: f1f0398ddbb9756304a1417e49dbe08a767db10fff10302f2ad087a4d1f41626

#### Native item 1

Native pointer: /joint_analysis/provenance/14/proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native item 2

Native pointer: /joint_analysis/provenance/14/proof_refs/1; canonical SHA-256: f9f6aa4c790d095f8ab63c10f8a9d57a7e5d6c296cf91292be357b1aac39a948

ZO_PROOF_UNIVARIATE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/14/source_domain; canonical SHA-256: 0344260ffd8dddf81506831af2d4760e057c91408fc6eb087439a5fe1945446e

Frozen logarithmic/nontriviality combination.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/14/source_locator; canonical SHA-256: b4007f74f9003c0733027638afb8fe3e71619079af7ff0d7d8b9b1634a466bc0

/bounds/16; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/14/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/14/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/14/target_domain; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 16

Native pointer: /joint_analysis/provenance/15; canonical SHA-256: 74c54d31d427c822578b27e02eef5c64470dbc16cbc5104d91972afb13fbd26b

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/15/bound_id; canonical SHA-256: 009dab73992997d1a59ed3330938b8601737e8f7846a527550b9b4c04905360a

SO_ZO_E01__randomized__b9

#### Native field: mapping

Native pointer: /joint_analysis/provenance/15/mapping; canonical SHA-256: 4286005a1928f66baadaf42851c20167c1eb44b3973ee5ab3f6ccec55d1ecb3e

Unchanged deterministic algorithm under randomized guarantee.

#### Native field: origin

Native pointer: /joint_analysis/provenance/15/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/15/proof_refs; canonical SHA-256: 85af83b6220c98da3cbcfe06e0d12e40ea455247aa52b9eeceb98b0fc87ebb22

#### Native item 1

Native pointer: /joint_analysis/provenance/15/proof_refs/0; canonical SHA-256: f9f6aa4c790d095f8ab63c10f8a9d57a7e5d6c296cf91292be357b1aac39a948

ZO_PROOF_UNIVARIATE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/15/source_domain; canonical SHA-256: 192a8f5194f67f732443909a5c5e68c6482d24a333ed8e6e34c42658ac7a172f

Frozen ternary-search derivation.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/15/source_locator; canonical SHA-256: 85305520a94cfb05f6e2c645211e3111113f1773ef8462b18b70d0c3d7acdec1

/bounds/17; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/15/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/15/target_domain; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 17

Native pointer: /joint_analysis/provenance/16; canonical SHA-256: a46e9ddbcdea4fe425a23406d018597dc026b93485da191403e5c188f12d2514

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/16/bound_id; canonical SHA-256: d1035bd08e969a0de5da5cbf458056ccaff2b9d1c6bc08cb4e759ba6ad6c83d6

SO_ZO_E01__randomized__b10

#### Native field: mapping

Native pointer: /joint_analysis/provenance/16/mapping; canonical SHA-256: c2b2957f49f2723387526fa78f042a4543459cb460d07c90213db32c5374bcd4

Unchanged randomized slice lower.

#### Native field: origin

Native pointer: /joint_analysis/provenance/16/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/16/proof_refs; canonical SHA-256: f1f0398ddbb9756304a1417e49dbe08a767db10fff10302f2ad087a4d1f41626

#### Native item 1

Native pointer: /joint_analysis/provenance/16/proof_refs/0; canonical SHA-256: 617a24ce79b83a835edc0c7bea9496dd09b7b1994f5030eea9056f527fe82b10

ZO_PROOF_PRECISION_LOG

#### Native item 2

Native pointer: /joint_analysis/provenance/16/proof_refs/1; canonical SHA-256: f9f6aa4c790d095f8ab63c10f8a9d57a7e5d6c296cf91292be357b1aac39a948

ZO_PROOF_UNIVARIATE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/16/source_domain; canonical SHA-256: 0344260ffd8dddf81506831af2d4760e057c91408fc6eb087439a5fe1945446e

Frozen logarithmic/nontriviality combination.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/16/source_locator; canonical SHA-256: 5fd1629a60f868fd5e7e165472c07e94c02996ca2bcf8daa3cfed7a47e268e25

/bounds/18; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/16/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/16/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/16/target_domain; canonical SHA-256: 9c067312cac13ae4bd93c58e60fbd9eb70e9e892abb9f3c0bd9a79565dc60562

d=1,A>1

#### Native item 18

Native pointer: /joint_analysis/provenance/17; canonical SHA-256: 50c11325c4acf7f02f8acbdce4de75a1e3adb332c120a69b2b5f72f8de55813b

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/17/bound_id; canonical SHA-256: 109b0b4392439ae92d3f51969a606e4a2fc115912606c8243d0b978d29776529

SO_ZO_E01__deterministic__b10

#### Native field: mapping

Native pointer: /joint_analysis/provenance/17/mapping; canonical SHA-256: 6000213fa86e12fb8cd35cf4a0d65c86dea05fa8e56df612cd5c1705079bd87b

Existing cost-preserving restriction retained; no new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/17/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/17/proof_refs; canonical SHA-256: b6b614de1cc1e62370415f950d585eb48d2106a76b076be1ee73061e83f64e52

#### Native item 1

Native pointer: /joint_analysis/provenance/17/proof_refs/0; canonical SHA-256: 71a4e2e3071d17a19caa3068c71a150f2b37f9f277b2105d06cceb6fd5cd20d8

ZO_PROOF_SMOOTH_SUBCLASS

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/17/source_domain; canonical SHA-256: 960c6b6ce9e422cf762d9a6a825c43922505303b0a1e011d0517ea1bd78421fa

Frozen smooth-subclass transfer.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/17/source_locator; canonical SHA-256: 2dd84f8d3ff9d56f4cbf87dcc104299678341756c2bd31405df43b4d66505d86

/bounds/19; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/17/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/17/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/17/target_domain; canonical SHA-256: 9a88ee3d6a85c8ea900e4dd748a275e8d32c7dc9a2553494a9fd4aaacbb4cd2b

Native R2 and A>=64

#### Native item 19

Native pointer: /joint_analysis/provenance/18; canonical SHA-256: c4e130f2f6ebfd571a5803667caa5deb8d6ec4c8763db191db441dbb9f2c160d

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/18/bound_id; canonical SHA-256: 4e5284261539c79664ee5eede28cf229c0111b5926085deb886b6ba64745277c

SO_ZO_E01__randomized__b11

#### Native field: mapping

Native pointer: /joint_analysis/provenance/18/mapping; canonical SHA-256: 6000213fa86e12fb8cd35cf4a0d65c86dea05fa8e56df612cd5c1705079bd87b

Existing cost-preserving restriction retained; no new adoption.

#### Native field: origin

Native pointer: /joint_analysis/provenance/18/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/18/proof_refs; canonical SHA-256: b6b614de1cc1e62370415f950d585eb48d2106a76b076be1ee73061e83f64e52

#### Native item 1

Native pointer: /joint_analysis/provenance/18/proof_refs/0; canonical SHA-256: 71a4e2e3071d17a19caa3068c71a150f2b37f9f277b2105d06cceb6fd5cd20d8

ZO_PROOF_SMOOTH_SUBCLASS

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/18/source_domain; canonical SHA-256: 960c6b6ce9e422cf762d9a6a825c43922505303b0a1e011d0517ea1bd78421fa

Frozen smooth-subclass transfer.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/18/source_locator; canonical SHA-256: 0c1d3f0dedb1ed997741865666d677f3c730df0b57554f73ab5aaf826d5ef94f

/bounds/20; canonical parent hash in E01_JOINT_ANNOTATION_V1

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/18/source_refs; canonical SHA-256: cd81b7d49ba72a81c81ca9ad51a6e07b7af08bbf3a372c0df5adec2776ab75b4

#### Native item 1

Native pointer: /joint_analysis/provenance/18/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/18/target_domain; canonical SHA-256: 9a88ee3d6a85c8ea900e4dd748a275e8d32c7dc9a2553494a9fd4aaacbb4cd2b

Native R2 and A>=64

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 8306c332d49bd51756beb49d223ab665300c9434cb37787d7d67ced560b0cd7f

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 683777f97029a556ed040cfc186602ad740b7a702b54f6bbdb57fbe9d10e0a1d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/6; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/7; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: e0bd884fdc5970f58f41474880bcc3b9242df6dcedf05dc6fa408714369f7200

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: c82069b6e01f3f3fcebfd2c8bf2c9461c50361fd3ced6e50692d00f4ef10bb3b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 41534440e82c020456181e3b391ed640648e081fefe15459dde3eb2af5ce6011

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 4e37783ad562a293bffb78fa32c08b157f082850700320ab1070814cbfb40bcc

SO_ZO_E01__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 109b0b4392439ae92d3f51969a606e4a2fc115912606c8243d0b978d29776529

SO_ZO_E01__deterministic__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 51b0c2324078b3f4453114cbca82e09925a62434ab1cac2f04866fcf20d16c12

SO_ZO_E01__deterministic__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: 91c4f33bfebb6e4a43a9c030f3663ce4e7dc2714f65e01cc6271c57d5f650a3c

SO_ZO_E01__deterministic__b3

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/4; canonical SHA-256: 585eaefd845b615b59f44dc3e3daa168b482980b77b6e8d05aba33c233b18e23

SO_ZO_E01__deterministic__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/5; canonical SHA-256: 1e4cb2aeb9db919a5cb9d0b181c1c4cab6ac311d089601d56bef5a9042edb3f6

SO_ZO_E01__deterministic__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/6; canonical SHA-256: 0b9b494e575e3718b55b00b87fb4094988b5dd30fbfb997ba738c4b9d990ef17

SO_ZO_E01__deterministic__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/7; canonical SHA-256: 29c3ff41867d52d86767fe0f709299914d78c94644d8a2f5290ee09e3f32e942

SO_ZO_E01__deterministic__b8

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/8; canonical SHA-256: 4fed4bb5fb50e132630c6ad9c724da2cedd9fd4d79b7da1336e77c7c77249682

SO_ZO_E01__deterministic__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 396d2f04aa0637fe96bb90b7b2d5df1de5cca90ec56a36291e306748065b5e35

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: f0a0bf112a23df5fb981f7c9cda963073b52c6aea50380ca441ee733aac11b40

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 41534440e82c020456181e3b391ed640648e081fefe15459dde3eb2af5ce6011

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 4e37783ad562a293bffb78fa32c08b157f082850700320ab1070814cbfb40bcc

SO_ZO_E01__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 109b0b4392439ae92d3f51969a606e4a2fc115912606c8243d0b978d29776529

SO_ZO_E01__deterministic__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 51b0c2324078b3f4453114cbca82e09925a62434ab1cac2f04866fcf20d16c12

SO_ZO_E01__deterministic__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: 91c4f33bfebb6e4a43a9c030f3663ce4e7dc2714f65e01cc6271c57d5f650a3c

SO_ZO_E01__deterministic__b3

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/4; canonical SHA-256: 585eaefd845b615b59f44dc3e3daa168b482980b77b6e8d05aba33c233b18e23

SO_ZO_E01__deterministic__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/5; canonical SHA-256: 1e4cb2aeb9db919a5cb9d0b181c1c4cab6ac311d089601d56bef5a9042edb3f6

SO_ZO_E01__deterministic__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/6; canonical SHA-256: 0b9b494e575e3718b55b00b87fb4094988b5dd30fbfb997ba738c4b9d990ef17

SO_ZO_E01__deterministic__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/7; canonical SHA-256: 29c3ff41867d52d86767fe0f709299914d78c94644d8a2f5290ee09e3f32e942

SO_ZO_E01__deterministic__b8

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/8; canonical SHA-256: 4fed4bb5fb50e132630c6ad9c724da2cedd9fd4d79b7da1336e77c7c77249682

SO_ZO_E01__deterministic__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: df3f07d17f9f0f343292b29a0e4f9ef6195671f8ecb9dacab63c174213015ff8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: e5b6286016dd41152ea4ce2f4b6dfff9f6d5639b29712fd2149aea7108a80fde

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 41534440e82c020456181e3b391ed640648e081fefe15459dde3eb2af5ce6011

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: 4e37783ad562a293bffb78fa32c08b157f082850700320ab1070814cbfb40bcc

SO_ZO_E01__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 109b0b4392439ae92d3f51969a606e4a2fc115912606c8243d0b978d29776529

SO_ZO_E01__deterministic__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 51b0c2324078b3f4453114cbca82e09925a62434ab1cac2f04866fcf20d16c12

SO_ZO_E01__deterministic__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: 91c4f33bfebb6e4a43a9c030f3663ce4e7dc2714f65e01cc6271c57d5f650a3c

SO_ZO_E01__deterministic__b3

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: 585eaefd845b615b59f44dc3e3daa168b482980b77b6e8d05aba33c233b18e23

SO_ZO_E01__deterministic__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/5; canonical SHA-256: 1e4cb2aeb9db919a5cb9d0b181c1c4cab6ac311d089601d56bef5a9042edb3f6

SO_ZO_E01__deterministic__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/6; canonical SHA-256: 0b9b494e575e3718b55b00b87fb4094988b5dd30fbfb997ba738c4b9d990ef17

SO_ZO_E01__deterministic__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/7; canonical SHA-256: 29c3ff41867d52d86767fe0f709299914d78c94644d8a2f5290ee09e3f32e942

SO_ZO_E01__deterministic__b8

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/8; canonical SHA-256: 4fed4bb5fb50e132630c6ad9c724da2cedd9fd4d79b7da1336e77c7c77249682

SO_ZO_E01__deterministic__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: affa75910f1c8a07ffec55d8f34e8a6b8e68089e3e2f2ef34c076ade95fd145b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 78e1869fa75fd8bd79cbd3a2c4decdace80a328d87daaae5411be07121f34739

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 41534440e82c020456181e3b391ed640648e081fefe15459dde3eb2af5ce6011

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: 4e37783ad562a293bffb78fa32c08b157f082850700320ab1070814cbfb40bcc

SO_ZO_E01__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 109b0b4392439ae92d3f51969a606e4a2fc115912606c8243d0b978d29776529

SO_ZO_E01__deterministic__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: 51b0c2324078b3f4453114cbca82e09925a62434ab1cac2f04866fcf20d16c12

SO_ZO_E01__deterministic__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/3; canonical SHA-256: 91c4f33bfebb6e4a43a9c030f3663ce4e7dc2714f65e01cc6271c57d5f650a3c

SO_ZO_E01__deterministic__b3

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/4; canonical SHA-256: 585eaefd845b615b59f44dc3e3daa168b482980b77b6e8d05aba33c233b18e23

SO_ZO_E01__deterministic__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/5; canonical SHA-256: 1e4cb2aeb9db919a5cb9d0b181c1c4cab6ac311d089601d56bef5a9042edb3f6

SO_ZO_E01__deterministic__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/6; canonical SHA-256: 0b9b494e575e3718b55b00b87fb4094988b5dd30fbfb997ba738c4b9d990ef17

SO_ZO_E01__deterministic__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/7; canonical SHA-256: 29c3ff41867d52d86767fe0f709299914d78c94644d8a2f5290ee09e3f32e942

SO_ZO_E01__deterministic__b8

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/8; canonical SHA-256: 4fed4bb5fb50e132630c6ad9c724da2cedd9fd4d79b7da1336e77c7c77249682

SO_ZO_E01__deterministic__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 2b812e4699de0ee559fca537d078e8a372cf5e1e41525bd76244f4bdf6c363f4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: e780a11e11b8d60a38797719fbf8c1eaea01deeda8a52cb617d4e1df49a9d294

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 087d8e5b2e3c90a454f48497ecd256de90212620cfb85e8da8402359c5e3fc5e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: b9c7f56e25e3e08b596022bb36e790258080b32af8decc0b50087a2b6ff90927

SO_ZO_E01__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: d1035bd08e969a0de5da5cbf458056ccaff2b9d1c6bc08cb4e759ba6ad6c83d6

SO_ZO_E01__randomized__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: 4e5284261539c79664ee5eede28cf229c0111b5926085deb886b6ba64745277c

SO_ZO_E01__randomized__b11

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/3; canonical SHA-256: 748af08626701be2e969b459261cfb09e59137d39833aa230fce151c8ddf829d

SO_ZO_E01__randomized__b2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/4; canonical SHA-256: ad6cdb72cb3bc8024fbc5e48eb87d1bc456f496507a8cf2ecb886c2397e11e60

SO_ZO_E01__randomized__b3

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/5; canonical SHA-256: c66dc5d6937c5845c51a4228f56119db61de4418e1612c8257e68cdb977845cb

SO_ZO_E01__randomized__b4

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/6; canonical SHA-256: 737e6cbf953f3c73d6e2e21c94dfd4a9eba71aa19745ba7c8707b08c76d1b95d

SO_ZO_E01__randomized__b6

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/7; canonical SHA-256: 24f60c818d1dfd1ca48eaacb0e6de83285b686375919325037df14be34e73cb0

SO_ZO_E01__randomized__b7

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/8; canonical SHA-256: c702c9264613cec20640c97bf35c33bc7b818c69ca163a0bf15002918f83599c

SO_ZO_E01__randomized__b8

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/9; canonical SHA-256: 009dab73992997d1a59ed3330938b8601737e8f7846a527550b9b4c04905360a

SO_ZO_E01__randomized__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 6a20ce1a74f4649fd6b16aab006812a0ede38d547e5fc9fa6eba20715ed0a51b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 6fbb13eafea7249029c72f586dc37525296d15054d2ad7aade80f235996cb078

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 087d8e5b2e3c90a454f48497ecd256de90212620cfb85e8da8402359c5e3fc5e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/0; canonical SHA-256: b9c7f56e25e3e08b596022bb36e790258080b32af8decc0b50087a2b6ff90927

SO_ZO_E01__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/1; canonical SHA-256: d1035bd08e969a0de5da5cbf458056ccaff2b9d1c6bc08cb4e759ba6ad6c83d6

SO_ZO_E01__randomized__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/2; canonical SHA-256: 4e5284261539c79664ee5eede28cf229c0111b5926085deb886b6ba64745277c

SO_ZO_E01__randomized__b11

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/3; canonical SHA-256: 748af08626701be2e969b459261cfb09e59137d39833aa230fce151c8ddf829d

SO_ZO_E01__randomized__b2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/4; canonical SHA-256: ad6cdb72cb3bc8024fbc5e48eb87d1bc456f496507a8cf2ecb886c2397e11e60

SO_ZO_E01__randomized__b3

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/5; canonical SHA-256: c66dc5d6937c5845c51a4228f56119db61de4418e1612c8257e68cdb977845cb

SO_ZO_E01__randomized__b4

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/6; canonical SHA-256: 737e6cbf953f3c73d6e2e21c94dfd4a9eba71aa19745ba7c8707b08c76d1b95d

SO_ZO_E01__randomized__b6

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/7; canonical SHA-256: 24f60c818d1dfd1ca48eaacb0e6de83285b686375919325037df14be34e73cb0

SO_ZO_E01__randomized__b7

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/8; canonical SHA-256: c702c9264613cec20640c97bf35c33bc7b818c69ca163a0bf15002918f83599c

SO_ZO_E01__randomized__b8

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/9; canonical SHA-256: 009dab73992997d1a59ed3330938b8601737e8f7846a527550b9b4c04905360a

SO_ZO_E01__randomized__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: a1625bbe072794eedb398b7a45ee72aa15085abb83208ea7e0a844c5ccaecb00

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 78c49e299c4b1905799a05460b8c14b6e6937c8968793bfb796c693b7671a09a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 087d8e5b2e3c90a454f48497ecd256de90212620cfb85e8da8402359c5e3fc5e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/0; canonical SHA-256: b9c7f56e25e3e08b596022bb36e790258080b32af8decc0b50087a2b6ff90927

SO_ZO_E01__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/1; canonical SHA-256: d1035bd08e969a0de5da5cbf458056ccaff2b9d1c6bc08cb4e759ba6ad6c83d6

SO_ZO_E01__randomized__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/2; canonical SHA-256: 4e5284261539c79664ee5eede28cf229c0111b5926085deb886b6ba64745277c

SO_ZO_E01__randomized__b11

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/3; canonical SHA-256: 748af08626701be2e969b459261cfb09e59137d39833aa230fce151c8ddf829d

SO_ZO_E01__randomized__b2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/4; canonical SHA-256: ad6cdb72cb3bc8024fbc5e48eb87d1bc456f496507a8cf2ecb886c2397e11e60

SO_ZO_E01__randomized__b3

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/5; canonical SHA-256: c66dc5d6937c5845c51a4228f56119db61de4418e1612c8257e68cdb977845cb

SO_ZO_E01__randomized__b4

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/6; canonical SHA-256: 737e6cbf953f3c73d6e2e21c94dfd4a9eba71aa19745ba7c8707b08c76d1b95d

SO_ZO_E01__randomized__b6

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/7; canonical SHA-256: 24f60c818d1dfd1ca48eaacb0e6de83285b686375919325037df14be34e73cb0

SO_ZO_E01__randomized__b7

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/8; canonical SHA-256: c702c9264613cec20640c97bf35c33bc7b818c69ca163a0bf15002918f83599c

SO_ZO_E01__randomized__b8

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/9; canonical SHA-256: 009dab73992997d1a59ed3330938b8601737e8f7846a527550b9b4c04905360a

SO_ZO_E01__randomized__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: d7ebf5374639220e7dcd4cf1b807583721431f609b0444bb40875ae110c860fa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: d09db1a90f923e60a87f3fd9d877078cd313c88a927e88ec14be26cc6a13cc87

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 087d8e5b2e3c90a454f48497ecd256de90212620cfb85e8da8402359c5e3fc5e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/0; canonical SHA-256: b9c7f56e25e3e08b596022bb36e790258080b32af8decc0b50087a2b6ff90927

SO_ZO_E01__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/1; canonical SHA-256: d1035bd08e969a0de5da5cbf458056ccaff2b9d1c6bc08cb4e759ba6ad6c83d6

SO_ZO_E01__randomized__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/2; canonical SHA-256: 4e5284261539c79664ee5eede28cf229c0111b5926085deb886b6ba64745277c

SO_ZO_E01__randomized__b11

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/3; canonical SHA-256: 748af08626701be2e969b459261cfb09e59137d39833aa230fce151c8ddf829d

SO_ZO_E01__randomized__b2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/4; canonical SHA-256: ad6cdb72cb3bc8024fbc5e48eb87d1bc456f496507a8cf2ecb886c2397e11e60

SO_ZO_E01__randomized__b3

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/5; canonical SHA-256: c66dc5d6937c5845c51a4228f56119db61de4418e1612c8257e68cdb977845cb

SO_ZO_E01__randomized__b4

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/6; canonical SHA-256: 737e6cbf953f3c73d6e2e21c94dfd4a9eba71aa19745ba7c8707b08c76d1b95d

SO_ZO_E01__randomized__b6

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/7; canonical SHA-256: 24f60c818d1dfd1ca48eaacb0e6de83285b686375919325037df14be34e73cb0

SO_ZO_E01__randomized__b7

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/8; canonical SHA-256: c702c9264613cec20640c97bf35c33bc7b818c69ca163a0bf15002918f83599c

SO_ZO_E01__randomized__b8

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/9; canonical SHA-256: 009dab73992997d1a59ed3330938b8601737e8f7846a527550b9b4c04905360a

SO_ZO_E01__randomized__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 81c64752d20fbfc0e62106898dacb9051814e8db283312759275cd5fb8663f3c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: f8b7fdbd16168056fdee32d4f7df2cc66b9f1edf94b5066452b8ab00fc13a37c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 13a31168910945e74304b2c2644c3fe127ff47c56bb706a4be6a706639cc67ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/2; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/3; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/4; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/5; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/6; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/7; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 8fdb40fce4b3a5621b15149fb467d89cc88ea9bc9904cc202a62586fe1db9e27

Assemble and verify brackets on the explicit residual domain, including source-guard complements, before claiming scientific assessment there.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 189be3a41ad6de36e9dac9fbe60b2e6cea7a4068e22b353cd386f917b0d0e491

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 13a31168910945e74304b2c2644c3fe127ff47c56bb706a4be6a706639cc67ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/2; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/3; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/4; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/5; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/6; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/7; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: cee9c53382cbe0b9959aa528fa81c37e76dd2dfc2ab02445f59b0f70598139d2

Literature outside the three recorded queries and fresh authentication of unchanged baseline external premises were not undertaken; these are scope limits, not evidence that stronger bounds are absent.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: 636202792fe7b07bb4dbc22e1b972987108dae686bca83eb5ee6b41516a2bfc5

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 13a31168910945e74304b2c2644c3fe127ff47c56bb706a4be6a706639cc67ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/2; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/3; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/4; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/5; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/6; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/7; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: 0970b43ccf87312cef3fe6a31364d7362ae4345a40e77ae5e043f6d96cd1c3fe

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: d01819709f509642832efc752070b61055ca95b766bdd2041e0b5629fea1e2e3

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs/0; canonical SHA-256: 85193dba0957a13c1033a96541c4fddfcaada85e081c435f44fa65120eb2f2e6

SO_ZO_E01__deterministic__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: 433daf1399430e912569761f1b62275cdde268f30a3580e8ccf150bb3017b497

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/2; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/3; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: edb9ac5e0c0db21544e22a5ee2d7c75c0a70093cfc01199b9ae3e1d4e618b9e4

possible-projection-262cfe61bdaf

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: 82282b3d7aedac39e42fbb2d791ec6a62a242ba196d87604c437b08a29f61aa6

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E01__deterministic__b4 to SO_ZO_E01__deterministic__c1, SO_ZO_E01__deterministic__c2, SO_ZO_E01__deterministic__c3, SO_ZO_E01__deterministic__c4; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/obligations/12; canonical SHA-256: 1267fab1d76b99c9f476d1a0ff27576fa822f410dea1043ca8cd5f4e370e4a03

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs; canonical SHA-256: d01819709f509642832efc752070b61055ca95b766bdd2041e0b5629fea1e2e3

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs/0; canonical SHA-256: 85193dba0957a13c1033a96541c4fddfcaada85e081c435f44fa65120eb2f2e6

SO_ZO_E01__deterministic__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids; canonical SHA-256: 433daf1399430e912569761f1b62275cdde268f30a3580e8ccf150bb3017b497

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/0; canonical SHA-256: 99d222b0dc404135b7037ab925815e374b3f6f573d180d03e4afd9bca7fd90ae

SO_ZO_E01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/1; canonical SHA-256: b436de241b901b29564e263b0eb01f035dc9fb65d11e754eb8ba2d7c2e83f97e

SO_ZO_E01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/2; canonical SHA-256: 26b6bac6bab167b5f20cdeb91d9bfac0cb9b36e8fcd43ed2e5badf1c088fc3c3

SO_ZO_E01__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/3; canonical SHA-256: 689cbf83ed0a4af2df49aa984ba0fa6ba5a008bc5676e048dcc680fab8c4cb4c

SO_ZO_E01__deterministic__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/id; canonical SHA-256: 663e2af9d7e345f536f03eb3ac2085e6da6ec3bc4ae98d2c72fc99b3d7137abd

possible-projection-262cfe61bdaf-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/lead; canonical SHA-256: 82282b3d7aedac39e42fbb2d791ec6a62a242ba196d87604c437b08a29f61aa6

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E01__deterministic__b4 to SO_ZO_E01__deterministic__c1, SO_ZO_E01__deterministic__c2, SO_ZO_E01__deterministic__c3, SO_ZO_E01__deterministic__c4; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 14

Native pointer: /joint_analysis/synthesis_coverage/obligations/13; canonical SHA-256: 92a63d88f9011b83e68a1a8766890720a358e302a9a0f16785ba717347d5fdc4

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs; canonical SHA-256: 876ba6ee10746c789b0f498d5a2d13b95ffc66ee3ed1e3c3dc49e5e7ebc532a1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/0; canonical SHA-256: 2183f558c0fe14497d4050ab913bb0bf1d30f55a505c97db68209f561442486e

SO_ZO_E01__randomized__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids; canonical SHA-256: 78c7277274f74e646403c61d11413525b3b394362ba938de5641b6888e632dab

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/0; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/1; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/2; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/3; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/id; canonical SHA-256: 57f0530a3b264e463e33643b58e584791069b75710d433c3bf856e4b748b959a

possible-projection-6acc33df4af1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/lead; canonical SHA-256: a0a065e6900eed6c721966cc79dd0108d9ebb80c6213cf7b86beca80e580aa9c

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E01__randomized__b5 to SO_ZO_E01__randomized__c1, SO_ZO_E01__randomized__c2, SO_ZO_E01__randomized__c3, SO_ZO_E01__randomized__c4; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 15

Native pointer: /joint_analysis/synthesis_coverage/obligations/14; canonical SHA-256: f569932ce1f83eea81e0417c9dc6c702112b893d8229eef5afabe3d0f065a18c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs; canonical SHA-256: 876ba6ee10746c789b0f498d5a2d13b95ffc66ee3ed1e3c3dc49e5e7ebc532a1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs/0; canonical SHA-256: 2183f558c0fe14497d4050ab913bb0bf1d30f55a505c97db68209f561442486e

SO_ZO_E01__randomized__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids; canonical SHA-256: 78c7277274f74e646403c61d11413525b3b394362ba938de5641b6888e632dab

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/0; canonical SHA-256: cfff2859f8066b5943c8ea63da5cc9d2beebad7a7aa3d6cb251537cbb7327c1f

SO_ZO_E01__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/1; canonical SHA-256: 010d895fb08cc2c89039b9313348d0f1deff73bdeb0f2eea5f145d048f92035f

SO_ZO_E01__randomized__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/2; canonical SHA-256: 95a9895da0b5b4dfa116db3b2bab78bc1166668b771187a0ae7937429dbe9df9

SO_ZO_E01__randomized__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/3; canonical SHA-256: 4a761cb5722cba820c7b749da1ba448275283d950cf2dc2f4ecd86deb0855fef

SO_ZO_E01__randomized__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/id; canonical SHA-256: b0c3c78d0210250e18995f7897bd6790867bcb71a211c182ce167b929dd9c26d

possible-projection-6acc33df4af1-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/lead; canonical SHA-256: a0a065e6900eed6c721966cc79dd0108d9ebb80c6213cf7b86beca80e580aa9c

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E01__randomized__b5 to SO_ZO_E01__randomized__c1, SO_ZO_E01__randomized__c2, SO_ZO_E01__randomized__c3, SO_ZO_E01__randomized__c4; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 233122ca7263098851fa33e2dd45815947aafa23892af7fefb09292726356d12

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

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

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 921eeb59e7350c0d8667114c84f7d018959742349a6797a84164fdab73bad10b

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 747bd43912b607d598b9338acf799ade2e5ac2dbc867b761a10a21ae89a6a382

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: c649fd913b728542870bb463d3960bb4b15dc96170a65a5e70b9410e2dfa2b66

Fixed universal source dimension threshold d_0>0; not a varying task parameter.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 29976ce88a307a1de717bb9f02f58cec58c66871992571363d3686bc80dbf67f

SO_ZO_E01_p_35084f2651

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: cf6f5b14e83cb68bee414a34e59543d41a8c2c6ad4d4ec2d1f205c7d58e6e887

d_0

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: cd262f6d4189ceaf997e88fdb95fe931b56bbaa315e92652fd56243f61f3a198

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: ab17dadc0da6345c2f0c22ae6cc3732eaf9e3a044a7067aa37277505b35844d4

Fixed universal source applicability threshold C>0; R1 explicitly requires C>=8. All additional native source guards remain required.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: 49fafea693eaf9349d84943e15659c00be046c6f9057aadb2d6c7ea5fe966151

SO_ZO_E01_p_4f002420f8

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: c2e8c0cc2e73b9bd1ba9ef1979e73169b471e25b0e9909efe98fde462c0bf55f

C

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: c1bc8ce079ce281ff9852dd72f30cfc5628caf907ff83723297ed87304f41a18

For each existing q1 quantity and its own view/guarantee, minimize the fixed worst-case number of exact scalar values over arbitrary adaptive algorithms. Deterministic correctness and randomized pointwise private-seed success >=2/3 remain separate. Domain: integer d>=1, L,R,epsilon>0, equivalently d>=1 and A>0. Queries and output lie in B_2(0,R); no regularity outside it is assumed. The invertible scaling h(y)=f(Ry)/(LR) gives unit radius, unit Lipschitz modulus and tolerance 1/A with one scalar call per query and unchanged guarantees. Thus d and A vary jointly without hiding dimension or precision in constants. Proof thresholds are universal fixed constants. Distinct q2 identities are outside adoption. All retained asymptotic envelopes below retain their native applicability and claim guards.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: e8aee203f177d33a036ae8c6b07ead3fda4e584b23e1258da9c956b248e92edc

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 3fa5834dc920d385ca9b099c9fe55dcca163a6b256a261f8f147291b0e7cf633

d

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 798640599597df7a8daa32b1132f07850a68b5e71bd295650399a38074f52804

A

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 18838d8fcf0867583b41f98ae8e2d00a25e93e9d2d36a9d4ade193b4e3a45380

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 7980ef682bbd5fba5f7ca5b3457461afee90448f8b80738e257d45e6687e3c32

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: 9c8d8fea3cfe02005790b9d03d3e472f93e190fd7900ffd067e7b1cf876acb68

LR/epsilon

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: 793c504844af9675f07edfb7637366c94e24367b13d3f14d0479752273744e21

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 88bb899143f5ed56b426e8d02858f958f2c66b41abeb1ca77dd680799c27c926

SO_ZO_E01_p_c4a9342c4d

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 13fed401a95c105e4aa28ff2b191383ba8ce47e7863a11fd397acacd0fc640a8

SO_ZO_E01_p_8686d8c61c

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/2; canonical SHA-256: a409d49134a3f76b16e1178a430672c7fd18bac0bd6101a9299e0ec4367159cb

SO_ZO_E01_p_a4aab29c5f

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/3; canonical SHA-256: 53d1aeb8ab055b402ccdc62cc28be25dcf625486402fe868f5a101917b9ad71e

SO_ZO_E01_p_5c322c6737

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 798640599597df7a8daa32b1132f07850a68b5e71bd295650399a38074f52804

A

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 6c68d0406836aecf440381d679f7d86e7db1cc41302790a98d59d3ede0d09d4c

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 3fa5834dc920d385ca9b099c9fe55dcca163a6b256a261f8f147291b0e7cf633

d

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 798640599597df7a8daa32b1132f07850a68b5e71bd295650399a38074f52804

A

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 8463f556f97cf8fdcda977c053a5ff1b530500723772b0f884160d04256ad2fa

L

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: d7425aeca0691c2fde605cfb1b386316dd4a1ee8705b05fc7fec4557dad77232

R

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: b84b05e599ab42cdaa5ca485a31c57ea891f25c8329539d9b2aaad2aedfa6771

epsilon

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] V. Yu. Protasov. Algorithms for approximate calculation of the minimum of a convex function from its values. Mathematical Notes 59(1):69--74, 1996.

https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper

[3] Haihan Zhang, Chenheng Zhang, Zhiquan Qi and Zhouchen Lin. Near-Optimal Lower Bounds for Randomized Algorithms in Exact Value Zeroth-Order Convex Optimization. arXiv:2607.16558v2, 2026-07-30.

https://arxiv.org/html/2607.16558v2

[4] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. JMLR 18(52):1--11, 2017.

https://jmlr.org/papers/volume18/16-632/16-632.pdf
