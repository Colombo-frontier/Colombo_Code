# Smooth convex finite-sum optimization with selectable exact component values

**Setting ID.** `SO_ZO_E09a`

Single-objective optimization

Minimize $F$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Other quantified gap present

**Gap classes present.** Other quantified gap; Logarithmic gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex components; smoothness: Component gradient lipschitz; structure: Finite sum

**ORACLE tags.** access order: Zeroth-order interface; interface family: Selected component value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $F$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

### Admissible model

$F(x)=n^{-1}\sum_{i=1}^n f_i(x)$, with $n\in\mathbb{N}$. Each component $f_i:\mathbb{R}^d\to\mathbb{R}$ is globally convex.

Every component satisfies $\|\nabla f_i(x)-\nabla f_i(y)\|_2\le\beta\|x-y\|_2$. Component affine terms and gradients at the optimum are unrestricted, and components need not attain minima.

$\operatorname{argmin}F\cap B_2(0,R)\ne\varnothing$.

### Oracle interface

The algorithm may actively choose $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$. The interface $(i,x)\mapsto f_i(x)$ returns one exact component value. Components may be revisited; full-average values must be computed through component calls.

The public inputs are $d$, $n$, $\beta$, $R$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=F(x)-F_*$, where $F_*=\inf_{u\in \mathbb{R}^d}F(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

One $(i,x)\mapsto f_i(x)$ costs $1$ component-value calls; recomputing the full average costs $n$ calls. Every initialization, snapshot and differencing point is charged individually.

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

$n$: Number of finite-sum components **Domain:** $n\in\mathbb{N},\ n\ge1$.

$F=n^{-1}\sum_{i=1}^n f_i$

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$R$: Localization radius for a global minimizer **Domain:** $R>0$.

$x_*\in B_2(0,R)$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$Q$: Smoothness accuracy ratio **Domain:** $Q>0$.

$Q=\beta R^2/\varepsilon$

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

$f_i,i$: Finite-sum components and their indices **Domain:** $f_i:\mathbb{R}^d\to\mathbb{R},\ i\in\{1,\ldots,n\}$.

Components are unknown; indices may be selected actively and revisited at a cost.

$F$: Finite-sum mean objective **Domain:** $F:\mathbb{R}^d\to\mathbb{R}$.

$F=n^{-1}\sum_{i=1}^n f_i$

$F_*$: Optimal value of the finite-sum objective over the optimization domain **Domain:** $F_*\in\mathbb{R}$.

$F_*=\inf_{x\in\mathcal{X}}F(x)$.

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

**Definition.** one exact selected component scalar value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact selected component scalar value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact selected component scalar value

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact selected component scalar value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q5 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact selected component scalar value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q6 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact selected component scalar value

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime E09a.R4

**Region.** $\varepsilon\ge\beta R^2/2$, equivalently $Q\le2$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q4

**Resource.** one exact selected component scalar value

**Status.** Optimal

**Lower bound.** B8, B26

$$
0
$$

**Upper bound.** B7, B25

$$
0
$$

### R2 - Parameter regime E09a.NEW.det_main

**Region.** $n\ge 2,\quad Q\ge512$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact selected component scalar value

**Status.** Other quantified gap

**Lower bound.** B2, B3, B4

$$
\begin{cases}\Omega(d\max\{n,\min(d,\sqrt Q)\}),&Q<128^2,\\\Omega(d\max\{n,\min(d,\sqrt Q),\log Q\}),&Q\ge128^2.\end{cases}
$$

**Upper bound.** B6, B5

$$
O(nd\min\{\sqrt Q,d\log(e+Q)\})
$$

**Gap or comparison.** $O(\min\{n\sqrt Q,nd\log(e+Q)\}/\max\{n,\min(d,\sqrt Q),\log Q\ \mathrm{if}\ Q\ge128^2\})$

### R3 - Single-component identity reduction: regime E03.R1

**Region.** $n=1$; $32\le Q\le d^2$.

**Views.** Deterministic; Randomized

**Quantity.** Q2; Q5

**Resource.** one exact selected component scalar value

**Status.** Optimal

**Lower bound.** B10, B28

$$
\Omega(d\sqrt Q)
$$

**Upper bound.** B9, B27

$$
O(d\sqrt Q)
$$

**Gap or comparison.** $O(1)$

### R4 - Single-component identity reduction: regime E03.R2

**Region.** $n=1$; $Q\ge32,\ Q>d^2$.

**Views.** Deterministic

**Quantity.** Q2

**Resource.** one exact selected component scalar value

**Status.** Logarithmic gap

**Lower bound.** B10, B13

$$
\begin{cases}\Omega(d^2),&Q<128^2,\\\Omega(\max\{d^2,d\log Q\}),&Q\ge128^2.\end{cases}
$$

**Upper bound.** B9

$$
O(\min\{d\sqrt Q,d^2\log Q\})
$$

**Gap or comparison.** $O(\log Q)$

### R5 - Single-component identity reduction: regime E03.R4.part1

**Region.** $n=1$; $2<Q<4$.

**Views.** Deterministic

**Quantity.** Q2

**Resource.** one exact selected component scalar value

**Status.** Optimal

**Lower bound.** B15

$$
\Omega(d)
$$

**Upper bound.** B14

$$
O(d)
$$

**Gap or comparison.** $O(1)$

### R6 - Single-component identity reduction: regime E03.R4.part3

**Region.** $n=1$; $4\le Q<32$.

**Views.** Deterministic; Randomized

**Quantity.** Q2; Q5

**Resource.** one exact selected component scalar value

**Status.** Optimal

**Lower bound.** B11, B29

$$
\Omega(d)
$$

**Upper bound.** B12, B30

$$
O(d)
$$

**Gap or comparison.** $O(1)$

### R7 - Parameter regime E09a.R1

**Region.** $n\ge2$, $Q\ge512$, $n\ge Q$.

**Views.** Randomized

**Quantity.** Q4

**Resource.** one exact selected component scalar value

**Status.** Logarithmic gap

**Lower bound.** B19

$$
\Omega(nd)
$$

**Upper bound.** B22, B23

$$
\widetilde{O}(nd)
$$

**Gap or comparison.** $\operatorname{polylog}(n,d,Q)$

### R8 - Parameter regime E09a.R2

**Region.** $n\ge2$, $Q\ge512$, $n<Q$.

**Views.** Randomized

**Quantity.** Q4

**Resource.** one exact selected component scalar value

**Status.** Other quantified gap

**Lower bound.** B19, B20, B21

$$
\begin{cases}\Omega(d\max\{n,\min(d,\sqrt Q)\}),&Q<128^2,\\\Omega(d\max\{n,\min(d,\sqrt Q),\log Q\}),&Q\ge128^2.\end{cases}
$$

**Upper bound.** B22, B23

$$
\widetilde{O}(d\min\{n+\sqrt{nQ},nd\})
$$

**Gap or comparison.** $\widetilde{O}(\min\{n+\sqrt{nQ},nd\}/\max\{n,\min(d,\sqrt Q),\log Q\ \mathrm{if}\ Q\ge128^2\})$

### R9 - Single-component identity reduction: regime E03.R2

**Region.** $n=1$; $Q\ge32,\ Q>d^2$.

**Views.** Randomized

**Quantity.** Q5

**Resource.** one exact selected component scalar value

**Status.** Logarithmic gap

**Lower bound.** B28, B31

$$
\begin{cases}\Omega(d^2),&Q<128^2,\\\Omega(\max\{d^2,d\log Q\}),&Q\ge128^2.\end{cases}
$$

**Upper bound.** B27

$$
O(\min\{d\sqrt Q,d^2\log Q\})
$$

**Gap or comparison.** $O(\log Q)$

### R10 - Single-component identity reduction: regime E03.R4.part2

**Region.** $n=1$; $2<Q<4$.

**Views.** Randomized

**Quantity.** Q5

**Resource.** one exact selected component scalar value

**Status.** Optimal

**Lower bound.** B34

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Upper bound.** B33

$$
O(\max\{1,d(1-2/Q)\})
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each source component value corresponds to one selectable component query; computing the exact mean requires accessing every component.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Adaptive Gaussian component measurements and a single-function subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(d\max\{n,\min(d,\sqrt Q),\log Q\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $0<\varepsilon\le\beta R^2/512$. The accuracy-dependent term additionally requires the parameter window of its source theorem. The $nd$ term follows from a separate adaptive Gaussian linear-measurement argument.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A4, A5, A6

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; Theorem E.6, PDF page 36: midpoint-curvature contraction ; Theorem 2.1 and Corollary 2.4, PDF pages 3–4 ; Theorem 2.5, PDF/printed page 4

### B2 - Adaptive-measurement lower bound for independent Gaussian components

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(nd)
$$

**Conditions.** $Q\ge512$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

### B3 - Adaptive Gaussian component measurements and a single-function subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt Q\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $Q\ge32$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem2.1; pdf pages: 3; printed pages: 3

### B4 - Multiscale hard family for accuracy dependence

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

**Local argument.** A6

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem2.5; pdf pages: 4; printed pages: 4

### B5 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(nd^2\log(e+Q))
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $Q\ge1$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: AppendixC.2; pdf pages: 29; printed pages: 29

### B6 - Accelerated finite differences of the full average

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(nd\sqrt Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $Q\ge1$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: AppendixC.2; pdf pages: 29; printed pages: 29

### B7 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge\beta R^2/2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A7

### B8 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge\beta R^2/2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A7

### B9 - ARCS variance reduction or acceleration using full-average evaluations

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\min\{d\sqrt Q,d^2\log Q\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $n=1$; coordinate differences with error-tolerant acceleration, or localization by approximate cutting planes.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; pdf pages: 29; printed pages: 29

### B10 - Adaptive Gaussian component measurements and a single-function subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max\{5d/16,(d/4096)\min(d,\sqrt Q)\}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $n=1$ and $0<\varepsilon\le\beta R^2/32$; the hard subclass consists of positive-definite quadratics.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.1; pdf pages: 3; printed pages: 3

### B11 - Adaptive Gaussian component measurements and a single-function subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$; $Q\ge3$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A9, A4

### B12 - ARCS variance reduction or acceleration using full-average evaluations

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$; $4\le Q\le128^2$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A9, A4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; pdf pages: 29; printed pages: 29

### B13 - Multiscale hard family for accuracy dependence

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$; $Q\ge128^2$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A6, A4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5; pdf pages: 4; printed pages: 4

### B14 - Deterministic finite-difference descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$ and $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A8, A4

### B15 - Deterministic hard family with indistinguishable directions

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega(d)
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$ and $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A8, A4

### B16 - Lower bound for estimation of a random spherical center

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$ and $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A8, A4

### B17 - ARCS variance reduction or acceleration using full-average evaluations

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}\!\left(d\min\{n+\sqrt{nQ},nd\}\right)
$$

**Sources.** [2](https://arxiv.org/abs/2109.08858) [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** ARCS runs over the known ball $B(R)$. Linear minimization over this ball is a public computation. Differences may query outside the ball, and the logarithmic factors include $n,Q,d$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

**Source location.** [2](https://arxiv.org/abs/2109.08858) theorem: ARCS, Corollary 6, with localization simulated by full-average evaluations; pdf pages: 9; printed pages: 9

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: ARCS, Corollary 6, with localization simulated by full-average evaluations

### B18 - Adaptive Gaussian component measurements and a single-function subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(d\max\{n,\min(d,\sqrt Q),\log Q\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $0<\varepsilon\le\beta R^2/512$. The accuracy-dependent term additionally requires the parameter window of its source theorem. The $nd$ term follows from a separate adaptive Gaussian linear-measurement argument.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A4, A5, A6

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; Theorem E.6, PDF page 36: midpoint-curvature contraction ; Theorem 2.1 and Corollary 2.4, PDF pages 3–4 ; Theorem 2.5, PDF/printed page 4

### B19 - Adaptive-measurement lower bound for independent Gaussian components

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(nd)
$$

**Conditions.** $Q\ge512$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

### B20 - Adaptive Gaussian component measurements and a single-function subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt Q\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $Q\ge32$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem2.1; pdf pages: 3; printed pages: 3

### B21 - Multiscale hard family for accuracy dependence

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

**Local argument.** A6

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem2.5; pdf pages: 4; printed pages: 4

### B22 - Randomized variance reduction with ARCS

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}(d[n+\sqrt{nQ}])
$$

**Sources.** [2](https://arxiv.org/abs/2109.08858) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $Q\ge1$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

**Source location.** [2](https://arxiv.org/abs/2109.08858) theorem: Corollary6; pdf pages: 9; printed pages: 9

### B23 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(nd^2\log(e+Q))
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $Q\ge1$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: AppendixC.2; pdf pages: 29; printed pages: 29

### B24 - Accelerated finite differences of the full average

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(nd\sqrt Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $Q\ge1$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: AppendixC.2; pdf pages: 29; printed pages: 29

### B25 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge\beta R^2/2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A7

### B26 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge\beta R^2/2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A7

### B27 - ARCS variance reduction or acceleration using full-average evaluations

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\min\{d\sqrt Q,d^2\log Q\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $n=1$; coordinate differences with error-tolerant acceleration, or localization by approximate cutting planes.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; pdf pages: 29; printed pages: 29

### B28 - Adaptive Gaussian component measurements and a single-function subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max\{5d/16,(d/4096)\min(d,\sqrt Q)\}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $n=1$ and $0<\varepsilon\le\beta R^2/32$; the hard subclass consists of positive-definite quadratics.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.1; pdf pages: 3; printed pages: 3

### B29 - Adaptive Gaussian component measurements and a single-function subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$; $Q\ge3$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A9, A4

### B30 - ARCS variance reduction or acceleration using full-average evaluations

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$; $4\le Q\le128^2$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A9, A4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; pdf pages: 29; printed pages: 29

### B31 - Multiscale hard family for accuracy dependence

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log Q)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$; $Q\ge128^2$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A6, A4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.5; pdf pages: 4; printed pages: 4

### B32 - Deterministic finite-difference descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d)
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$ and $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A8, A4

### B33 - Randomized projection descent at critical accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(\max\{1,d(1-2/Q)\})
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$ and $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A8, A4

### B34 - Lower bound for estimation of a random spherical center

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\max\{1,d(1-2/Q)\})
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/abs/2109.08858)

**Conditions.** $n=1$ and $2<Q=\beta R^2/\varepsilon<4$. Exact real-valued queries are allowed throughout the ambient space; $\gamma=1-2/Q$. The number of scalar evaluations has a fixed worst-case cap.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A8, A4

## 5. Local arguments

### A1 - Exact recovery at equal smoothness and strong convexity

**Scope.** Global $\mu$-strong convexity and $\beta$-smoothness with $\mu=\beta$; exact scalar values and unrestricted finite queries.

The objective is $f(x)=\beta\|x\|^2/2-b^\top x+c$. Values at $0,e_1,\ldots,e_d$ recover a minimizer in $d+1$ calls.

Strong monotonicity, Cauchy--Schwarz, and Lipschitz continuity of the gradient imply
$$\beta\|x-y\|^2\le\langle\nabla f(x)-\nabla f(y),x-y\rangle\le\|\nabla f(x)-\nabla f(y)\|\,\|x-y\|\le\beta\|x-y\|^2.$$
Equality throughout forces $\nabla f(x)-\nabla f(y)=\beta(x-y)$. Therefore $b_j=\beta/2+f(0)-f(e_j)$ and $x_*=b/\beta$. For a finite-sum average, each of these $d+1$ average values costs $n$ component values, giving $n(d+1)$ calls. A one-component specialization has $n=1$. Restricted query domains require an admissible nonzero coordinate scale in place of unit vectors.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A2 - An adaptive $nd$ lower bound for selected-component values

**Scope.** Fixed scalar-call cap; arbitrary measurable adaptive randomized queries, including unbounded query points; only the explicitly stated average or component localization promises.

For smooth finite sums, $T>nd/2$ is necessary at $\varepsilon\le\mu R^2/512$. For globally Lipschitz components the same conclusion holds at
$$\varepsilon\le\frac{LRd}{512n[d+\log(16n)]}.$$
The displayed constants give success probability $2/3$; an expected-error transfer uses the same statement at $3\varepsilon$.

Take independent $a_i\sim N(0,s^2I_d)$. A component query, after subtracting a known common term, reveals one linear measurement of $a_i$. Conditional on the random seed and the transcript, the components remain independent Gaussian vectors with covariance $s^2P_i$, where $P_i$ projects onto the complement of the span queried in that component. Hence the mean $\bar a$ has covariance $\Sigma=(s^2/n^2)\sum_iP_i$ and
$$\operatorname{tr}\Sigma\ge s^2(nd-T)/n^2,\qquad\Sigma\preceq(s^2/n)I.$$
For any Gaussian vector $Z$, any proposed center $b$, and $t>0$, Gaussian integration gives $\mathbb E e^{-t\|Z-b\|^2}\le(1+2t\operatorname{tr}\Sigma)^{-1/2}$. Taking $t=1/(2r^2)$ yields
$$\Pr(\|Z-b\|^2\le r^2)\le\sqrt{\frac{er^2}{r^2+\operatorname{tr}\Sigma}}.$$
In particular, $r^2\le\operatorname{tr}\Sigma/8$ makes this at most $\sqrt e/3$.

For the smooth family set $f_i(x)=\mu\|x\|^2/2-\mu\langle a_i,x\rangle$ and $s^2=nR^2/(16d)$. The mean is minimized at $\bar a$. The event $E=\{\|\bar a\|\le R\}$ has probability at least $15/16$. For $T\le nd/2$, $\operatorname{tr}\Sigma\ge R^2/32$. Objective accuracy $\varepsilon$ means squared center error at most $2\varepsilon/\mu$, which is at most $\operatorname{tr}\Sigma/8$ on the displayed window. The unconditional success probability is at most $\sqrt e/3$; conditioning on $E$ only after this calculation bounds valid-instance success by $16\sqrt e/45<2/3$. Choose $\mu=\beta$ for the merely convex smooth class, or the declared $\mu\le\beta$ for the strongly convex class. Individual component centers are not bounded in this construction.

For globally Lipschitz components define the radial Huber function
$$h_R(x)=\begin{cases}\|x\|^2/2,&\|x\|\le R,\\R\|x\|-R^2/2,&\|x\|>R,\end{cases}\quad q=L/(2R),\quad f_i=q(h_R-\langle a_i,x\rangle).$$
Choose $s^2=R^2/[8(d+\log(16n))]$. A Gaussian tail bound and union bound give $\Pr(\max_i\|a_i\|\le R)\ge15/16$. On this event each component is globally convex and $L$-Lipschitz. Inside the feasible ball the mean gap is $q\|x-\bar a\|^2/2$. The same posterior argument gives $\operatorname{tr}\Sigma\ge R^2d/[16n(d+\log(16n))]$, proving the stated window. Every unbounded query still reveals just one linear measurement because the common Huber term is known. Inside the ball this family has curvature $qI$, so it also proves the average-strongly-convex finite-sum lower for every public $\mu\le L/(2R)$.

These are joint $nd$ arguments. Separate $\Omega(n)$ and $\Omega(d)$ statements would justify only a maximum, not their product.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A3 - Deterministic extraction of an approximate subgradient

**Scope.** Exact real scalar values; finite positive probe scales; free real arithmetic and no bit-precision charge. Ball-restricted variants keep all probes inside the ball; global variants allow all-space probes.

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

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

### A4 - Finite-sum simulation and single-component inheritance

**Scope.** The average objective, component regularity, public geometry, algorithm permissions, and guarantee are retained exactly.

One average value costs $n$ selected-component values. A lower bound obtained by making all components equal transfers with cost one. Bounds copied from a one-component model without an $n$ factor apply only on $n=1$.

For $F=n^{-1}\sum_i f_i$, evaluate every component at the same point and average. This exactly simulates any whole-objective value, including finite-difference probes outside the feasible ball when all-space queries are permitted. Thus deterministic convex acceleration and localization give $O(nd\sqrt Q)$ and $O(nd^2\log(e+Q))$; strongly convex acceleration, restart, and localization give
$$O\!\left(nd\min\{\sqrt Q,\sqrt\kappa[1+\log_+(Q/\kappa)],d\log(e+Q)\}\right).$$
The near-unit-condition-number method uses the midpoint-curvature contraction $(\kappa-1)/(\kappa+1)$ with a finite-difference error small enough for the prescribed horizon, and each value again costs $n$. At $\kappa=1$, use exact recovery of the average quadratic. For a nonsmooth mean, multiply deterministic localization or approximate-subgradient simulation by $n$.

For lower bounds set every component equal to a legal single-objective hard instance. A requested component index adds no information and one hard-oracle value supplies its response. This transfers the source lower bound without multiplying by $n$, with exactly its own dimension, accuracy, and condition-number windows. Combine it with the independent joint $nd$ lower only where both apply. If a row imports a one-component upper or endpoint formula without an $n$ multiplier, its condition is $n=1$.

ARCS Corollaries 6 and 8 supply the separate randomized finite-sum upper branches. The public ball's linear minimization oracle is free in this model; the global minimizer lies in that ball, so the initial potential is bounded using $\beta R^2$ (for the convex branch, $D_0\le7\beta R^2$). Its finite-difference component queries are legal in the all-space domain. A constant-factor tighter expected nonnegative gap gives fixed success by Markov's inequality. These algorithms remain randomized and do not enter a deterministic view.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/abs/2109.08858) [3](https://arxiv.org/html/2607.16558v2)

### A5 - The smooth strongly convex dimension lower and its finite-sum embedding

**Scope.** The declared public curvature budgets are lower/upper bounds, not a promise that the best curvature moduli equal them.

For $Q=\beta R^2/\varepsilon\ge32$, the cited theorem gives
$$\Omega\!\left(d\min\{d,\sqrt\kappa,\sqrt Q\}\right),\qquad\kappa=\beta/\mu\ge1.$$
For the merely convex class omit the condition-number truncation.

Dorn et al., Corollary 2.4, directly covers global smoothness, global strong convexity, a global minimizer in the public radius, unrestricted exact-value queries/output, and adaptive randomized algorithms. Its explicit dimension baseline is retained, including at $\kappa=1$. A deterministic algorithm is included in that lower algorithm class. For selected-component access, set every component equal to the same source hard function; each requested component value is one source value. When combined with an independent $nd$ or precision-log lower bound, retain the source window of each term and maximize only valid terms. No extra factor of $n$ or $d$ follows from this embedding.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

### A6 - Explicit logarithmic lower bounds and class restrictions

**Scope.** The source theorem retains its unrestricted query/output domain, fixed query cap, and stated accuracy window.

For the smooth class, $Q\ge128^2$ gives $\Omega(d\log Q)$. This also holds in a public strongly convex class with $\kappa\ge2$. For a ball-restricted Lipschitz class, $A=LR/\varepsilon\ge6\cdot128^2$ gives $\Omega(d\log A)$.

Dorn et al., Theorem 2.5, gives
$$\frac{3d}{4000}\left[1+\frac{\log(\beta_hR_h^2/\varepsilon)}{\log((\beta_h+\mu_h)/(\beta_h-\mu_h))}\right]$$
when $\mu_h/\beta_h\in[1/2,1]$ and $\beta_hR_h^2/\varepsilon\ge128^2$. Choose $\mu_h=\beta_h/2$, so the denominator is $\log3$. A convex $\beta$-smooth class contains this subclass with $\beta_h=\beta$, $R_h=R$. A public lower curvature budget $\mu\le\beta/2$ also contains it, uniformly in the public condition number.

For the ball-restricted Lipschitz class choose $R_h=R/2$, $\beta_h=2L/(3R)$, and $\mu_h=\beta_h/2$. On $B_2(R)$, $\|\nabla f(x)\|\le\beta_h(\|x\|+\|x_*\|)\le L$, and the global minimizer remains inside the feasible ball. One source value simulates one restricted value. The stronger source oracle permits all such algorithms, and $Q_h=A/6$. The explicit window makes $\log(A/6)$ and $\log A$ uniformly comparable.

For a selected-component finite sum with all components equal to the same hard function, one component query is one source query. This transfer has cost one, not $n$. A logarithmic and a dimension-dependent lower bound may be maximized only where both respective windows hold.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

### A7 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A8 - Smooth exact-value complexity just below the zero-query threshold

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

### A9 - Extending the endpoint bound to fixed accuracy windows

**Scope.** All model budgets are fixed while accuracy varies; exact unrestricted value access.

The endpoint lower bound at $Q=3$ yields $\Omega(d)$ for every $Q\ge3$. The deterministic finite-difference accelerated bound is $O(d)$ on every fixed numerical interval $4\le Q\le128^2$.

Solving to a smaller error also solves to any larger error, so minimax complexity is nondecreasing as $\varepsilon$ decreases. At $Q=3$, the endpoint lemma gives $\gamma=1/3$ and hence a uniform $\Omega(d)$ randomized lower bound. The deterministic accelerated upper bound $O(d\sqrt Q)$ is at most $128$ times its universal constant on the stated interval. The same upper bound applies to randomized algorithms. The endpoint hard family is already quadratic, so the lower statement transfers unchanged to the quadratic subclass; the quadratic upper follows by restriction of the smooth algorithm.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] Xiyuan Wei
Bin Gu
Heng Huang. An Accelerated Variance-Reduced Conditional Gradient Sliding Algorithm for First-order and Zeroth-order Optimization. 2021. arXiv2109.08858v1 (2021-09-18).

https://arxiv.org/abs/2109.08858

[3] Haihan Zhang, Chenheng Zhang, Zhiquan Qi and Zhouchen Lin. Near-Optimal Lower Bounds for Randomized Algorithms in Exact Value Zeroth-Order Convex Optimization. arXiv:2607.16558v2, 2026-07-30.

https://arxiv.org/html/2607.16558v2

[4] V. Yu. Protasov. Algorithms for approximate calculation of the minimum of a convex function from its values. Mathematical Notes 59(1):69--74, 1996.

https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper
