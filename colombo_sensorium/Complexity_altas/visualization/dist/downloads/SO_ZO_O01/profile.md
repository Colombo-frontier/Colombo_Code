# Exact comparison feedback for smooth convex objectives

**Setting ID.** `SO_ZO_O01`

Single-objective optimization

Minimize a globally smooth convex objective using exact comparisons. Deterministic and randomized fixed-budget complexities agree up to logarithmic factors throughout the documented joint domain $Q=\beta R^2/\varepsilon\ge32$.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Lipschitz gradient

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact comparison; public information: Public inputs explicitly declared; query domain: Full space

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

$f$ is globally convex.

A global minimizer $x_*\in B_2(0,R)$ exists; the localization ball does not restrict the function domain.

### Oracle interface

Any finite point pair $(x,y)\in\mathbb{R}^d\times\mathbb{R}^d$ may be queried, returning $\operatorname{sign}(f(x)-f(y))\in\{-1,0,1\}$. Equal values produce zero. Neither the magnitude of the difference nor either function value is revealed.

The public inputs are $d$, $\beta$, $R$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in \mathbb{R}^d}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

One point-pair comparison costs $1$ call. Every repeated comparison and every comparison in a line search is charged. The budget $T$ counts scalar comparison replies.

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

**Definition.** One exact point-pair comparison reply, including ties

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One exact point-pair comparison reply, including ties

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One exact point-pair comparison reply, including ties

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One exact point-pair comparison reply, including ties

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime O01.R1

**Region.** $32\le Q=\beta R^2/\varepsilon\le d^2$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** One exact point-pair comparison reply, including ties

**Status.** Logarithmic gap

**Lower bound.** B3, B10, B6, B12

$$
\Omega(d\sqrt Q)
$$

**Upper bound.** B13, B15

$$
O\!\left(\sqrt Q\,[d\log(2dQ)+\log^2(2Q)]\right)
$$

**Gap or comparison.** $O(\log(2dQ)+d^{-1}\log^2(2Q))=O(\log d)$ on $32\le Q\le d^2$.

### R2 - Parameter regime O01.R2

**Region.** $Q=\beta R^2/\varepsilon\ge32$ and $Q>d^2$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** One exact point-pair comparison reply, including ties

**Status.** Logarithmic gap

**Lower bound.** B3, B10, B6, B12

$$
\Omega(d\max\{d,\log Q\})
$$

**Upper bound.** B13, B9, B15, B11

$$
O\!\left(\min\!\left\{\sqrt Q\,[d\log(2dQ)+\log^2(2Q)],\ d^2\log Q\log(dQ)\right\}\right)
$$

**Gap or comparison.** $O\!\left(\frac{\min\{\sqrt Q[d\log(2dQ)+\log^2(2Q)],d^2\log Q\log(dQ)\}}{d\max\{d,\log Q\}}\right)\le O(\min\{d,\log Q\}\log(dQ))$.

## 4. Bounds and supporting evidence

### B1 - Comparison-based gradient estimation and convex localization

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\min\{dQ\log(dQ),\ d^2\log(dQ)\}\right)
$$

**Sources.** [2](https://arxiv.org/html/2405.11454v1)

**Conditions.** $Q$ is sufficiently large. The objective is globally convex and $\beta$-smooth, and has a global minimizer in the known localization ball of radius $R$.

**Oracle correspondence.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

**Source location.** [2](https://arxiv.org/html/2405.11454v1) theorem: Theorems 2--3

**Source location.** [2](https://arxiv.org/html/2405.11454v1) theorem: Theorems 2--3

**Source location.** [2](https://arxiv.org/html/2405.11454v1) pdf pages: 7; printed pages: 7; theorem: Theorems 2--3

**Source location.** [2](https://arxiv.org/html/2405.11454v1) pdf pages: 9; printed pages: 9; theorem: Theorems 2--3

**Source location.** [2](https://arxiv.org/html/2405.11454v1) pdf pages: 6; 9; 10; printed pages: 6; 9; 10; theorem: v1 Theorem 3; historical source locator

Source locator for the historical combined upper claims. Both b1 records remain excluded from the current comparison envelopes. PDF SHA256 150ea20d6fd61257782c67fe15fe135ee03ab828d84a3dc26f236b57ef4ac6c3; HTML SHA256 354e38c235a5dcb24fca2e74ae4363767de6e27a0b8480b5240b30802d99a57a. Active upper support is given separately by the current bound records and their stated proofs.

### B2 - Reduction of an exact-value lower bound to the comparison interface

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\max\{d\min(d,\sqrt Q),\ d\log Q\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2610.19652v1)

**Conditions.** Each comparison can be simulated by two exact values. The dimension–accuracy term applies when $Q\ge32$, and the logarithmic-accuracy term when $Q\ge128^2$. Take their maximum only in the window where both apply.

**Oracle correspondence.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_COMPARE_TRANSFER

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.1 and Appendix E

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 3; printed pages: 3; theorem: Theorem 2.1 and Appendix E

### B3 - Reduction of an exact-value lower bound to the comparison interface

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt Q\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2610.19652v1) [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf)

**Conditions.** $Q=\beta R^2/\varepsilon \ge 32$; $d\ge 1$.

**Oracle correspondence.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_COMPARE_TRANSFER

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 3; theorem: Theorem 2.1; simulation of comparisons using exact values

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf) [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2; Section 4; external Theorem 2.1 of arXiv:2610.00345v1; pdf pages: 4; 5; 6; printed pages: 4; 5; 6

Online use of two exact values per comparison preserves the private seed, full transcript, arbitrary full-space outputs, success event and deterministic pathwise cap, giving the dimension-accuracy lower bound.

### B4 - Comparison-based gradient estimation and convex localization

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\min\{dQ\log(dQ),\ d^2\log(dQ)\}\right)
$$

**Sources.** [2](https://arxiv.org/html/2405.11454v1)

**Conditions.** $Q$ is sufficiently large. The objective is globally convex and $\beta$-smooth, and has a global minimizer in the known localization ball of radius $R$.

**Oracle correspondence.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

**Source location.** [2](https://arxiv.org/html/2405.11454v1) theorem: Theorems 2--3

**Source location.** [2](https://arxiv.org/html/2405.11454v1) theorem: Theorems 2--3

**Source location.** [2](https://arxiv.org/html/2405.11454v1) pdf pages: 7; printed pages: 7; theorem: Theorems 2--3

**Source location.** [2](https://arxiv.org/html/2405.11454v1) pdf pages: 9; printed pages: 9; theorem: Theorems 2--3

**Source location.** [2](https://arxiv.org/html/2405.11454v1) pdf pages: 6; 9; 10; printed pages: 6; 9; 10; theorem: v1 Theorem 3; historical source locator

Source locator for the historical combined upper claims. Both b1 records remain excluded from the current comparison envelopes. PDF SHA256 150ea20d6fd61257782c67fe15fe135ee03ab828d84a3dc26f236b57ef4ac6c3; HTML SHA256 354e38c235a5dcb24fca2e74ae4363767de6e27a0b8480b5240b30802d99a57a. Active upper support is given separately by the current bound records and their stated proofs.

### B5 - Reduction of an exact-value lower bound to the comparison interface

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\max\{d\min(d,\sqrt Q),\ d\log Q\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2610.19652v1)

**Conditions.** Each comparison can be simulated by two exact values. The dimension–accuracy term applies when $Q\ge32$, and the logarithmic-accuracy term when $Q\ge128^2$. Take their maximum only in the window where both apply.

**Oracle correspondence.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_COMPARE_TRANSFER

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2.1 and Appendix E

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 3; printed pages: 3; theorem: Theorem 2.1 and Appendix E

### B6 - Reduction of an exact-value lower bound to the comparison interface

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt Q\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2610.19652v1) [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf)

**Conditions.** $Q=\beta R^2/\varepsilon \ge 32$; $d\ge 1$.

**Oracle correspondence.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_COMPARE_TRANSFER

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 3; theorem: Theorem 2.1; simulation of comparisons using exact values

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf) [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 2; Section 4; external Theorem 2.1 of arXiv:2610.00345v1; pdf pages: 4; 5; 6; printed pages: 4; 5; 6

Online use of two exact values per comparison preserves the private seed, full transcript, arbitrary full-space outputs, success event and deterministic pathwise cap, giving the dimension-accuracy lower bound.

### B7 - Deterministic comparison direction estimation and uniform projected normalized descent

**Admission.** Eligible evidence; not selected in the displayed bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(dQ\log(dQ))
$$

**Sources.** [2](https://arxiv.org/html/2405.11454v1)

**Conditions.** d>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

**Oracle correspondence.** One comparison per finite directional-preference probe; map native zero ties to either allowed source tie reply.

**Guarantee conversion.** Deterministic gap <=epsilon on every instance; the deterministic strategy also meets randomized success >=2/3. Constants are universal.

**Output rule.** Return the comparison-tournament minimum of projected iterates in B_R, a permitted native output; no value or certificate is required.

**Resource conversion.** T=ceil(128Q) fixed iterations; the explicit estimator in ZO_PROOF_COMPARE_UPPER_AUDIT_20261115 costs O(d log(dQ)) each, plus T-1 charged tournament comparisons. The deterministic cap holds on every path.

**Local argument.** ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

**Source location.** [2](https://arxiv.org/html/2405.11454v1) pdf pages: 5; 6; 7; 8; printed pages: 5; 6; 7; 8; theorem: v1 Lemma 1, Theorems 1-2 and Problem 1; explicit estimator and projected-descent derivation

Immutable PDF SHA256 150ea20d6fd61257782c67fe15fe135ee03ab828d84a3dc26f236b57ef4ac6c3; source_read chars 14000-24000 and 10500-14500. HTML SHA256 354e38c235a5dcb24fca2e74ae4363767de6e27a0b8480b5240b30802d99a57a; chars 25000-35000 verifies formulas. See ZO_PROOF_COMPARE_UPPER_AUDIT_20261115 for every cost, uniformity, output and guarantee step.

### B8 - Deterministic comparison direction estimation and uniform projected normalized descent

**Admission.** Eligible evidence; not selected in the displayed bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(dQ\log(dQ))
$$

**Sources.** [2](https://arxiv.org/html/2405.11454v1)

**Conditions.** d>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

**Oracle correspondence.** One comparison per finite directional-preference probe; map native zero ties to either allowed source tie reply.

**Guarantee conversion.** Deterministic gap <=epsilon on every instance; the deterministic strategy also meets randomized success >=2/3. Constants are universal.

**Output rule.** Return the comparison-tournament minimum of projected iterates in B_R, a permitted native output; no value or certificate is required.

**Resource conversion.** T=ceil(128Q) fixed iterations; the explicit estimator in ZO_PROOF_COMPARE_UPPER_AUDIT_20261115 costs O(d log(dQ)) each, plus T-1 charged tournament comparisons. The deterministic cap holds on every path.

**Local argument.** ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

**Source location.** [2](https://arxiv.org/html/2405.11454v1) pdf pages: 5; 6; 7; 8; printed pages: 5; 6; 7; 8; theorem: v1 Lemma 1, Theorems 1-2 and Problem 1; explicit estimator and projected-descent derivation

Immutable PDF SHA256 150ea20d6fd61257782c67fe15fe135ee03ab828d84a3dc26f236b57ef4ac6c3; source_read chars 14000-24000 and 10500-14500. HTML SHA256 354e38c235a5dcb24fca2e74ae4363767de6e27a0b8480b5240b30802d99a57a; chars 25000-35000 verifies formulas. See ZO_PROOF_COMPARE_UPPER_AUDIT_20261115 for every cost, uniformity, output and guarantee step.

### B9 - Deterministic centroid cuts using the already-proved finite direction estimator

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d^2\log Q\log(dQ))
$$

**Sources.** [4](https://arxiv.org/pdf/1405.4980v2) [5](https://arxiv.org/html/2611.29533v1) [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf)

**Conditions.** d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

**Oracle correspondence.** One comparison per finite directional-preference probe; map native zero ties to either allowed source tie reply.

**Guarantee conversion.** Exact same native view/g1 and model; complete proof ZO_PROOF_COMPARE_CENTROID_20261116

**Output rule.** The charged tournament returns the smallest-value recorded centroid or fixed fallback candidate. Centroids lie in the known ball B(0,2R); the proof uses no output projection. All candidates and the final finite R^d output are permitted by the target output contract. If a body degenerates, the fixed completion supplies finite fallback candidates; the all-bad volume argument has already forced an earlier good candidate. Every tournament comparison is charged.

**Resource conversion.** All actual gradient/comparison calls are counted; no hidden oracle access. See complete proof ZO_PROOF_COMPARE_CENTROID_20261116

**Local argument.** ZO_PROOF_COMPARE_CENTROID_20261116

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf) theorem: Theorem 4; pdf pages: 8; printed pages: 8

The same full-space comparison model admits a deterministic fixed-cap centroid method with O(d^2 log Q log(d sqrt(Q))) comparisons for Q>=32.

**Source location.** [5](https://arxiv.org/html/2611.29533v1) theorem: Proposition E.1; pdf pages: 23; 24; printed pages: 23; 24

An independent deterministic centroid comparison method has O(d^2 log Q log(dQ)) fixed cap for Q>=32; its binary replies are implemented by one ternary native reply.

### B10 - Finite ternary transcript counting on disjoint quadratic-success balls

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\frac{(d/2)\log(Q/8)+\log(2/3)}{\log 3}=\Omega(d\log Q)
$$

**Conditions.** d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

**Oracle correspondence.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Guarantee conversion.** Exact same native view/g1 and model; complete proof ZO_PROOF_COMPARE_PACKING_20261116

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** All actual gradient/comparison calls are counted; no hidden oracle access. See complete proof ZO_PROOF_COMPARE_PACKING_20261116

**Local argument.** ZO_PROOF_COMPARE_PACKING_20261116

### B11 - Deterministic centroid cuts using the already-proved finite direction estimator

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d^2\log Q\log(dQ))
$$

**Sources.** [4](https://arxiv.org/pdf/1405.4980v2) [5](https://arxiv.org/html/2611.29533v1) [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf)

**Conditions.** d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

**Oracle correspondence.** One comparison per finite directional-preference probe; map native zero ties to either allowed source tie reply.

**Guarantee conversion.** Exact same native view/g1 and model; complete proof ZO_PROOF_COMPARE_CENTROID_20261116

**Output rule.** The charged tournament returns the smallest-value recorded centroid or fixed fallback candidate. Centroids lie in the known ball B(0,2R); the proof uses no output projection. All candidates and the final finite R^d output are permitted by the target output contract. If a body degenerates, the fixed completion supplies finite fallback candidates; the all-bad volume argument has already forced an earlier good candidate. Every tournament comparison is charged.

**Resource conversion.** All actual gradient/comparison calls are counted; no hidden oracle access. See complete proof ZO_PROOF_COMPARE_CENTROID_20261116

**Local argument.** ZO_PROOF_COMPARE_CENTROID_20261116

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf) theorem: Theorem 4; pdf pages: 8; printed pages: 8

The same full-space comparison model admits a deterministic fixed-cap centroid method with O(d^2 log Q log(d sqrt(Q))) comparisons for Q>=32.

**Source location.** [5](https://arxiv.org/html/2611.29533v1) theorem: Proposition E.1; pdf pages: 23; 24; printed pages: 23; 24

An independent deterministic centroid comparison method has O(d^2 log Q log(dQ)) fixed cap for Q>=32; its binary replies are implemented by one ternary native reply.

### B12 - Finite ternary transcript counting on disjoint quadratic-success balls

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\frac{(d/2)\log(Q/8)+\log(2/3)}{\log 3}=\Omega(d\log Q)
$$

**Conditions.** d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

**Oracle correspondence.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Guarantee conversion.** Exact same native view/g1 and model; complete proof ZO_PROOF_COMPARE_PACKING_20261116

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** All actual gradient/comparison calls are counted; no hidden oracle access. See complete proof ZO_PROOF_COMPARE_PACKING_20261116

**Local argument.** ZO_PROOF_COMPARE_PACKING_20261116

### B13 - Deterministic normalized two-dimensional subspace acceleration

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\sqrt Q\,[d\log(2dQ)+\log^2(2Q)]\right)
$$

**Sources.** [5](https://arxiv.org/html/2611.29533v1)

**Conditions.** $d\ge1$; $\beta,R,\varepsilon>0$; $Q=\beta R^2/\varepsilon\ge1$.

**Oracle correspondence.** One native ternary reply implements the source bit $1\{f(x)\ge f(y)\}$: map 0 and +1 to 1, and -1 to 0. All queries remain finite full-space pairs.

**Guarantee conversion.** Deterministic objective gap at most $\varepsilon$ on every instance. The same strategy gives probability one under the randomized view, hence satisfies its per-instance 2/3 guarantee.

**Output rule.** The output is an arbitrary finite full-space iterate; it need not lie in the localization ball and no objective value or optimality certificate accompanies it.

**Resource conversion.** The prescribed horizon $K=\lceil10\sqrt Q\rceil$ and fixed inner schedules count every comparison. Lemma F.1 also bounds the number on every possible reply sequence.

**Source location.** [5](https://arxiv.org/html/2611.29533v1) Theorem 3.4; Algorithm 2; Appendix B; Lemma F.1

A deterministic comparison-only algorithm minimizes over one- and two-dimensional bounded subproblems and returns an epsilon-optimal point with the stated fixed cap.

### B14 - Deterministic full-history acceleration with bounded affine optimization

**Admission.** Eligible evidence; not selected in the displayed bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(d\sqrt Q\log(dQ)+Q^{3/2}\log^2 Q\right)
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf)

**Conditions.** $d\ge1$; $\beta,R,\varepsilon>0$; $32\le Q=\beta R^2/\varepsilon\le d^2$.

**Oracle correspondence.** The source uses the same full-space ternary exact comparison oracle, including zero on ties. Direction probes, inner solves and selection use only comparisons.

**Guarantee conversion.** Deterministic objective gap at most $\varepsilon$ on every instance. The same strategy gives probability one under the randomized view, hence satisfies its per-instance 2/3 guarantee.

**Output rule.** The output is an arbitrary finite full-space iterate; it need not lie in the localization ball and no objective value or optimality certificate accompanies it.

**Resource conversion.** The prescribed horizon $N=\lceil16\sqrt Q/3\rceil$ and equation (2) count all direction probes, bounded affine solves, bounded line searches and incumbent comparisons on every path.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf) Theorem 5; Section 7; equation (2); Lemma 1; Proposition 1; Lemma 2

A deterministic full-history algorithm retains all estimated directions, approximately minimizes in the resulting bounded subspace and uses charged incumbent selection; its full fixed cap is the stated sum.

### B15 - Deterministic normalized two-dimensional subspace acceleration

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\sqrt Q\,[d\log(2dQ)+\log^2(2Q)]\right)
$$

**Sources.** [5](https://arxiv.org/html/2611.29533v1)

**Conditions.** $d\ge1$; $\beta,R,\varepsilon>0$; $Q=\beta R^2/\varepsilon\ge1$.

**Oracle correspondence.** One native ternary reply implements the source bit $1\{f(x)\ge f(y)\}$: map 0 and +1 to 1, and -1 to 0. All queries remain finite full-space pairs.

**Guarantee conversion.** Deterministic objective gap at most $\varepsilon$ on every instance. The same strategy gives probability one under the randomized view, hence satisfies its per-instance 2/3 guarantee.

**Output rule.** The output is an arbitrary finite full-space iterate; it need not lie in the localization ball and no objective value or optimality certificate accompanies it.

**Resource conversion.** The prescribed horizon $K=\lceil10\sqrt Q\rceil$ and fixed inner schedules count every comparison. Lemma F.1 also bounds the number on every possible reply sequence.

**Source location.** [5](https://arxiv.org/html/2611.29533v1) Theorem 3.4; Algorithm 2; Appendix B; Lemma F.1

A deterministic comparison-only algorithm minimizes over one- and two-dimensional bounded subproblems and returns an epsilon-optimal point with the stated fixed cap.

### B16 - Deterministic full-history acceleration with bounded affine optimization

**Admission.** Eligible evidence; not selected in the displayed bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(d\sqrt Q\log(dQ)+Q^{3/2}\log^2 Q\right)
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf)

**Conditions.** $d\ge1$; $\beta,R,\varepsilon>0$; $32\le Q=\beta R^2/\varepsilon\le d^2$.

**Oracle correspondence.** The source uses the same full-space ternary exact comparison oracle, including zero on ties. Direction probes, inner solves and selection use only comparisons.

**Guarantee conversion.** Deterministic objective gap at most $\varepsilon$ on every instance. The same strategy gives probability one under the randomized view, hence satisfies its per-instance 2/3 guarantee.

**Output rule.** The output is an arbitrary finite full-space iterate; it need not lie in the localization ball and no objective value or optimality certificate accompanies it.

**Resource conversion.** The prescribed horizon $N=\lceil16\sqrt Q/3\rceil$ and equation (2) count all direction probes, bounded affine solves, bounded line searches and incumbent comparisons on every path.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf) Theorem 5; Section 7; equation (2); Lemma 1; Proposition 1; Lemma 2

A deterministic full-history algorithm retains all estimated directions, approximately minimizes in the resulting bounded subspace and uses charged incumbent selection; its full fixed cap is the stated sum.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: aebe76fad6f1c99ab8d9259ad81e6d56775a693bdafb6b46bb525894c45904b5

### Native proof: ZO_PROOF_COMPARE_TRANSFER

Native pointer: /proofs/0; canonical SHA-256: c8ce86e9ae2bb397e4f76dd5c236d3f4443d596025d272bfd93dbffeff7bf86b

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 9fd8fd145f57cee534298bc780f287636c06f0076521ee2aeb2b63f7af047089

Two exact scalar values simulate one comparison. Therefore a fixed-success exact-value lower bound $L$ gives a comparison lower bound $L/2$. Expected-error targets require a separate constant-factor accuracy conversion.

At each adaptive comparison request $(x,y)$, query both exact values and return their order, including the declared tie convention. The same seed and transcript generate the same next query and output, using at most twice the comparison budget. Hence a comparison algorithm contradicts a value lower theorem only when all source model and guarantee conditions match.

For smooth convex objectives, apply the dimension/accuracy branch of Dorn et al., Theorem 2.1, at $Q\ge32$, and its logarithmic strongly convex subclass at $Q\ge128^2$; maximize only on their common window. For a strongly convex model with initial gap $\Delta$, choose a hard-instance radius $R_h=\sqrt{2\Delta/\beta}$. Smoothness at the global minimizer gives the required initial gap. If the target guarantee is expected error $\varepsilon$, Markov supplies success $2/3$ at error $3\varepsilon$; then the source scale is $Q_h=2\Delta/(3\varepsilon)$ and must be at least 32. No new public radius is added to the target specification.

For nonconvex gradient stationarity, use the exact-value hard subclass with a proof-only Lipschitz budget satisfying $L^2\ge\beta\Delta$. The source cap $B=\min\{\beta\Delta,L^2\}$ becomes $\beta\Delta$. Retain its small-gradient window and dimension requirement $d\ge C(\beta\Delta/\varepsilon^2)\log(2+\beta\Delta/\varepsilon^2)$. The same two-value simulation then gives the registered comparison lower bound.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/0/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 303e02c06610d313e9347909799f1dbc2f9803e773d42ed7e76ecfa613b6a925

The comparison oracle returns only the exact order of two function values. Query/output domains, model budgets, and guarantees are preserved.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 977241fab46979879bf0f9f29328779d6f47061fda21d0440ffd0866219d845e

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native item 2

Native pointer: /proofs/0/source_refs/1; canonical SHA-256: cae76ce93df3e19a425b1d241baeefabe3ec71bc0147013d0a00884e08fe70b7

SO_SRC_12e2b72bb6c9ca16

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 9873420f0001b4f6fe4194a02f74506afcc774c9b161b81c51e4323ea77bdf04

Exact-value lower bounds transferred to comparison feedback

### Native proof: ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

Native pointer: /proofs/1; canonical SHA-256: 3d0823e89a6954cac3174da6aea948601be44cf704d57fc20e248753c5ec5846

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: be2d73292501cb5e670328d0d9ed7e8651e18ce33589fa189b8a2d9afc5d8953

Primary source read: 2405.11454v1 Lemma 1 (directional preference), Theorem 1 and Theorem 2/Problem 1. PDF SHA256 150ea20d6fd61257782c67fe15fe135ee03ab828d84a3dc26f236b57ef4ac6c3, chars10500-14500 and14000-24000; HTML SHA256 354e38c235a5dcb24fca2e74ae4363767de6e27a0b8480b5240b30802d99a57a, chars25000-35000 verifies Theorems2-3 formulas. Source n=d,L=beta. A native tie0 is mapped to +1, an allowed source tie reply. Finite positive probes and Euclidean projection use only native public inputs; no value or certificate is obtained. The following explicit estimator supplies the needed direction guarantee independently of implementation details in source Algorithm2.

Complete direction-estimation construction: Given delta in(0,1], gamma>0, use tolerance tau=delta gamma/(100d^2). A comparison at (x+(2tau/beta)v,x), for unit v, yields either <grad f(x),v>>=-tau or <grad f(x),v><=tau; this follows immediately from the smoothness Taylor remainder bounded by beta h^2/2, and is source Lemma1. Orient each basis vector v_i=+/-e_i using this test, so a_i=<grad f,v_i>>=-tau. Find a pivot p by a sequential tournament: compare components with direction (v_i-v_j)/sqrt(2); the selected winner is at least the loser minus sqrt(2)tau. If ||grad f||>=gamma, max a_i>=||grad f||/sqrt(d), and the final pivot a_p>=max a_i-sqrt(2)(d-1)tau>=gamma/(2sqrt(d))>0. Moreover each ratio r_i=a_i/a_p lies in[-2,2], because a_i>=-tau and a_i<=a_p+2d tau. For i!=p bisect [-2,2] using the directional test on (z v_p-v_i)/sqrt(1+z^2). Each reply compares z with r_i up to kappa=sqrt(5)tau/a_p<=2sqrt(5)sqrt(d)tau/gamma<=delta/(16sqrt(d)). Keep the indicated half interval; inductively the true r_i stays within distance kappa of it. After K=ceil(log_2(32sqrt(d)/delta)) rounds, its midpoint alpha_i satisfies |alpha_i-r_i|<=2/2^K+kappa<=delta/(8sqrt(d)). Set alpha_p=1. The vector r=(a_i/a_p) has norm>=1; ||alpha-r||<=delta/8. The elementary normalization inequality ||u/||u||-v/||v||||<=2||u-v||/||v|| shows that h=(sum alpha_i v_i)/||alpha|| differs from grad f/||grad f|| by at most delta/4, hence at most delta. For d=1 the ratio loop is empty and the oriented sign is correct under the promise. With or without the promise, the schedule has d+(d-1)+(d-1)K=O(d log(d/delta)) comparisons and returns a unit vector because alpha_p=1. Every probing radius is positive and finite, and no unbounded line search occurs.

Complete uniform optimization derivation: Let Q=beta R^2/epsilon>=32, T=ceil(128Q), delta=1/(16 sqrt(Q)), gamma=epsilon/(2R), eta=R/sqrt(T). Start x_0=0; at each t=0,...,T-1 get unit h_t from the explicit fixed-schedule estimator above and set x_{t+1}=Proj_{B_R}(x_t-eta h_t). Select the minimum-value point among x_0,...,x_{T-1} by T-1 charged comparisons. This never needs a function value or optimality certificate. Suppose every recorded point has gap g_t>epsilon. Convexity gives ||grad f(x_t)||>=g_t/||x_t-x_*||>=epsilon/(2R), so all estimates satisfy their promise. Smoothness and the global infimum give ||grad f(x)||^2<=2 beta (f(x)-f_*): apply the descent inequality to x-grad f(x)/beta. Consequently <h_t,x_t-x_*>>=g_t/||grad f(x_t)||-2R delta>=(1/sqrt(2)-1/8)R/sqrt(Q). The projection inequality telescopes to (1/T)sum_t <h_t,x_t-x_*><=R^2/(2 eta T)+eta/2=R/sqrt(T)<=R/sqrt(128Q), a contradiction. Thus the tournament output has gap <=epsilon. The deterministic worst-case cost is T O(d log(d/delta))+(T-1)=O(dQ log(dQ)), with universal constants, uniform in d,beta,R,epsilon. The same deterministic strategy is admissible for randomized g1, with success probability one; no random selection or amplification is needed.

Scope: the argument above supports the separate projected-descent b4 records. The historical combined b1 claims remain excluded from the current comparison envelopes.

Endpoint checks: R,beta,epsilon are positive and d>=1, so there is no Q=0 endpoint in the contract. Smoothness at x_* gives f(0)-f_*<=beta R^2/2; hence returning 0 uses zero queries when Q<=2. This elementary check is outside all four registered comparison regions and is not added here as a native endpoint bound/comparison. For Q>=32 our fixed schedule applies also at d=1, with no precision-independent saturation assertion. At Q=d^2 the c1/c2 lower formulas both equal Omega(d^2); c1 owns equality.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: cbbd563b514bb9c83f5ba75786033643201836de03dd901364a1c1b4865bbf4d

#### Native item 1

Native pointer: /proofs/1/limitations/0; canonical SHA-256: c76da0b6a4698470ef3777103ca0c7620461a3862cefe1014cf7c17b05157f75

Uses only the source directional-preference lemma and the explicit estimator/descent proof above; unrelated lower-bound sources are not recertified.

#### Native item 2

Native pointer: /proofs/1/limitations/1; canonical SHA-256: a7e94cae7efab6a5f95c2344a5c52252956f1465e3f3c3e6fd181610dfa83c34

This proof supports only the stated projected-descent upper bound; other optimization compositions, quantity transfers and sharp one-dimensional rates require separate records.

#### Native item 3

Native pointer: /proofs/1/limitations/2; canonical SHA-256: e55b47707e2f0fb863541b2f4c5acdc707e13dc26d09a76749238d1987efde26

Zero-query endpoint is checked as a contract consequence but its native registration is deferred.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: e79d28d4dcc0e66f4ab62528d507613ffd2375f1e3870fb8b8c9fa35f3035404

SO_ZO_O01, deterministic g1 and randomized g1, q1 quantities, fixed worst-case comparison budget; Q>=32. No new oracle.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 407bb103bbbb97d04ea5d263a277297169395a697720ec44592a896f1f8cfe95

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: a4c411849b0792886c4696cc85e8098df55c809ac0ee0b6e01b04b4e83783a28

SO_SRC_25cbefe670f1e510

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 7fe7649926b931b42b17c4e66f47c266ad0c47689e3d70de7a61a4f85d5ca83f

Uniform normalized projected descent with a fixed comparison budget

### Native proof: ZO_PROOF_COMPARE_CENTROID_20261116

Native pointer: /proofs/2; canonical SHA-256: fb25dd669078b792883b66e1ab4f63d886bf5bff35e815cdf4a0b4baed0d814f

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: a50609698fb4b364e81c2bf6adc22c7caa9ab8763ab9f1b1daacfda4d0c243b3

# O01: Center-of-gravity cutting upper bound and comparison-tree packing lower bound (guided analyst derivation, pending independent review)

The historical combined min upper bound remains excluded from current envelopes. This derivation has its own explicit estimator and localization argument. Direction estimation uses only the independent fixed-length construction already accepted in previous-baseline/proofs/1: given public γ>0 and 0<δ≤1, if ||∇f(x)||≥γ, it returns a unit vector h with error ≤δ using C_dir(d,δ)=2d−1+(d−1)ceil(log2(32sqrt(d)/δ)) comparisons; even when the promise is not satisfied, it always terminates and returns a unit vector. Native tie0 is mapped to +; all step sizes are finite and positive.

## Upper bound under the exact source guard Q≥32

Let Q=βR²/ε≥32, r=sqrt(ε/β), and Kε=B(0,2R)∩{f≤f*+ε/2}. Smoothness and a point x*∈B_R give B(x*,r)⊂Kε, because r≤R and ∇f(x*)=0.

Starting from C0=B(0,2R), at each iteration take the center of gravity x of the current known convex body, run the direction estimator above with γ=ε/(3R) and δ=1/(48Q), and retain C∩{y:<h,y−x>≤0}. Suppose, for contradiction, that every examined center of gravity has gap>ε. Then ||x−x*||≤3R, convexity gives ||∇f(x)||>ε/(3R), and β-smoothness gives ||∇f(x)||≤3βR. For every y∈Kε, ||y−x||≤4R and

\[
\langle h,y-x\rangle
\le\frac{f(y)-f(x)}{\|\nabla f(x)\|}+4R\delta
<-\frac{\varepsilon}{6\beta R}+\frac{\varepsilon}{12\beta R}<0.
\]

Thus every bad cut retains the inner ball. The Grünbaum property implies that any halfspace through the center of gravity retains at most 1−1/e of the volume (apply the ≥1/e bound for the opposite halfspace to the full-dimensional convex body). After the fixed number of iterations

\[
N=1+\left\lceil\frac{d\log(2\sqrt Q)}{-\log(1-1/e)}\right\rceil
\]

if all iterations were still bad, the remaining volume would be smaller than that of a ball of radius r, a contradiction. If positive volume disappears earlier, use the fixed fallback point 0 and a dummy schedule thereafter; this branch cannot occur when all iterations are bad, because the inner ball is retained. Zero-volume determination and center-of-gravity computation are measurable internal operations on a known ball and finitely many cuts, and use no free information about the unknown f; the current native contract allows arbitrary measurable strategies and does not charge for internal computation.

Finally, use N−1 charged comparisons to select the examined point with the smallest function value. The total per-path cap is N*C_dir(d,δ)+N−1, hence O(d²logQlog(dQ)). The same deterministic algorithm succeeds on every instance and also satisfies rand≥2/3. An exact center of gravity does not imply computational time efficiency.

The [Bubeck 2015 arXiv:1405.4980v2 §2.1 Lemma2.2](https://arxiv.org/pdf/1405.4980v2) Grünbaum volume statement and its adjacent proof, on PDF page 19/printed page 246, were actually checked online. No claim is made to have independently reproved the entire geometric theorem. This argument has the same asymptotic order as the preceding evaluator-only upper-followup/addendum; an independent proof suitable for adoption and a native bound candidate are established only in this round, without retroactively adding earlier approval/read credit.



#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: d8326689898c168b9baa4840d579a3dcb722a6196ba9935b5f203d63b2b8658d

#### Native item 1

Native pointer: /proofs/2/limitations/0; canonical SHA-256: 169044e0d4c3cda8c1a6726155e3f4ec9331b45416bd1b52141e8dd567461ff3

user-feedback-guided curated analyst_derivation; not a prior blind scout result; no old approval/source-read credit transferred

#### Native item 2

Native pointer: /proofs/2/limitations/1; canonical SHA-256: f32fbff2e31d9fb69deace36ed7b339a1d0539d8f82ae462ab845a17c6c50355

External retained premises keep their original validity; this candidate has no native approval.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: a21379d8fe05d8dbcad298de22e6e9aaa2a852114d7536d2e29cebe5623c6b97

All d>=1,beta,R,epsilon>0,Q=beta R^2/epsilon>=32; both q1/g1 native views.

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: 0130c77557c6cf2f46cca654c50281acbe4632e9b941a9a062517157198c6906

#### Native item 1

Native pointer: /proofs/2/source_refs/0; canonical SHA-256: d9919b72be4d5d9126f3446008522bf36e04a8d1aa2f4bd71f94c70aab818541

SO_SRC_a00ef97da026391b

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 7b1d30bbeace1eff1be10aeb0cdc190929190dc4cb8c4beb1f363a988f349ce0

Fixed-cap centroid comparison optimizer with a valid gradient promise

### Native proof: ZO_PROOF_COMPARE_PACKING_20261116

Native pointer: /proofs/3; canonical SHA-256: ff4777c6c0a97df236a9eb4fbf2b24d19e9171795b864876b71e204214ce8011

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: 24be9f112ea9468cc264bdd50d0bb064582985dfaba5554896a7019aa9302214

## Direct-comparison packing lower bound under the exact guard Q≥32

Take f_a(x)=β||x−a||²/2 with a∈B_R. The success set is the closed ball B(a,r0), where r0=sqrt(2ε/β). Take a maximal finite packing in B_R whose centers have pairwise distances strictly greater than 2r0. Its balls of radius 2r0 cover B_R, and volume comparison gives M≥(R/(2r0))^d=(Q/8)^(d/2). The success balls are pairwise disjoint.

Fix the algorithm’s entire private random seed. A native ternary comparison tree of depth ≤T has at most 3^T leaves; the unique output at a given leaf can succeed for at most one center. Taking expectation over the seed, success≥2/3 for every center implies 3^T≥(2/3)M. Therefore

\[
T\ge\frac{(d/2)\log(Q/8)+\log(2/3)}{\log3}.
\]

For Q≥32,d≥1, the right-hand side is bounded below by a uniform positive constant times dlogQ, so T=Ω(dlogQ). Deterministic algorithms form a subclass. Early stopping can be padded with zero-tie queries without changing the T cap; outputs need not have been queried, and queries may have arbitrary precision/be unbounded, but none of these allowances enlarges the ternary alphabet of each comparison. This proof does not rely on the exact-value multiscale lower bound; the same counting argument cannot be applied to an exact-value oracle with an infinite real-valued reply alphabet.

## Combination

Combining with the retained projected upper bound and the original b3 lower bound under the same guard gives:
\[
\Omega(d\max\{\min(d,\sqrt Q),\log Q\})\le T^*\le O(d\min\{Q,d\log Q\}\log(dQ)).
\]

J1=32≤Q≤d²: the lower bound remains Ω(dsqrtQ), with ratio≤O(min{sqrtQ,dlogQ/sqrtQ}log(dQ)); J2=Q≥32,Q>d²: sqrtQ>logQ ensures that the upper branch reduces to O(d²logQlog(dQ)), the lower bound is Ω(d max{d,logQ}), and ratio≤O(min{d,logQ}log(dQ)), leaving only a polylog gap. Q=d² belongs to J1, and Q=32 includes equality. These are valid envelope/asymptotic-order relations, and crossings of hidden constants are not treated as exact phase transitions. Q<32, the native zero-query registration, and the sharp one-dimensional slice remain separately listed; the historical b1 upper bound remains excluded from current envelopes.


#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: d8326689898c168b9baa4840d579a3dcb722a6196ba9935b5f203d63b2b8658d

#### Native item 1

Native pointer: /proofs/3/limitations/0; canonical SHA-256: 169044e0d4c3cda8c1a6726155e3f4ec9331b45416bd1b52141e8dd567461ff3

user-feedback-guided curated analyst_derivation; not a prior blind scout result; no old approval/source-read credit transferred

#### Native item 2

Native pointer: /proofs/3/limitations/1; canonical SHA-256: f32fbff2e31d9fb69deace36ed7b339a1d0539d8f82ae462ab845a17c6c50355

External retained premises keep their original validity; this candidate has no native approval.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: fc4b53dd08ac334d24ce41c5b3de9dcc7550964b1adb8a7fcec969f535d826c2

All native d>=1,beta,R,epsilon>0,Q>=32; unrestricted randomized algorithms and thus deterministic ones.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: d3a3a82e43bff399ec6388c8b338826374857296b01e9df231bf9ea3038842d4

Ternary comparison-tree packing lower bound

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 93913abfc308a38380d932077c9b7627271fbebcaa56424282f843a8226814c4

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 12c0156775a9bc54ad1a9b5b09f1f573ae5b124db98896e4910b6d7c5081d811

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 882b17536f0a85d59e2d33fcbab81d097a4821fc480cd8abf8d028c960c7c5e7

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 0db1952d7fcc87ae403c61653423e19bcbe465eebd7587a1baa8f6c98f3d3fe4

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 4e23b21d4d4b0b764d7e7aff349078d346a8540b6943b40561d78eaa17c97cfa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: b36ffc04e97b0874f9a68ee1acfe09fe2d3837b6a3c69c66c53416062e4cf079

SO_ZO_O01__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 39efec2f18938c1e76fe13d490dca42933372e35252d5f98d5f493c0630eba87

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: f058a36ede1d8055c583234579be7ab841fcf21df085076edc60add65a9ba355

ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: c161d6f6fcddb27b81f9797ed3b0ca2dae865f453da459cb258b07ba86dbaf03

Historical statement excluded from current envelopes; normalized projected descent is represented by the separate b4 record. The b1 record is not selected.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: ca0175186f91436fba2e6adfd51cbb11e83b8075cd41742c5f799c5000620d6e

Historical combined claim with a sufficiently-large-Q source guard; not adopted in the current comparison envelopes.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 1fe944fb9b2b634353f5636cab92a1f90f61423653bdb330e2d2b0e47afd3c2e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: fdc1dac28d2e0ef28ed244ed4c2e233ff3d4af99a6277447f93c9fb04dadd408

SO_ZO_O01__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 23d015bbceffbae595c11ac10da2407fb5fb65d7477a97c1a9155484824d25ec

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: b7f6ce980a74a0d3d2d0281158c60503f30071680c97ca527c78395e6f4476fe

The literal historical q2 ID is not merged with q1. Its logarithmic consequence is now independently proved and adopted through q1 b6, so this is not an unresolved absence of a legal logarithmic lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 01684449126ff4a5f798cf2be278736b80b44cf56685cb5068959bfed1dfcc16

Its own frozen q2 contract; dimension branch Q>=32 and logarithmic branch Q>=128^2, maximized only on their common window.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 49575a6d7cbaaa75ce2f6da1a8fb530c77ab16a30906d427c7fceaec735c5d99

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: e9865214587940cf09761cc1ce224e9f092314a4af47482f75603ab03b3c6b1b

J1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 32a4728c80f62576358af5b408e940b383d6ca1f4528d86e51c699c57e1a0da5

SO_ZO_O01__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 424e7eefce05b301d0fe69a63b2693ec90d2a668bf5a8de0ca91724494093882

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 66190fd94763a22e0d2b2d1ba03dff13c067f274c622a2a8662f615df79e4b4b

Unchanged q1 lower retained conditionally from the frozen baseline and its exact-value simulation proof; not freshly recertified.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: a01215ff5cf3c1b385b8154f12676359b3f6e119569f2a917ee4023f2e0df864

Q>=32, d>=1, exact frozen guard in /bounds/2/applicability

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: b3a7e4735ec4558ac1e07963c7a3c27a0a78706d131600fe840498fffafb46f6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: dc2f63ea57ebae0831a35a8ae5589c6858967000c05b9c516c2444c26a296bc8

SO_ZO_O01__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 39efec2f18938c1e76fe13d490dca42933372e35252d5f98d5f493c0630eba87

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: f058a36ede1d8055c583234579be7ab841fcf21df085076edc60add65a9ba355

ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: fd92dbace71db0f7a48ab7769f0417e721fc5da695da688be5db327c7cfb1513

A compatible deterministic accelerated upper bound gives the selected envelope in this parameter region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: e8ed069bc07eedda6b92b3722606bf226fa288aa8f5b81bfc96f2a13038f5920

d>=1; beta,R,epsilon>0; Q>=32.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: 60d6bc16a218c3a92a7f60a79fc6bc88a59f3e2bbfb828313e10b07f5e1e7d0b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: b53e7b0873c06f88f5bffea2268f8de5ed4c33bea1d9734fb432abf2200948db

SO_ZO_O01__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: a5fa34774cf7a7b63dd5ef5678040eceda8a5c4f2551d98d4c9c81df7e43cd4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 2ff70ff2e71c0814360472ade1a9ceefa94cb2ce744805f0092e4820514aeb0f

ZO_PROOF_COMPARE_CENTROID_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: fd92dbace71db0f7a48ab7769f0417e721fc5da695da688be5db327c7cfb1513

A compatible deterministic accelerated upper bound gives the selected envelope in this parameter region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: 0e0cbe0bc337892d272e3896d8bd8b440b843a3c4f18d8f8d722f74667edcfb9

Exact bound guard; see native applicability.

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/bound_uses/5; canonical SHA-256: 8bb26c74e527648134c60ac623da3b8ead3cccdf832a5544c3a25b2f1b5e9f82

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/adopted_region; canonical SHA-256: 2b8dea31a21cf686ceeb0d6df6eda4747d5a1655fca0f738c9e3304bc01593e9

$32\le Q=\beta R^2/\varepsilon\le d^2$.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/bound_id; canonical SHA-256: 4564df58db2937c9f80324ec6f350bc311995c0e0b7bcb2851329b287561dff7

SO_ZO_O01__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs; canonical SHA-256: 23d015bbceffbae595c11ac10da2407fb5fb65d7477a97c1a9155484824d25ec

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/reason; canonical SHA-256: a79d2f14db7a67252089ba2bee4146fbf4ee4056e36418eb9a9625df71ffd8f3

Included as an explicit quantity-matched native participant.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/validity_region; canonical SHA-256: 0e0cbe0bc337892d272e3896d8bd8b440b843a3c4f18d8f8d722f74667edcfb9

Exact bound guard; see native applicability.

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/bound_uses/6; canonical SHA-256: 8182911f05dda37e85c0c69dcfd8d1c2dc7a6da55c99dde436efce7f25137845

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/bound_id; canonical SHA-256: b952f88b796514dfc643f8bcd2843a229051a68a0ebd25d5a81f69aa04437472

SO_ZO_O01__deterministic__public_acceleration_20261124

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/adopted_region; canonical SHA-256: 2b8dea31a21cf686ceeb0d6df6eda4747d5a1655fca0f738c9e3304bc01593e9

$32\le Q=\beta R^2/\varepsilon\le d^2$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/validity_region; canonical SHA-256: c1db85e4f2d169498d0ced1d03dd56b3b992ad5442c262d481a482a1145f2a99

$d\ge1$; $\beta,R,\varepsilon>0$; $Q=\beta R^2/\varepsilon\ge1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/reason; canonical SHA-256: bd2442e88fa38f483ce7c244ad572371747aa35a2ed2e52c56408545ddad68b1

The deterministic witness has the native fixed-cap objective-gap guarantee; source binary replies cost one native comparison.

#### Native item 8

Native pointer: /joint_analysis/comparisons/0/bound_uses/7; canonical SHA-256: 00a8150902d5704a3c3b5c027b64ecdaa8425da8da2ee89de44dec0f354f2bf3

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/bound_id; canonical SHA-256: 0eb79b631c7cf7804e3bcb32dde1a433bc5dd53a801eacd290bb2480c7db9ddb

SO_ZO_O01__deterministic__kimi_full_history_20261124

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/validity_region; canonical SHA-256: ebc80cacc2cff1e6654547026e0e9d7a85a5453b8c465b5c17551cf3fafbb050

$d\ge1$; $\beta,R,\varepsilon>0$; $32\le Q=\beta R^2/\varepsilon\le d^2$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/reason; canonical SHA-256: 6362835cabc35b6ec4be5bcfc8722f9a52350945d783384dd26f3050266dab15

The valid full-history witness has a larger recorded upper order in this region.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 37d777769bc774a9718833e8d563403523db27ba30659ad2fb759db18fd3b875

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 1b83fb6d7496f18aea8752942223656b58a4c11a0eed5549c6fff8b7ed96c9b0

$Q=32$ is included. $Q=d^2$ belongs to the first regime; that regime is empty for $d\le5$.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: d0907a49aec11ef20b3d6d6620b8e83b5911ddaacc7221de6e3e588ccad3f135

The accelerated upper applies for all $Q\ge1$; its selected lower comparison uses the common guard $Q\ge32$.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 5770c045496a43b0c68c8da6d665b55967dcd2e18117c217dae7e06080d10d8a

The high-accuracy envelope includes the direct ternary-packing lower $\Omega(d\log Q)$ on its original guard $Q\ge32$.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: b793fa087ac64102c83a8abbecf35d1db7db2b87bf6e3db695537677d3dc8c0e

Only the stated parameter domains and guarantees are compared; the coarse-accuracy complement is separate.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: cc2adcdeb65a438290336ef59b9e53c064be187cbbb60d5d9055c35bad62c634

$O(\log(2dQ)+d^{-1}\log^2(2Q))=O(\log d)$ on $32\le Q\le d^2$.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 56a7d83b93fc7928ef7ef6598f1c795e0edf185dd48bf150f50698d59adc0952

\Omega(d\sqrt Q)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: d1893136fdd4e759fc9a23b87bf5220063c2f8b658b25518054a4a09613b6cc9

The ratio is at most logarithmic in the joint dimension-accuracy variables; constants and logarithmic exponents are not matched.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: a04447034ae1b8240b691f6a269573ee1e2cede8a42fbe2def4df7797fe71122

O\!\left(\sqrt Q\,[d\log(2dQ)+\log^2(2Q)]\right)

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 2ff44fb4a3f19500b18ffd1850aced92830a884f1b1acc2eefe54a4b2fce39ba

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 45c1891799ca65d08d66a9b5cc7ded27d0f9c6cdb3ea42fe50e0b5ea4e1384e5

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 4e23b21d4d4b0b764d7e7aff349078d346a8540b6943b40561d78eaa17c97cfa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: b36ffc04e97b0874f9a68ee1acfe09fe2d3837b6a3c69c66c53416062e4cf079

SO_ZO_O01__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 39efec2f18938c1e76fe13d490dca42933372e35252d5f98d5f493c0630eba87

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: f058a36ede1d8055c583234579be7ab841fcf21df085076edc60add65a9ba355

ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: c161d6f6fcddb27b81f9797ed3b0ca2dae865f453da459cb258b07ba86dbaf03

Historical statement excluded from current envelopes; normalized projected descent is represented by the separate b4 record. The b1 record is not selected.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: ca0175186f91436fba2e6adfd51cbb11e83b8075cd41742c5f799c5000620d6e

Historical combined claim with a sufficiently-large-Q source guard; not adopted in the current comparison envelopes.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 1fe944fb9b2b634353f5636cab92a1f90f61423653bdb330e2d2b0e47afd3c2e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: fdc1dac28d2e0ef28ed244ed4c2e233ff3d4af99a6277447f93c9fb04dadd408

SO_ZO_O01__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 23d015bbceffbae595c11ac10da2407fb5fb65d7477a97c1a9155484824d25ec

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: b7f6ce980a74a0d3d2d0281158c60503f30071680c97ca527c78395e6f4476fe

The literal historical q2 ID is not merged with q1. Its logarithmic consequence is now independently proved and adopted through q1 b6, so this is not an unresolved absence of a legal logarithmic lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 01684449126ff4a5f798cf2be278736b80b44cf56685cb5068959bfed1dfcc16

Its own frozen q2 contract; dimension branch Q>=32 and logarithmic branch Q>=128^2, maximized only on their common window.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: b5d04145dc30ef7662bb9644ad2b059a38d1a2c348c3fc55a386821d22ff9222

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 4377b596e107dcc0b1035360b02736c84885f3ffb13058a0abbc7b2ffa67670d

J2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 32a4728c80f62576358af5b408e940b383d6ca1f4528d86e51c699c57e1a0da5

SO_ZO_O01__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 424e7eefce05b301d0fe69a63b2693ec90d2a668bf5a8de0ca91724494093882

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 66190fd94763a22e0d2b2d1ba03dff13c067f274c622a2a8662f615df79e4b4b

Unchanged q1 lower retained conditionally from the frozen baseline and its exact-value simulation proof; not freshly recertified.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: a01215ff5cf3c1b385b8154f12676359b3f6e119569f2a917ee4023f2e0df864

Q>=32, d>=1, exact frozen guard in /bounds/2/applicability

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: b3a7e4735ec4558ac1e07963c7a3c27a0a78706d131600fe840498fffafb46f6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: dc2f63ea57ebae0831a35a8ae5589c6858967000c05b9c516c2444c26a296bc8

SO_ZO_O01__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 39efec2f18938c1e76fe13d490dca42933372e35252d5f98d5f493c0630eba87

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: f058a36ede1d8055c583234579be7ab841fcf21df085076edc60add65a9ba355

ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: fd92dbace71db0f7a48ab7769f0417e721fc5da695da688be5db327c7cfb1513

A compatible deterministic accelerated upper bound gives the selected envelope in this parameter region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: e8ed069bc07eedda6b92b3722606bf226fa288aa8f5b81bfc96f2a13038f5920

d>=1; beta,R,epsilon>0; Q>=32.

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: d841ba54897d3090b8b724834ce99ff2f7ca5c862167dd228c154ac2f1c7bbfa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: d8d35e6d16826e60f26624407b143f862fa3f8dd8c38f052626682ca2f5ef993

$Q=\beta R^2/\varepsilon\ge32$ and $Q>d^2$.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: b53e7b0873c06f88f5bffea2268f8de5ed4c33bea1d9734fb432abf2200948db

SO_ZO_O01__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: a5fa34774cf7a7b63dd5ef5678040eceda8a5c4f2551d98d4c9c81df7e43cd4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 2ff70ff2e71c0814360472ade1a9ceefa94cb2ce744805f0092e4820514aeb0f

ZO_PROOF_COMPARE_CENTROID_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: a79d2f14db7a67252089ba2bee4146fbf4ee4056e36418eb9a9625df71ffd8f3

Included as an explicit quantity-matched native participant.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: 0e0cbe0bc337892d272e3896d8bd8b440b843a3c4f18d8f8d722f74667edcfb9

Exact bound guard; see native applicability.

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: ae839923771330a0ebfccf3a5cd532ed6a188000c93571eeaedcb6297905a0aa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: d8d35e6d16826e60f26624407b143f862fa3f8dd8c38f052626682ca2f5ef993

$Q=\beta R^2/\varepsilon\ge32$ and $Q>d^2$.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: 4564df58db2937c9f80324ec6f350bc311995c0e0b7bcb2851329b287561dff7

SO_ZO_O01__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 23d015bbceffbae595c11ac10da2407fb5fb65d7477a97c1a9155484824d25ec

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: a79d2f14db7a67252089ba2bee4146fbf4ee4056e36418eb9a9625df71ffd8f3

Included as an explicit quantity-matched native participant.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: 0e0cbe0bc337892d272e3896d8bd8b440b843a3c4f18d8f8d722f74667edcfb9

Exact bound guard; see native applicability.

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/bound_uses/6; canonical SHA-256: ce17b09e3421db8176c473df0d1242e24861d104385cb14938b3542c28eb312e

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/bound_id; canonical SHA-256: b952f88b796514dfc643f8bcd2843a229051a68a0ebd25d5a81f69aa04437472

SO_ZO_O01__deterministic__public_acceleration_20261124

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/adopted_region; canonical SHA-256: d8d35e6d16826e60f26624407b143f862fa3f8dd8c38f052626682ca2f5ef993

$Q=\beta R^2/\varepsilon\ge32$ and $Q>d^2$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/validity_region; canonical SHA-256: c1db85e4f2d169498d0ced1d03dd56b3b992ad5442c262d481a482a1145f2a99

$d\ge1$; $\beta,R,\varepsilon>0$; $Q=\beta R^2/\varepsilon\ge1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/reason; canonical SHA-256: bd2442e88fa38f483ce7c244ad572371747aa35a2ed2e52c56408545ddad68b1

The deterministic witness has the native fixed-cap objective-gap guarantee; source binary replies cost one native comparison.

#### Native item 8

Native pointer: /joint_analysis/comparisons/1/bound_uses/7; canonical SHA-256: 6a3c30cc930ebc7d6d7272f2342d8553ebfbb6fe8034d1aa2aed5f7f912ca527

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/bound_id; canonical SHA-256: 0eb79b631c7cf7804e3bcb32dde1a433bc5dd53a801eacd290bb2480c7db9ddb

SO_ZO_O01__deterministic__kimi_full_history_20261124

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/validity_region; canonical SHA-256: ebc80cacc2cff1e6654547026e0e9d7a85a5453b8c465b5c17551cf3fafbb050

$d\ge1$; $\beta,R,\varepsilon>0$; $32\le Q=\beta R^2/\varepsilon\le d^2$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/reason; canonical SHA-256: 67637da03f9ff3d650f6976fc73d1936afd0e20f146905367cf0cae8aa702b26

The full-history theorem is stated only through Q<=d^2.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 37d777769bc774a9718833e8d563403523db27ba30659ad2fb759db18fd3b875

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 1b83fb6d7496f18aea8752942223656b58a4c11a0eed5549c6fff8b7ed96c9b0

$Q=32$ is included. $Q=d^2$ belongs to the first regime; that regime is empty for $d\le5$.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: d0907a49aec11ef20b3d6d6620b8e83b5911ddaacc7221de6e3e588ccad3f135

The accelerated upper applies for all $Q\ge1$; its selected lower comparison uses the common guard $Q\ge32$.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 5770c045496a43b0c68c8da6d665b55967dcd2e18117c217dae7e06080d10d8a

The high-accuracy envelope includes the direct ternary-packing lower $\Omega(d\log Q)$ on its original guard $Q\ge32$.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: b793fa087ac64102c83a8abbecf35d1db7db2b87bf6e3db695537677d3dc8c0e

Only the stated parameter domains and guarantees are compared; the coarse-accuracy complement is separate.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 736c71428e7dcfdfb994b59904379424681d84cf84c6e7ec6ddd617f60f508e3

$O\!\left(\frac{\min\{\sqrt Q[d\log(2dQ)+\log^2(2Q)],d^2\log Q\log(dQ)\}}{d\max\{d,\log Q\}}\right)\le O(\min\{d,\log Q\}\log(dQ))$.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: f61991308c89358ec1cbcaa5596802f6d09c606f02d8765172ebf2b2044157e7

\Omega(d\max\{d,\log Q\})

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: d1893136fdd4e759fc9a23b87bf5220063c2f8b658b25518054a4a09613b6cc9

The ratio is at most logarithmic in the joint dimension-accuracy variables; constants and logarithmic exponents are not matched.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: ed64b4fd2921cd28e826a9d2abb50bc019181963ee068345ff5ab3702fbbdfe8

O\!\left(\min\!\left\{\sqrt Q\,[d\log(2dQ)+\log^2(2Q)],\ d^2\log Q\log(dQ)\right\}\right)

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 871343dab1a4ad03add8d15146f8e762141803be6a721bfd96f7c9defd337a03

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 4cafd9cb5d6773033d88515986a115a19826aa307c1abd82b1dc8551c6cc2c46

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: b260a94b3ff3c210ef7785614b434725bbb01b44ed7a8b13c4393914f72d5225

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 1094eddba8ed22be4cd6f0260b7d07ebe0f24d26a76f35a74621caad7cbf1310

SO_ZO_O01__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 39efec2f18938c1e76fe13d490dca42933372e35252d5f98d5f493c0630eba87

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: f058a36ede1d8055c583234579be7ab841fcf21df085076edc60add65a9ba355

ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: c161d6f6fcddb27b81f9797ed3b0ca2dae865f453da459cb258b07ba86dbaf03

Historical statement excluded from current envelopes; normalized projected descent is represented by the separate b4 record. The b1 record is not selected.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: ca0175186f91436fba2e6adfd51cbb11e83b8075cd41742c5f799c5000620d6e

Historical combined claim with a sufficiently-large-Q source guard; not adopted in the current comparison envelopes.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 065b11fea49812014e37694216dcfd8030f97676c9e8c84f43d457cd8f0a1389

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 394a4ded4bd867545123777d3e698294cee5b969ff71bee54d3920da63ad93fe

SO_ZO_O01__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 23d015bbceffbae595c11ac10da2407fb5fb65d7477a97c1a9155484824d25ec

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: b7f6ce980a74a0d3d2d0281158c60503f30071680c97ca527c78395e6f4476fe

The literal historical q2 ID is not merged with q1. Its logarithmic consequence is now independently proved and adopted through q1 b6, so this is not an unresolved absence of a legal logarithmic lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 01684449126ff4a5f798cf2be278736b80b44cf56685cb5068959bfed1dfcc16

Its own frozen q2 contract; dimension branch Q>=32 and logarithmic branch Q>=128^2, maximized only on their common window.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: 6b2e5fc1fed2183ac8f99e05ac07fc208cc99de49f5b4b69d7a33f426e9903e6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: e9865214587940cf09761cc1ce224e9f092314a4af47482f75603ab03b3c6b1b

J1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: 6d92c38962e03a044299705004005375c85d0c7f856966cf613f460685a9e226

SO_ZO_O01__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 424e7eefce05b301d0fe69a63b2693ec90d2a668bf5a8de0ca91724494093882

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 66190fd94763a22e0d2b2d1ba03dff13c067f274c622a2a8662f615df79e4b4b

Unchanged q1 lower retained conditionally from the frozen baseline and its exact-value simulation proof; not freshly recertified.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 8dcb616c23d606ab3db336eb46d5949f6aaad468fbf10e34571204cda932ff79

Q>=32, d>=1, exact frozen guard in /bounds/5/applicability

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: 138056ed8115351be56b4a91b178b9ba7550ac1273ae0b4443c3d09631938c76

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: 260ce8d2b58f7636db409761b59817a9603b0b5036978b2ef8b267f1a5d36cee

SO_ZO_O01__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 39efec2f18938c1e76fe13d490dca42933372e35252d5f98d5f493c0630eba87

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: f058a36ede1d8055c583234579be7ab841fcf21df085076edc60add65a9ba355

ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: fd92dbace71db0f7a48ab7769f0417e721fc5da695da688be5db327c7cfb1513

A compatible deterministic accelerated upper bound gives the selected envelope in this parameter region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: e8ed069bc07eedda6b92b3722606bf226fa288aa8f5b81bfc96f2a13038f5920

d>=1; beta,R,epsilon>0; Q>=32.

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: c33a1d724af26fc7e5fe86545fb10ea2969a5482d85d421ffd091c266c690f07

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: 001fe84b5cb801569ba3daa58c323122399a8e776c74c0c12ed1c81d2f60bdbd

SO_ZO_O01__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: a5fa34774cf7a7b63dd5ef5678040eceda8a5c4f2551d98d4c9c81df7e43cd4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 2ff70ff2e71c0814360472ade1a9ceefa94cb2ce744805f0092e4820514aeb0f

ZO_PROOF_COMPARE_CENTROID_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: fd92dbace71db0f7a48ab7769f0417e721fc5da695da688be5db327c7cfb1513

A compatible deterministic accelerated upper bound gives the selected envelope in this parameter region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 0e0cbe0bc337892d272e3896d8bd8b440b843a3c4f18d8f8d722f74667edcfb9

Exact bound guard; see native applicability.

#### Native item 6

Native pointer: /joint_analysis/comparisons/2/bound_uses/5; canonical SHA-256: 0d5cd930dee1c72acbe3a78eb06fef2ef28b7bf46377fc6ca8608cb6489f34da

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/adopted_region; canonical SHA-256: 2b8dea31a21cf686ceeb0d6df6eda4747d5a1655fca0f738c9e3304bc01593e9

$32\le Q=\beta R^2/\varepsilon\le d^2$.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/bound_id; canonical SHA-256: 8395bb94fe4392c3e7b9ceab418cb7460e53e8367dad2845b7cf064a23134efd

SO_ZO_O01__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs; canonical SHA-256: 23d015bbceffbae595c11ac10da2407fb5fb65d7477a97c1a9155484824d25ec

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/reason; canonical SHA-256: a79d2f14db7a67252089ba2bee4146fbf4ee4056e36418eb9a9625df71ffd8f3

Included as an explicit quantity-matched native participant.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/validity_region; canonical SHA-256: 0e0cbe0bc337892d272e3896d8bd8b440b843a3c4f18d8f8d722f74667edcfb9

Exact bound guard; see native applicability.

#### Native item 7

Native pointer: /joint_analysis/comparisons/2/bound_uses/6; canonical SHA-256: 08c6453a1982bd4401a4090333669a1238999eff0aba12c33ae63336433d3404

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/bound_id; canonical SHA-256: fee9340f3ff00a34adbe5cd0ab111e70b7d2eee02f202c41854a3388a70dc7e7

SO_ZO_O01__randomized__public_acceleration_20261124

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/adopted_region; canonical SHA-256: 2b8dea31a21cf686ceeb0d6df6eda4747d5a1655fca0f738c9e3304bc01593e9

$32\le Q=\beta R^2/\varepsilon\le d^2$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/validity_region; canonical SHA-256: c1db85e4f2d169498d0ced1d03dd56b3b992ad5442c262d481a482a1145f2a99

$d\ge1$; $\beta,R,\varepsilon>0$; $Q=\beta R^2/\varepsilon\ge1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/reason; canonical SHA-256: bd2442e88fa38f483ce7c244ad572371747aa35a2ed2e52c56408545ddad68b1

The deterministic witness has the native fixed-cap objective-gap guarantee; source binary replies cost one native comparison.

#### Native item 8

Native pointer: /joint_analysis/comparisons/2/bound_uses/7; canonical SHA-256: 683743befccea558aeac5214d0a67730c97bc709dd5da9a1c233a89634e7a087

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/bound_id; canonical SHA-256: fbe33af89a83937981738d13a11070125a4bc1ac710a460e0effc1264cf3d844

SO_ZO_O01__randomized__kimi_full_history_20261124

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/validity_region; canonical SHA-256: ebc80cacc2cff1e6654547026e0e9d7a85a5453b8c465b5c17551cf3fafbb050

$d\ge1$; $\beta,R,\varepsilon>0$; $32\le Q=\beta R^2/\varepsilon\le d^2$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/reason; canonical SHA-256: 6362835cabc35b6ec4be5bcfc8722f9a52350945d783384dd26f3050266dab15

The valid full-history witness has a larger recorded upper order in this region.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 37d777769bc774a9718833e8d563403523db27ba30659ad2fb759db18fd3b875

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: 1b83fb6d7496f18aea8752942223656b58a4c11a0eed5549c6fff8b7ed96c9b0

$Q=32$ is included. $Q=d^2$ belongs to the first regime; that regime is empty for $d\le5$.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: d0907a49aec11ef20b3d6d6620b8e83b5911ddaacc7221de6e3e588ccad3f135

The accelerated upper applies for all $Q\ge1$; its selected lower comparison uses the common guard $Q\ge32$.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/boundary_checks/2; canonical SHA-256: 5770c045496a43b0c68c8da6d665b55967dcd2e18117c217dae7e06080d10d8a

The high-accuracy envelope includes the direct ternary-packing lower $\Omega(d\log Q)$ on its original guard $Q\ge32$.

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/boundary_checks/3; canonical SHA-256: b793fa087ac64102c83a8abbecf35d1db7db2b87bf6e3db695537677d3dc8c0e

Only the stated parameter domains and guarantees are compared; the coarse-accuracy complement is separate.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: cc2adcdeb65a438290336ef59b9e53c064be187cbbb60d5d9055c35bad62c634

$O(\log(2dQ)+d^{-1}\log^2(2Q))=O(\log d)$ on $32\le Q\le d^2$.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 56a7d83b93fc7928ef7ef6598f1c795e0edf185dd48bf150f50698d59adc0952

\Omega(d\sqrt Q)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: d1893136fdd4e759fc9a23b87bf5220063c2f8b658b25518054a4a09613b6cc9

The ratio is at most logarithmic in the joint dimension-accuracy variables; constants and logarithmic exponents are not matched.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: a04447034ae1b8240b691f6a269573ee1e2cede8a42fbe2def4df7797fe71122

O\!\left(\sqrt Q\,[d\log(2dQ)+\log^2(2Q)]\right)

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: bf1c38e194d4e96425d89b7d1a1015cd34741b6dbf4cc221f2d471f8db0961d4

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: f06464f6d09d5509d0aa0374a97a943729e4f3e228e41b659e61ab70bde0d2ae

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: b260a94b3ff3c210ef7785614b434725bbb01b44ed7a8b13c4393914f72d5225

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 1094eddba8ed22be4cd6f0260b7d07ebe0f24d26a76f35a74621caad7cbf1310

SO_ZO_O01__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 39efec2f18938c1e76fe13d490dca42933372e35252d5f98d5f493c0630eba87

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: f058a36ede1d8055c583234579be7ab841fcf21df085076edc60add65a9ba355

ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: c161d6f6fcddb27b81f9797ed3b0ca2dae865f453da459cb258b07ba86dbaf03

Historical statement excluded from current envelopes; normalized projected descent is represented by the separate b4 record. The b1 record is not selected.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: ca0175186f91436fba2e6adfd51cbb11e83b8075cd41742c5f799c5000620d6e

Historical combined claim with a sufficiently-large-Q source guard; not adopted in the current comparison envelopes.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 065b11fea49812014e37694216dcfd8030f97676c9e8c84f43d457cd8f0a1389

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 394a4ded4bd867545123777d3e698294cee5b969ff71bee54d3920da63ad93fe

SO_ZO_O01__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 23d015bbceffbae595c11ac10da2407fb5fb65d7477a97c1a9155484824d25ec

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: b7f6ce980a74a0d3d2d0281158c60503f30071680c97ca527c78395e6f4476fe

The literal historical q2 ID is not merged with q1. Its logarithmic consequence is now independently proved and adopted through q1 b6, so this is not an unresolved absence of a legal logarithmic lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 01684449126ff4a5f798cf2be278736b80b44cf56685cb5068959bfed1dfcc16

Its own frozen q2 contract; dimension branch Q>=32 and logarithmic branch Q>=128^2, maximized only on their common window.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 20674e931795d42bc05bd25adf1e7442d272b5ecac91a073f6b48e8cb38ffe5c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 4377b596e107dcc0b1035360b02736c84885f3ffb13058a0abbc7b2ffa67670d

J2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: 6d92c38962e03a044299705004005375c85d0c7f856966cf613f460685a9e226

SO_ZO_O01__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 424e7eefce05b301d0fe69a63b2693ec90d2a668bf5a8de0ca91724494093882

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 66190fd94763a22e0d2b2d1ba03dff13c067f274c622a2a8662f615df79e4b4b

Unchanged q1 lower retained conditionally from the frozen baseline and its exact-value simulation proof; not freshly recertified.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 8dcb616c23d606ab3db336eb46d5949f6aaad468fbf10e34571204cda932ff79

Q>=32, d>=1, exact frozen guard in /bounds/5/applicability

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 138056ed8115351be56b4a91b178b9ba7550ac1273ae0b4443c3d09631938c76

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: 260ce8d2b58f7636db409761b59817a9603b0b5036978b2ef8b267f1a5d36cee

SO_ZO_O01__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 39efec2f18938c1e76fe13d490dca42933372e35252d5f98d5f493c0630eba87

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: f058a36ede1d8055c583234579be7ab841fcf21df085076edc60add65a9ba355

ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: fd92dbace71db0f7a48ab7769f0417e721fc5da695da688be5db327c7cfb1513

A compatible deterministic accelerated upper bound gives the selected envelope in this parameter region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: e8ed069bc07eedda6b92b3722606bf226fa288aa8f5b81bfc96f2a13038f5920

d>=1; beta,R,epsilon>0; Q>=32.

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: e1fc26a01b94395c7b0565650fc856e4d45d54b5b0a9190e473a5388454236fa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: d8d35e6d16826e60f26624407b143f862fa3f8dd8c38f052626682ca2f5ef993

$Q=\beta R^2/\varepsilon\ge32$ and $Q>d^2$.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: 001fe84b5cb801569ba3daa58c323122399a8e776c74c0c12ed1c81d2f60bdbd

SO_ZO_O01__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: a5fa34774cf7a7b63dd5ef5678040eceda8a5c4f2551d98d4c9c81df7e43cd4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 2ff70ff2e71c0814360472ade1a9ceefa94cb2ce744805f0092e4820514aeb0f

ZO_PROOF_COMPARE_CENTROID_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: a79d2f14db7a67252089ba2bee4146fbf4ee4056e36418eb9a9625df71ffd8f3

Included as an explicit quantity-matched native participant.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: 0e0cbe0bc337892d272e3896d8bd8b440b843a3c4f18d8f8d722f74667edcfb9

Exact bound guard; see native applicability.

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/bound_uses/5; canonical SHA-256: 622448cb78b720a4271e44a6012c249904f9b8c4f806ad467f30050fcfbf80e6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/adopted_region; canonical SHA-256: d8d35e6d16826e60f26624407b143f862fa3f8dd8c38f052626682ca2f5ef993

$Q=\beta R^2/\varepsilon\ge32$ and $Q>d^2$.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/bound_id; canonical SHA-256: 8395bb94fe4392c3e7b9ceab418cb7460e53e8367dad2845b7cf064a23134efd

SO_ZO_O01__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs; canonical SHA-256: 23d015bbceffbae595c11ac10da2407fb5fb65d7477a97c1a9155484824d25ec

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/reason; canonical SHA-256: a79d2f14db7a67252089ba2bee4146fbf4ee4056e36418eb9a9625df71ffd8f3

Included as an explicit quantity-matched native participant.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/validity_region; canonical SHA-256: 0e0cbe0bc337892d272e3896d8bd8b440b843a3c4f18d8f8d722f74667edcfb9

Exact bound guard; see native applicability.

#### Native item 7

Native pointer: /joint_analysis/comparisons/3/bound_uses/6; canonical SHA-256: 4defbbd4cdae11a52b33b5832b6de4d01ac811cd700c7f2e5c3607fce7a891b8

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/bound_id; canonical SHA-256: fee9340f3ff00a34adbe5cd0ab111e70b7d2eee02f202c41854a3388a70dc7e7

SO_ZO_O01__randomized__public_acceleration_20261124

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/adopted_region; canonical SHA-256: d8d35e6d16826e60f26624407b143f862fa3f8dd8c38f052626682ca2f5ef993

$Q=\beta R^2/\varepsilon\ge32$ and $Q>d^2$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/validity_region; canonical SHA-256: c1db85e4f2d169498d0ced1d03dd56b3b992ad5442c262d481a482a1145f2a99

$d\ge1$; $\beta,R,\varepsilon>0$; $Q=\beta R^2/\varepsilon\ge1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/reason; canonical SHA-256: bd2442e88fa38f483ce7c244ad572371747aa35a2ed2e52c56408545ddad68b1

The deterministic witness has the native fixed-cap objective-gap guarantee; source binary replies cost one native comparison.

#### Native item 8

Native pointer: /joint_analysis/comparisons/3/bound_uses/7; canonical SHA-256: 589f225cf0fc4b3ed1d1802fe121c576a690de6dc79d1818c1a93a93af0d930b

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/bound_id; canonical SHA-256: fbe33af89a83937981738d13a11070125a4bc1ac710a460e0effc1264cf3d844

SO_ZO_O01__randomized__kimi_full_history_20261124

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/validity_region; canonical SHA-256: ebc80cacc2cff1e6654547026e0e9d7a85a5453b8c465b5c17551cf3fafbb050

$d\ge1$; $\beta,R,\varepsilon>0$; $32\le Q=\beta R^2/\varepsilon\le d^2$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/reason; canonical SHA-256: 67637da03f9ff3d650f6976fc73d1936afd0e20f146905367cf0cae8aa702b26

The full-history theorem is stated only through Q<=d^2.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: 37d777769bc774a9718833e8d563403523db27ba30659ad2fb759db18fd3b875

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: 1b83fb6d7496f18aea8752942223656b58a4c11a0eed5549c6fff8b7ed96c9b0

$Q=32$ is included. $Q=d^2$ belongs to the first regime; that regime is empty for $d\le5$.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: d0907a49aec11ef20b3d6d6620b8e83b5911ddaacc7221de6e3e588ccad3f135

The accelerated upper applies for all $Q\ge1$; its selected lower comparison uses the common guard $Q\ge32$.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/boundary_checks/2; canonical SHA-256: 5770c045496a43b0c68c8da6d665b55967dcd2e18117c217dae7e06080d10d8a

The high-accuracy envelope includes the direct ternary-packing lower $\Omega(d\log Q)$ on its original guard $Q\ge32$.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/boundary_checks/3; canonical SHA-256: b793fa087ac64102c83a8abbecf35d1db7db2b87bf6e3db695537677d3dc8c0e

Only the stated parameter domains and guarantees are compared; the coarse-accuracy complement is separate.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 736c71428e7dcfdfb994b59904379424681d84cf84c6e7ec6ddd617f60f508e3

$O\!\left(\frac{\min\{\sqrt Q[d\log(2dQ)+\log^2(2Q)],d^2\log Q\log(dQ)\}}{d\max\{d,\log Q\}}\right)\le O(\min\{d,\log Q\}\log(dQ))$.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: f61991308c89358ec1cbcaa5596802f6d09c606f02d8765172ebf2b2044157e7

\Omega(d\max\{d,\log Q\})

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: d1893136fdd4e759fc9a23b87bf5220063c2f8b658b25518054a4a09613b6cc9

The ratio is at most logarithmic in the joint dimension-accuracy variables; constants and logarithmic exponents are not matched.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: ed64b4fd2921cd28e826a9d2abb50bc019181963ee068345ff5ab3702fbbdfe8

O\!\left(\min\!\left\{\sqrt Q\,[d\log(2dQ)+\log^2(2Q)],\ d^2\log Q\log(dQ)\right\}\right)

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 6d3f621d4df39631c0154c9df1046f7017e26a377ac242014a305f56f5387e54

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 66767dd9684b4b2369491c22d58ec6b83d0b7d587e7be6fec604420014cb82a3

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 946fa1f73a3a3ebbda4d05b516a69ee4a8bb9650cd30c43d1b7fbe09e1848867

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: e9865214587940cf09761cc1ce224e9f092314a4af47482f75603ab03b3c6b1b

J1

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: e1c12ec4cce1b6b18e33988f7c97d73324f929ae40881d2c15aa8c818022b970

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 44c6db5006da55f9921e9860c554210dcd524c885fb14fd37ef589ccbbf2e080

Both algorithm views have a compatible deterministic upper and unrestricted randomized lower; the displayed ratio is at most logarithmic.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: fb105f266ed308e35bb2067981d83bf9144b657794d1eb4b3a202ba12c7ffe4d

d>=1; beta,R,epsilon>0; 32<=Q=beta R^2/epsilon<=d^2.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: a431d6038233c1ed438923e754882105f6fe88bd85f810c9dbb201dd2907b873

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 4377b596e107dcc0b1035360b02736c84885f3ffb13058a0abbc7b2ffa67670d

J2

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 3f9b6be22359df8a8737947b2f8b59e8d58ee1d46c23d2e7a57719b818baa8e1

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 44c6db5006da55f9921e9860c554210dcd524c885fb14fd37ef589ccbbf2e080

Both algorithm views have a compatible deterministic upper and unrestricted randomized lower; the displayed ratio is at most logarithmic.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 67f6c432c3ffcc811be665b9d5336d86f4d6ceb040f2429bc1d6e2872eb07631

d>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32 and Q>d^2.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 57adfe640e7155ca78bfa5ca7ff4f595b9706083143510383d6437d8a9d184b0

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 82070baba7d393c6ea60bac8bfa845bf7ca40b5cc19bae90be15d71472ff3e87

C0

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: ddf62098131e17cf8c45b8d4ee20990aac09d0cc33639a8a662979415849e292

Outside all registered comparisons; no native bound/comparison is added. Smoothness gives the elementary zero-query check Q<=2 in ZO_PROOF_COMPARE_UPPER_AUDIT_20261115; the rest, strict triviality threshold and native endpoint registration are unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: e3b2efb49cf13f57886d528aaf2c490c7f571e23e8296d5b54b387eb53ba5f9b

d>=1; beta,R,epsilon>0; 0<Q=beta R^2/epsilon<32.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 65281bc4b79b2c641f3389123378eeff27a5534af8f49659034c927a12aca6a0

For positive Q either Q<32 or Q>=32. In the latter case exactly one of Q<=d^2 and Q>d^2 holds. Equality belongs to J1. Cells are disjoint and cover the native domain for each view; scientific assessment is complete only for the recorded corrected brackets, conditionally retaining lower premises.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: b48167e3f6ec3df11a35e641284ca7a54af4d31b03ffc6a92ed9ea0e7fd3948f

No uncovered parameters: C0 is an explicitly unassessed complement, not a proved gap or open problem.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: b9ef0066ac79b0cb1b421c6dc09ffee72e08eb72778f03bdbf6ee9714c573019

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 4d493ed995c49bca89e1f33a1d7684836de105eecf03fbbaedf3767276cfec1b

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 71d485159100bd0be5240f28bfa41235a8880fd6a64db3b27ec2858be7739eae

The recorded support uses the explicit normalized projected-descent construction and its fixed-cap proof. The historical combined upper claim remains excluded. This entry records a change in the adopted envelope, without asserting a change in the minimax complexity or an exact transition at Q=d.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/0/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/impact/0/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: a6d7212dde5c2f558d75572af54363f0cf036c7eab8187035fc20101c6588537

upper_audit_20261115

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 6c06f6e60d1fffafbecf05f5bed196114bd8cbf586c8ca16008dfb25ef214913

empty; this entry records a historical change in adopted support rather than a rate improvement.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: c46ca557a90fc448f38fb1c804a737c075f3dae0c75773b7f59755a811c72e2c

U_new=O(dQ log(dQ)); L unchanged, with the J1/J2 restrictions in each synthesis.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 6016baadb846a3fc5717ff1cf2231738aa54c23c8d7a605bba18a2793cbe42b3

U_old=O(d min(Q,d) log(dQ)); L unchanged=Omega(d min(d,sqrt(Q))) on Q>=32.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 964c3498ff6acb14d44ce632b1cbde38fada798e03b03c176f747c60ae89df47

The lower side on all J1,J2; the displayed upper rate where Q<=d.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 9186ae0b09595ffe588d61121f27a99e385c708e1f53c0b8ffef3ff2fca07464

J1 union J2 (all d>=1,Q>=32), including equality at Q=32.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 03da783879f02334f5329a03fea2aa99279bd675291f01e1ee3d044834edb598

The separate b4 records specify the normalized projected-descent bound and fixed worst-case comparison budget. Historical b1 records remain excluded.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 513487f3042fb479b65944b6ae55583e076369b8c43ae89bd4bc7b78cdb47ac8

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 1b2052b811c00d6fb34ace1d65dbdac6bf453e4e886e508df609e692ee5ae7d3

v3 is dated 25 June 2026 and subsumes the old note under a new title. Its O(d log(1/angular_accuracy)) primitive is not a deterministic optimization theorem. Adaptive composition, failure allocation, off-promise runtime capping and a uniform optimization proof would be needed for a new native adoption; quantum branches use a different resource.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/impact/1/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: bf5d3ea81fd27d5ce8a36d9c06d60f94a8dfc28b99a45d027655746cec2e04de

v3_primitive_20261115

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 9ba1dbaea2b011c44045e2ccf74730ece23ea4c632a711b8fbf583861175d8ce

empty for the presently verified native optimization claim.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: aa2c3293e096ba1e48d62be04a653b6628856eefd9d170b1639550f411d9e6ff

Same; no v3 optimization bound adopted.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 5e1bc5b9c8ed9a5238ec1453d6b881c754deb2852d08d0771432f4cf86837d9c

Corrected q1 envelopes from upper_audit_20261115.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 43c87883f5f35f6ce941b14f6dc97154eab726d39cab8321e81af1652f471d99

All registered comparisons.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 67c892a18556a0f1ffc9abce879a21b4384eacfa5e7afd6c170a238086f437a0

v3 Problem 2: L-smooth gradient estimation at a point with ||grad f||>=gamma, angular epsilon in (0,1/sqrt(2)); randomized success and classical comparisons.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: b359e3390b6a1cdaa254f3adb5341aaeec56815940f5e950908e0276b396d630

v3 Theorem 3 and Algorithm 4 output a direction, with success at least 2/3, rather than an epsilon-optimal point.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: ba739934727059aed645d0f48fa58ecd72ce05bb43c969f86c053a6da4656699

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 89c68eee8f9daa31b83083d2ee3e66c0b240c538ac8efd1fce3bf0b543216b28

Defines normalized Q and the disjoint domain cells, accounts for unused q2 claims without merging identity, and records the coarse-accuracy complement as unassessed. This finding supplies no independent scientific approval.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/2/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/impact/2/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: e6a4a60863ee31632aa9dfcaf062eb8a891101e1e016b6678e5fc86d239c239e

first_joint_annotation_20261115

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 950ea969076fece983b80cfd731b75461289e06b3035b8ff101e2197891e5834

empty for this auxiliary presentation finding.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 8b0821cf3ae0a0f58442fbf9e6469500db88de3f3cba2da948b2a78592637916

A full first joint-domain annotation, with scientific upper changes supported separately by upper_audit_20261115 and unchanged lower records retained conditionally.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 2a11b580edd68f7f51e040866ffdc1bc320b3ad6ea9e0eb67040ad3814d0b587

No joint_analysis object; native brackets and their frozen guards existed.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 6f5997903e95fc3318e6ca92a15c415752f9e45c3a0b6f39d139df31e40f713c

All scientific rows except the independently supported upper correction and its dependent bracket/status edits.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 7155f74c06702314ab67d275d0783a32e692693365cf8d36cae18fbfa3e00d0e

Native full domain d>=1,beta,R,epsilon>0.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 85b900b25680797919c4b6094aca44a9e66fdb12c0355aa834fc1f291a618c6b

The native q1 quantities track d,beta,R,epsilon jointly; b2 uses distinct q2 IDs.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 49ba7b00511e2c5eb0b0b4407e2e879872900e26bfe53c6562265ea4a01b032a

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: a6527f8c5f06dee2881cd0cfaad3c972fbca38e8052394a4d59e0dd242e84e96

External Grunbaum lemma plus complete estimator/centroid proof and independent ternary packing proof. Old quarantined b1 is never reactivated.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: fbcd418bfd2b8e60608521f421962ea5cca6ea268b0907f7a942a4c9fa135ee5

O01_CENTROID_PACKING_CLOSURE_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 06752a6cb308395c9b519edd826db62081103b52d79284b6c8950361d2466938

Upper strictly better in order when Q/(d logQ)->infinity; lower strictly better when logQ/min(d,sqrtQ)->infinity. These are asymptotic regimes, not exact hidden-constant crossovers.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 2343d3d5cc1113b891566d17d446003dcf3f943f1f8b0f45e31c5c50e5fadfee

O(d min{Q,d logQ}log(dQ)); Omega(d max{min(d,sqrtQ),logQ}).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: 1c32884b148801aa369758b5492b9055b1db759293a468af1280fb6a1382d281

Only O(dQ log(dQ)) active upper; dimension-only b3 lower.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: ae88cd7a279cf69f0b2b4b906638216d5c38ec8c36bda350024a034a43b8717c

All immutable native contracts; all statements outside the explicit new guarded adoption remain unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: bc69360d4efdbad06ee4a4c66d74c792fb7dca9b09aa63867b05f765feac0427

Q>=32; exact native contracts.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 1d4224d473fc02decac2773d251938a6111b965ed0905e6f05253fcd89a1f262

d=1,Q->infinity improves both the recorded upper and lower; Q=d^2,d->infinity reduces the old active upper by order d/log(d).

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: f7cadde0f9c0b11db1abbb1d6d99bea302d4346aac831b88731f507994387300

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: e17691a07d4ae416aa7129f6054fe500b31ef3ea164ea01f1b2d7e0b64b961ad

Separate analyst derivations give the centroid cutting-plane branch from the finite comparison direction estimator and the cited Grunbaum volume theorem. A direct ternary-decision-tree packing lower bound supplements the value-oracle reduction on Q>=32. The envelopes use the explicitly guarded current bounds; historical b1 records remain excluded. Publication and typed projection obligations remain explicit, and historical changes are not counted as new frontier gains.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/4/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/impact/4/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 47143fb2197731b1d93c5e90c4215fdd41421073ae77069c813a52d3cef37323

curated_feedback_SO_ZO_O01_20261116_ab3e5d3796

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

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

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: f18e8cf36d54f3ffe8b7925271411db950281fa054eec9e73faca423a8ca78bf

d in N,d>=1; beta>0,R>0,epsilon>0 (Q>0). Minimax fixed worst-case scalar comparison calls for native global objective-gap optimization, separately deterministic g1 and randomized g1 (success>=2/3).

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: d0b99f8eeee5108c43a7e29cdcd954f2ed3804d6d9cfd942a539ffbd837cbca0

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: e3911bd81e0c3a8c72016be79d4b72cbee6b88f5cc81dbf4004b2164c1cf1599

Discovery remains partial: the broad query has unread records 4-9 and next_cursor=10 of total158. The narrower terminal seven-record page is fully exposed, but potentially relevant leads 2607.26969v2, 2604.26867v2, 2603.00023v1, 2411.16745v1 and 2010.02479v3 are not theorem-assessed.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: dfffb0f68279f101f5fb7020211f0bbda712f396754b7f70553a7a31e99c1247

A sharper single-log cutting-plane rate remains unproved; the complete conservative double-log centroid branch is now adopted.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 6ba7b2fc791733fa5c4cf09619f8511ac8a415e0006b956c2d4caf2a22b638ac

Assess v3 gradient-estimator composition separately before any optimization upper adoption, including adaptive success and deterministic pathwise caps.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 8dc16370729f02eb53b6b726a7ca66f94892caa16267c182ab63678f2fc79343

Other historical q2 identities still require explicit transfers; the q1 d logQ lower no longer depends on such a transfer.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 1edd2f3cab84349f54b8a62a17357b9575421ca4cb95aafe9ddf26c741a19a1b

Register and synthesize coarse-accuracy/zero-query endpoints and sharper d=1 behavior in a separate supported update.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 8d9fc3b6d3ec0d008f196cb1a9d6b3c38e4c3dbfbc51ebe5adbb30cce0c7251c

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 530d7a0399a450e4b042d19f59c0aa4a35c8ece0af6f53582e0e6fb21ce9c8ee

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: dc2f63ea57ebae0831a35a8ae5589c6858967000c05b9c516c2444c26a296bc8

SO_ZO_O01__deterministic__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: b47c3ec75335d4f09da410d03930942ad45d5c515659a1f17900fa823a1535f4

n=d,L=beta. The native proof constructs a fixed-schedule estimator from Lemma1 and derives projected descent. Convexity supplies gamma=epsilon/(2R) under the all-failing-iterates contradiction. Positive finite probes, charged tournament, uniform constants and deterministic containment are explicit.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 39efec2f18938c1e76fe13d490dca42933372e35252d5f98d5f493c0630eba87

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: f058a36ede1d8055c583234579be7ab841fcf21df085076edc60add65a9ba355

ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: deb8536bf94df181c47dc0cf3931bfeb3e2953fdead9c30c0024a5ea4cb1c096

L-smooth f on R^n, known positive gradient lower bound for each direction estimate; source optimization class has a minimizer in B_R.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: a28672feff40872b2abc8c0ae597bf021a5de69b98816c3ab61bef4ad46cebd1

2405.11454v1 Lemma 1, Theorems 1-2 and Problem 1; PDF pp5-8 chars10500-14500,14000-24000; HTML chars25000-35000. Immutable hashes in native evidence and finding upper_audit_20261115.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 407bb103bbbb97d04ea5d263a277297169395a697720ec44592a896f1f8cfe95

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: a4c411849b0792886c4696cc85e8098df55c809ac0ee0b6e01b04b4e83783a28

SO_SRC_25cbefe670f1e510

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 9a98ac78b0c2cb911a88f0b39af054f2c197f5e1a6b5506c9a3d56d92c4fe03b

Native model, d>=1, beta,R,epsilon>0, Q>=32; q1 and declared scalar comparison resource.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: d67596fc5b0eb2ca7b7266c6f4cf31a8108781d804125a0af282c36f98cd37b8

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 32a4728c80f62576358af5b408e940b383d6ca1f4528d86e51c699c57e1a0da5

SO_ZO_O01__deterministic__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 40e7ab3655eac285c9e1a5a3590674d1f927319aa16ea0313963da6517698150

Conditional retention only. The frozen proof records the two-exact-values simulation; no lower envelope or lower scientific record is edited.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 424e7eefce05b301d0fe69a63b2693ec90d2a668bf5a8de0ca91724494093882

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: d2f05ebb69fb1c318d6efeacf2b808165c40767c01b8b2adc0cdd734740fe509

The unchanged primary-source windows recorded in those frozen claims.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 5c4cafd618874c313ae11bdb21c435b34515782d2e3ab0d61d9b3907e4063bfe

Exact frozen /bounds and /proofs records, registered in finding first_joint_annotation_20261115.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 977241fab46979879bf0f9f29328779d6f47061fda21d0440ffd0866219d845e

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native item 2

Native pointer: /joint_analysis/provenance/1/source_refs/1; canonical SHA-256: cae76ce93df3e19a425b1d241baeefabe3ec71bc0147013d0a00884e08fe70b7

SO_SRC_12e2b72bb6c9ca16

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: f3bdcc796e137f91f07959144f9cd2e53691b7a4028b8a81615e8fd83099cb9d

Q>=32; native deterministic q1 and fixed comparison budget.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 9f059443226d9cf3af245e680d7520da53ed116c0bd4a98a4f07ad942c59cf73

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 260ce8d2b58f7636db409761b59817a9603b0b5036978b2ef8b267f1a5d36cee

SO_ZO_O01__randomized__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: b47c3ec75335d4f09da410d03930942ad45d5c515659a1f17900fa823a1535f4

n=d,L=beta. The native proof constructs a fixed-schedule estimator from Lemma1 and derives projected descent. Convexity supplies gamma=epsilon/(2R) under the all-failing-iterates contradiction. Positive finite probes, charged tournament, uniform constants and deterministic containment are explicit.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 39efec2f18938c1e76fe13d490dca42933372e35252d5f98d5f493c0630eba87

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: f058a36ede1d8055c583234579be7ab841fcf21df085076edc60add65a9ba355

ZO_PROOF_COMPARE_UPPER_AUDIT_20261115

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: deb8536bf94df181c47dc0cf3931bfeb3e2953fdead9c30c0024a5ea4cb1c096

L-smooth f on R^n, known positive gradient lower bound for each direction estimate; source optimization class has a minimizer in B_R.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: a28672feff40872b2abc8c0ae597bf021a5de69b98816c3ab61bef4ad46cebd1

2405.11454v1 Lemma 1, Theorems 1-2 and Problem 1; PDF pp5-8 chars10500-14500,14000-24000; HTML chars25000-35000. Immutable hashes in native evidence and finding upper_audit_20261115.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 407bb103bbbb97d04ea5d263a277297169395a697720ec44592a896f1f8cfe95

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: a4c411849b0792886c4696cc85e8098df55c809ac0ee0b6e01b04b4e83783a28

SO_SRC_25cbefe670f1e510

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 9a98ac78b0c2cb911a88f0b39af054f2c197f5e1a6b5506c9a3d56d92c4fe03b

Native model, d>=1, beta,R,epsilon>0, Q>=32; q1 and declared scalar comparison resource.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 595bc6d1c7562a6e533c98cdfc576e3dd05a6420e84c449812d6d74a9f9a55a5

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: 6d92c38962e03a044299705004005375c85d0c7f856966cf613f460685a9e226

SO_ZO_O01__randomized__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 40e7ab3655eac285c9e1a5a3590674d1f927319aa16ea0313963da6517698150

Conditional retention only. The frozen proof records the two-exact-values simulation; no lower envelope or lower scientific record is edited.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 424e7eefce05b301d0fe69a63b2693ec90d2a668bf5a8de0ca91724494093882

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: d2f05ebb69fb1c318d6efeacf2b808165c40767c01b8b2adc0cdd734740fe509

The unchanged primary-source windows recorded in those frozen claims.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 5c4cafd618874c313ae11bdb21c435b34515782d2e3ab0d61d9b3907e4063bfe

Exact frozen /bounds and /proofs records, registered in finding first_joint_annotation_20261115.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 977241fab46979879bf0f9f29328779d6f47061fda21d0440ffd0866219d845e

#### Native item 1

Native pointer: /joint_analysis/provenance/3/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native item 2

Native pointer: /joint_analysis/provenance/3/source_refs/1; canonical SHA-256: cae76ce93df3e19a425b1d241baeefabe3ec71bc0147013d0a00884e08fe70b7

SO_SRC_12e2b72bb6c9ca16

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 6d1a8213dd21682c68d4ffc54c19df0ff49a6a087133af1fbde2ac5a293d4a9c

Q>=32; native randomized q1 and fixed comparison budget.

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: ee4d849edd004feb4e4f8f887d937b585ab5377f79d98cd5a2b75a0bea4cb4dd

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: b53e7b0873c06f88f5bffea2268f8de5ed4c33bea1d9734fb432abf2200948db

SO_ZO_O01__deterministic__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: d99627a1fcf40b25b532ca6ff1b864ae4a6441fd2dff129be46cae2d12eb4f5f

Existing independent direction estimator plus a genuinely new adopted external Grunbaum premise, not pure baseline-only derivation.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: a5fa34774cf7a7b63dd5ef5678040eceda8a5c4f2551d98d4c9c81df7e43cd4b

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: 2ff70ff2e71c0814360472ade1a9ceefa94cb2ce744805f0092e4820514aeb0f

ZO_PROOF_COMPARE_CENTROID_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 2994a28a868ffbb9f17692da867c2d26f5c032173e6faf8d1d753c7701dadb0b

d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: d2fd9f34104e09759ed780073318f3b9f1b4e0037d2736d4109c026d2bb22360

Complete new guided proof ZO_PROOF_COMPARE_CENTROID_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 0130c77557c6cf2f46cca654c50281acbe4632e9b941a9a062517157198c6906

#### Native item 1

Native pointer: /joint_analysis/provenance/4/source_refs/0; canonical SHA-256: d9919b72be4d5d9126f3446008522bf36e04a8d1aa2f4bd71f94c70aab818541

SO_SRC_a00ef97da026391b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 2994a28a868ffbb9f17692da867c2d26f5c032173e6faf8d1d753c7701dadb0b

d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: d5e15b7872cba4c5030061bdacdd3396bce60236e4a86c1cabf0ea69153cec04

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: 4564df58db2937c9f80324ec6f350bc311995c0e0b7bcb2851329b287561dff7

SO_ZO_O01__deterministic__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 0782df87b3fe87c091159f1a74c3f065a84ec003c8749ed9a779d63f087da4e9

A native comparison has at most3 replies; two-value or external multiscale theorems are not needed.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 23d015bbceffbae595c11ac10da2407fb5fb65d7477a97c1a9155484824d25ec

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: 2994a28a868ffbb9f17692da867c2d26f5c032173e6faf8d1d753c7701dadb0b

d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: b3ada12125cae6e1138b54e9a18e65db77c315f885cd28c82cf7ea139d6e6911

Complete new guided proof ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 2994a28a868ffbb9f17692da867c2d26f5c032173e6faf8d1d753c7701dadb0b

d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: 5855b2037484d20e24f85a8da0dfbdeb40954bbca815ed59120e5fa65822ea45

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: 001fe84b5cb801569ba3daa58c323122399a8e776c74c0c12ed1c81d2f60bdbd

SO_ZO_O01__randomized__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: d99627a1fcf40b25b532ca6ff1b864ae4a6441fd2dff129be46cae2d12eb4f5f

Existing independent direction estimator plus a genuinely new adopted external Grunbaum premise, not pure baseline-only derivation.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: a5fa34774cf7a7b63dd5ef5678040eceda8a5c4f2551d98d4c9c81df7e43cd4b

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: 2ff70ff2e71c0814360472ade1a9ceefa94cb2ce744805f0092e4820514aeb0f

ZO_PROOF_COMPARE_CENTROID_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: 2994a28a868ffbb9f17692da867c2d26f5c032173e6faf8d1d753c7701dadb0b

d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: d2fd9f34104e09759ed780073318f3b9f1b4e0037d2736d4109c026d2bb22360

Complete new guided proof ZO_PROOF_COMPARE_CENTROID_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: 0130c77557c6cf2f46cca654c50281acbe4632e9b941a9a062517157198c6906

#### Native item 1

Native pointer: /joint_analysis/provenance/6/source_refs/0; canonical SHA-256: d9919b72be4d5d9126f3446008522bf36e04a8d1aa2f4bd71f94c70aab818541

SO_SRC_a00ef97da026391b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 2994a28a868ffbb9f17692da867c2d26f5c032173e6faf8d1d753c7701dadb0b

d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

#### Native item 8

Native pointer: /joint_analysis/provenance/7; canonical SHA-256: 80a2fa71c6a275831f9882a986d136bf2af0dc37ae96fd4075d1ce0467e8f767

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/7/bound_id; canonical SHA-256: 8395bb94fe4392c3e7b9ceab418cb7460e53e8367dad2845b7cf064a23134efd

SO_ZO_O01__randomized__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/7/mapping; canonical SHA-256: 0782df87b3fe87c091159f1a74c3f065a84ec003c8749ed9a779d63f087da4e9

A native comparison has at most3 replies; two-value or external multiscale theorems are not needed.

#### Native field: origin

Native pointer: /joint_analysis/provenance/7/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/7/proof_refs; canonical SHA-256: 23d015bbceffbae595c11ac10da2407fb5fb65d7477a97c1a9155484824d25ec

#### Native item 1

Native pointer: /joint_analysis/provenance/7/proof_refs/0; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/7/source_domain; canonical SHA-256: 2994a28a868ffbb9f17692da867c2d26f5c032173e6faf8d1d753c7701dadb0b

d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/7/source_locator; canonical SHA-256: b3ada12125cae6e1138b54e9a18e65db77c315f885cd28c82cf7ea139d6e6911

Complete new guided proof ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/7/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/7/target_domain; canonical SHA-256: 2994a28a868ffbb9f17692da867c2d26f5c032173e6faf8d1d753c7701dadb0b

d integer>=1; beta,R,epsilon>0; Q=beta R^2/epsilon>=32.

#### Native item 9

Native pointer: /joint_analysis/provenance/8; canonical SHA-256: b957e7619d8a8d783f581e9c8e3547a61e3c9bd2def53bfce96b6cc63fe04d6c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/8/bound_id; canonical SHA-256: b952f88b796514dfc643f8bcd2843a229051a68a0ebd25d5a81f69aa04437472

SO_ZO_O01__deterministic__public_acceleration_20261124

#### Native field: origin

Native pointer: /joint_analysis/provenance/8/origin; canonical SHA-256: 0ca1a4b8d8757ab03e2cc84f47f117ca352255f4d4434159b8d9e6363c72f259

cited_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/8/source_refs; canonical SHA-256: aaf70ec4323ec339aa6667fd3942cd052ef0966552bf4e45961b2398940b7fd9

#### Native item 1

Native pointer: /joint_analysis/provenance/8/source_refs/0; canonical SHA-256: 5042086d69173ca6eec770806ca8e14d3e2d3846edff44d457dbf5301d05fad7

SO_SRC_RICHTARIK_MAHRAN_2611_29533V1

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/8/source_locator; canonical SHA-256: 9fd52e6dfb20132e5d74cac939f0350c12df73bca66a271c6a9fc714db8bb1ba

Theorem 3.4; Algorithm 2; Appendix B; Lemma F.1

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/8/source_domain; canonical SHA-256: c1db85e4f2d169498d0ced1d03dd56b3b992ad5442c262d481a482a1145f2a99

$d\ge1$; $\beta,R,\varepsilon>0$; $Q=\beta R^2/\varepsilon\ge1$.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/8/target_domain; canonical SHA-256: 2df18b3327384b7d8d1a8eee1cb6a1bbdc9dfd82225b5bb3c5c3b815ffec5bad

$d\ge1$; $\beta,R,\varepsilon>0$; $Q=\beta R^2/\varepsilon\ge1$. Native deterministic g1 and q1.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/8/mapping; canonical SHA-256: 6963ca4b289b7caf126f537bbdddd6de652e9ba6554e57fcbf89226e398b4f26

One native ternary reply implements the source bit $1\{f(x)\ge f(y)\}$: map 0 and +1 to 1, and -1 to 0. All queries remain finite full-space pairs. Deterministic objective gap at most $\varepsilon$ on every instance. The same strategy gives probability one under the randomized view, hence satisfies its per-instance 2/3 guarantee.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 10

Native pointer: /joint_analysis/provenance/9; canonical SHA-256: 0b7ff673da3a71c78c36fe72ebb8d9e5bdba5945a4a644c5290b06ea317db071

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/9/bound_id; canonical SHA-256: 0eb79b631c7cf7804e3bcb32dde1a433bc5dd53a801eacd290bb2480c7db9ddb

SO_ZO_O01__deterministic__kimi_full_history_20261124

#### Native field: origin

Native pointer: /joint_analysis/provenance/9/origin; canonical SHA-256: 0ca1a4b8d8757ab03e2cc84f47f117ca352255f4d4434159b8d9e6363c72f259

cited_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/9/source_refs; canonical SHA-256: 8b9dd81aa011e1914d549a29c21e54580557cff1bf98354f36b8daa27e088770

#### Native item 1

Native pointer: /joint_analysis/provenance/9/source_refs/0; canonical SHA-256: 2e0b09f5e204690ae81af9ccb225721f6cb7b23e62a6c36b360cdb946ae4a07e

COLOMBO_KIMI_002

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/9/source_locator; canonical SHA-256: 63cca7957a86caed667c239bbf5b44ac804a4634ccaaf1caa50d609c716f1393

Theorem 5; Section 7; equation (2); Lemma 1; Proposition 1; Lemma 2

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/9/source_domain; canonical SHA-256: ebc80cacc2cff1e6654547026e0e9d7a85a5453b8c465b5c17551cf3fafbb050

$d\ge1$; $\beta,R,\varepsilon>0$; $32\le Q=\beta R^2/\varepsilon\le d^2$.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/9/target_domain; canonical SHA-256: 9fd772629fcbe141e093fb4f35693b4b305216691d80bdb77b141f655518d2c2

$d\ge1$; $\beta,R,\varepsilon>0$; $32\le Q=\beta R^2/\varepsilon\le d^2$. Native deterministic g1 and q1.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/9/mapping; canonical SHA-256: 91f5a3497e0cb94ee72bd9c6f9bc629b9f18713df2611bb0b8ca1c3209134e29

The source uses the same full-space ternary exact comparison oracle, including zero on ties. Direction probes, inner solves and selection use only comparisons. Deterministic objective gap at most $\varepsilon$ on every instance. The same strategy gives probability one under the randomized view, hence satisfies its per-instance 2/3 guarantee.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 11

Native pointer: /joint_analysis/provenance/10; canonical SHA-256: b0c35aae83e7f705bb91731ec2182469fd7e7f37ee51bad089e170f78a9a912c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/10/bound_id; canonical SHA-256: fee9340f3ff00a34adbe5cd0ab111e70b7d2eee02f202c41854a3388a70dc7e7

SO_ZO_O01__randomized__public_acceleration_20261124

#### Native field: origin

Native pointer: /joint_analysis/provenance/10/origin; canonical SHA-256: 0ca1a4b8d8757ab03e2cc84f47f117ca352255f4d4434159b8d9e6363c72f259

cited_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/10/source_refs; canonical SHA-256: aaf70ec4323ec339aa6667fd3942cd052ef0966552bf4e45961b2398940b7fd9

#### Native item 1

Native pointer: /joint_analysis/provenance/10/source_refs/0; canonical SHA-256: 5042086d69173ca6eec770806ca8e14d3e2d3846edff44d457dbf5301d05fad7

SO_SRC_RICHTARIK_MAHRAN_2611_29533V1

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/10/source_locator; canonical SHA-256: 9fd52e6dfb20132e5d74cac939f0350c12df73bca66a271c6a9fc714db8bb1ba

Theorem 3.4; Algorithm 2; Appendix B; Lemma F.1

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/10/source_domain; canonical SHA-256: c1db85e4f2d169498d0ced1d03dd56b3b992ad5442c262d481a482a1145f2a99

$d\ge1$; $\beta,R,\varepsilon>0$; $Q=\beta R^2/\varepsilon\ge1$.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/10/target_domain; canonical SHA-256: 12a9f1bb5562008a2136c705a5510f96f01a3a49a9d3e8726b54ee497fedab50

$d\ge1$; $\beta,R,\varepsilon>0$; $Q=\beta R^2/\varepsilon\ge1$. Native randomized g1 and q1.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/10/mapping; canonical SHA-256: 6963ca4b289b7caf126f537bbdddd6de652e9ba6554e57fcbf89226e398b4f26

One native ternary reply implements the source bit $1\{f(x)\ge f(y)\}$: map 0 and +1 to 1, and -1 to 0. All queries remain finite full-space pairs. Deterministic objective gap at most $\varepsilon$ on every instance. The same strategy gives probability one under the randomized view, hence satisfies its per-instance 2/3 guarantee.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 12

Native pointer: /joint_analysis/provenance/11; canonical SHA-256: 8d98437572649d21a9ffc7670b90e5440bd1d07bb6c7cb1ca5e6cdf53bfceb56

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/11/bound_id; canonical SHA-256: fbe33af89a83937981738d13a11070125a4bc1ac710a460e0effc1264cf3d844

SO_ZO_O01__randomized__kimi_full_history_20261124

#### Native field: origin

Native pointer: /joint_analysis/provenance/11/origin; canonical SHA-256: 0ca1a4b8d8757ab03e2cc84f47f117ca352255f4d4434159b8d9e6363c72f259

cited_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/11/source_refs; canonical SHA-256: 8b9dd81aa011e1914d549a29c21e54580557cff1bf98354f36b8daa27e088770

#### Native item 1

Native pointer: /joint_analysis/provenance/11/source_refs/0; canonical SHA-256: 2e0b09f5e204690ae81af9ccb225721f6cb7b23e62a6c36b360cdb946ae4a07e

COLOMBO_KIMI_002

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/11/source_locator; canonical SHA-256: 63cca7957a86caed667c239bbf5b44ac804a4634ccaaf1caa50d609c716f1393

Theorem 5; Section 7; equation (2); Lemma 1; Proposition 1; Lemma 2

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/11/source_domain; canonical SHA-256: ebc80cacc2cff1e6654547026e0e9d7a85a5453b8c465b5c17551cf3fafbb050

$d\ge1$; $\beta,R,\varepsilon>0$; $32\le Q=\beta R^2/\varepsilon\le d^2$.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/11/target_domain; canonical SHA-256: f1e6833546bf46bb70dbb47b40c468fe2c7c1212c85eca2d1f07682a93c6a4da

$d\ge1$; $\beta,R,\varepsilon>0$; $32\le Q=\beta R^2/\varepsilon\le d^2$. Native randomized g1 and q1.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/11/mapping; canonical SHA-256: 91f5a3497e0cb94ee72bd9c6f9bc629b9f18713df2611bb0b8ca1c3209134e29

The source uses the same full-space ternary exact comparison oracle, including zero on ties. Direction probes, inner solves and selection use only comparisons. Deterministic objective gap at most $\varepsilon$ on every instance. The same strategy gives probability one under the randomized view, hence satisfies its per-instance 2/3 guarantee.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 66569f0da34e5f96d8a082bf1daf72a10a7059a7af8e66aec5f43e8c54e237e4

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 852a252619b9c1e67d57f7ed7a2178aa08233e02cf63011d819c597f593124a2

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 74951c162352d92dd760c2009d1a3ce3bab76caaf6681abf243dd583723f85e4

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: 85bd74e003ad4315f9ce6b929e00f262e0d72db16e2f922bed8e0b9760a2a740

The selected upper is the minimum of compatible deterministic witnesses where both apply. The lower is the maximum of dimension-accuracy hardness and direct ternary-packing hardness. All share the native quantity, guarantee and fixed scalar-comparison resource.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 6c1216df22e1dd905c93e890879f3d28992840d8108a9be51e318439e8805973

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: b952f88b796514dfc643f8bcd2843a229051a68a0ebd25d5a81f69aa04437472

SO_ZO_O01__deterministic__public_acceleration_20261124

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 32a4728c80f62576358af5b408e940b383d6ca1f4528d86e51c699c57e1a0da5

SO_ZO_O01__deterministic__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 4564df58db2937c9f80324ec6f350bc311995c0e0b7bcb2851329b287561dff7

SO_ZO_O01__deterministic__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 0ab551cb0737bf8bcc122e76070b85be0634fa95e82f14862196ade201866bb0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 872112880ca08ba014986d9efa8d0d6c9fea415c373a5155aa40859c8f85090d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/0; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/1; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 219c2bff0ca9c2914135b37f21ed2ddfcd5a13103663f487bd2ccde255e9018a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: 85bd74e003ad4315f9ce6b929e00f262e0d72db16e2f922bed8e0b9760a2a740

The selected upper is the minimum of compatible deterministic witnesses where both apply. The lower is the maximum of dimension-accuracy hardness and direct ternary-packing hardness. All share the native quantity, guarantee and fixed scalar-comparison resource.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 20963becb0f19f621d6fad664e392be7bdec33e74cbe1797d323441f90f4832a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: b952f88b796514dfc643f8bcd2843a229051a68a0ebd25d5a81f69aa04437472

SO_ZO_O01__deterministic__public_acceleration_20261124

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: b53e7b0873c06f88f5bffea2268f8de5ed4c33bea1d9734fb432abf2200948db

SO_ZO_O01__deterministic__b5

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 32a4728c80f62576358af5b408e940b383d6ca1f4528d86e51c699c57e1a0da5

SO_ZO_O01__deterministic__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: 4564df58db2937c9f80324ec6f350bc311995c0e0b7bcb2851329b287561dff7

SO_ZO_O01__deterministic__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: a0ccd79617dc5be9a12230b1639a0e1af61b5dda68e120493c45dbc3f80ee5fb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 23d5e2dc9c3d53ae566541305705f3d9308aec86b56c12717fe6005c3a13b056

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/0; canonical SHA-256: 2ff70ff2e71c0814360472ade1a9ceefa94cb2ce744805f0092e4820514aeb0f

ZO_PROOF_COMPARE_CENTROID_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/1; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/2; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 86f252e030621b18e974ccec653501fbdd4649194a127ae8c2fa7430da57cc8a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: 85bd74e003ad4315f9ce6b929e00f262e0d72db16e2f922bed8e0b9760a2a740

The selected upper is the minimum of compatible deterministic witnesses where both apply. The lower is the maximum of dimension-accuracy hardness and direct ternary-packing hardness. All share the native quantity, guarantee and fixed scalar-comparison resource.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 181c3039934e275f6e8f167debdefe09599fecad56d14263e33a4bda0d335461

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: fee9340f3ff00a34adbe5cd0ab111e70b7d2eee02f202c41854a3388a70dc7e7

SO_ZO_O01__randomized__public_acceleration_20261124

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 6d92c38962e03a044299705004005375c85d0c7f856966cf613f460685a9e226

SO_ZO_O01__randomized__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 8395bb94fe4392c3e7b9ceab418cb7460e53e8367dad2845b7cf064a23134efd

SO_ZO_O01__randomized__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 384c4a5692b263e47ec2d974b926db7ca09713d0eb53cd971766b382b8b5ed08

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 872112880ca08ba014986d9efa8d0d6c9fea415c373a5155aa40859c8f85090d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/0; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/1; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 12c522faaa129cce7224878014f5729aedf5a2250be8304b114c04daaf776d4a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 85bd74e003ad4315f9ce6b929e00f262e0d72db16e2f922bed8e0b9760a2a740

The selected upper is the minimum of compatible deterministic witnesses where both apply. The lower is the maximum of dimension-accuracy hardness and direct ternary-packing hardness. All share the native quantity, guarantee and fixed scalar-comparison resource.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: f682a9a639b93473cb470f5d74faa6ed073b60add729cfa6f689ed0f379166f0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: fee9340f3ff00a34adbe5cd0ab111e70b7d2eee02f202c41854a3388a70dc7e7

SO_ZO_O01__randomized__public_acceleration_20261124

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 001fe84b5cb801569ba3daa58c323122399a8e776c74c0c12ed1c81d2f60bdbd

SO_ZO_O01__randomized__b5

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: 6d92c38962e03a044299705004005375c85d0c7f856966cf613f460685a9e226

SO_ZO_O01__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/3; canonical SHA-256: 8395bb94fe4392c3e7b9ceab418cb7460e53e8367dad2845b7cf064a23134efd

SO_ZO_O01__randomized__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 00205a37393a275d0a577d8293246cc30214c2ba2c5d701edfdf32c15dc76dc9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 23d5e2dc9c3d53ae566541305705f3d9308aec86b56c12717fe6005c3a13b056

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs/0; canonical SHA-256: 2ff70ff2e71c0814360472ade1a9ceefa94cb2ce744805f0092e4820514aeb0f

ZO_PROOF_COMPARE_CENTROID_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs/1; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs/2; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: a827b704e302a7475de249029f69a402d1d5126ee49eb27f66bf2b4398f493bd

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: d0167f548742ead3d895787ec442b4a84beeb280ebe70d01f9a7603611e9c56f

remaining-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: e3911bd81e0c3a8c72016be79d4b72cbee6b88f5cc81dbf4004b2164c1cf1599

Discovery remains partial: the broad query has unread records 4-9 and next_cursor=10 of total158. The narrower terminal seven-record page is fully exposed, but potentially relevant leads 2607.26969v2, 2604.26867v2, 2603.00023v1, 2411.16745v1 and 2010.02479v3 are not theorem-assessed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 2198fd2ed9a1aa4b28053e48ff85f8fc6214758add43b598c3346ca1bf4602d1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: a4b3d9806c41184784f257b17680c859184105b903c13a4dc473b5d4a38646ea

remaining-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: dfffb0f68279f101f5fb7020211f0bbda712f396754b7f70553a7a31e99c1247

A sharper single-log cutting-plane rate remains unproved; the complete conservative double-log centroid branch is now adopted.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 15030d758467ef021549286f3170c77f63c6c32f69271aa4bf54253768c41e41

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 3e14526e35b394fe370a6fc3dd84e97e336771629d764f97e1112f9be119d23a

remaining-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 6ba7b2fc791733fa5c4cf09619f8511ac8a415e0006b956c2d4caf2a22b638ac

Assess v3 gradient-estimator composition separately before any optimization upper adoption, including adaptive success and deterministic pathwise caps.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 73f0d741dcbf59dbd8a54ef6726f3a04cc2677e241bbfd5642f3a9a297c545d2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 2ad76a816cfedf1ea354b21e9948710836a980becdf5124dd84ab11a1a2b3afe

remaining-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 8dc16370729f02eb53b6b726a7ca66f94892caa16267c182ab63678f2fc79343

Other historical q2 identities still require explicit transfers; the q1 d logQ lower no longer depends on such a transfer.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: ab5eab0b20bb21ad3797297c84a0a6827697b988891f396cf7cdccb25f31683d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 8a1018ad75fb3da4cc08ea1e079513debdaa4af5b56952b5988e43572540acde

remaining-lead-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 1edd2f3cab84349f54b8a62a17357b9575421ca4cb95aafe9ddf26c741a19a1b

Register and synthesize coarse-accuracy/zero-query endpoints and sharper d=1 behavior in a separate supported update.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: b7f093a102a0e86776d47ba3cee0e571e31611ed036a9fa3784042d300815d19

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: 699671b4ca7ed0c98066c4eae9cbda57d541e947fa20c8fbfc856f2cfdb05982

Explicit native q2-to-q1 projection obligation for SO_ZO_O01__deterministic__b2. The q2 identity/transfer remains pending; its literal bound is not merged into q1. Its stated dimension-accuracy term is guardedQ>=32 and logarithmic termQ>=128^2; these guards must never be widened by copying the combined formula. The currently proved q1 b3/b6 envelope already contains the same orders d min(d,sqrtQ) and dlogQ on Q>=32, so the displayed consequences establish no new stronger q1 order even if a legal transfer is later justified. This order comparison does not certify the missing quantity/resource identity or a fresh external theorem. Preserve the existing partial material lead rather than completing unrelated literature work.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 4c493c3f3de5ef1a210884c049e2791ccd5c30824eb5f42326f4279766f9b290

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/0; canonical SHA-256: fdc1dac28d2e0ef28ed244ed4c2e233ff3d4af99a6277447f93c9fb04dadd408

SO_ZO_O01__deterministic__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 9a313844aea540dba610c286c020cec97890c76d71cca0034ab1aa9bc89be1a0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids/0; canonical SHA-256: e9865214587940cf09761cc1ce224e9f092314a4af47482f75603ab03b3c6b1b

J1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids/1; canonical SHA-256: 4377b596e107dcc0b1035360b02736c84885f3ffb13058a0abbc7b2ffa67670d

J2

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 9719dbb16171489698f5e6ebb9124a7195ddb2bb9b9b59bffa6ca2a1c9180b8d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: 271c2f6eda9f3f49f260b8ab0966be25d2d839f93654c2e8b41a1978bee16de0

historical-q2-to-q1-deterministic

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 8dc16370729f02eb53b6b726a7ca66f94892caa16267c182ab63678f2fc79343

Other historical q2 identities still require explicit transfers; the q1 d logQ lower no longer depends on such a transfer.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 872112880ca08ba014986d9efa8d0d6c9fea415c373a5155aa40859c8f85090d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs/0; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs/1; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: 9c40a0f400f18b34bf13ace1fa22c7c3aaf9936fa81e87d535f0f51eded5647a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: fa290041e1aca639f8197eb00975394f48d591116d7c74f0b28878c48ea48f6b

Explicit native q2-to-q1 projection obligation for SO_ZO_O01__randomized__b2. The q2 identity/transfer remains pending; its literal bound is not merged into q1. Its stated dimension-accuracy term is guardedQ>=32 and logarithmic termQ>=128^2; these guards must never be widened by copying the combined formula. The currently proved q1 b3/b6 envelope already contains the same orders d min(d,sqrtQ) and dlogQ on Q>=32, so the displayed consequences establish no new stronger q1 order even if a legal transfer is later justified. This order comparison does not certify the missing quantity/resource identity or a fresh external theorem. Preserve the existing partial material lead rather than completing unrelated literature work.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: 2f4bce3d79ad9776b1a5e72a833fecf3fc11847a233e5be64044ec6123722654

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/0; canonical SHA-256: 394a4ded4bd867545123777d3e698294cee5b969ff71bee54d3920da63ad93fe

SO_ZO_O01__randomized__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 9a313844aea540dba610c286c020cec97890c76d71cca0034ab1aa9bc89be1a0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids/0; canonical SHA-256: e9865214587940cf09761cc1ce224e9f092314a4af47482f75603ab03b3c6b1b

J1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids/1; canonical SHA-256: 4377b596e107dcc0b1035360b02736c84885f3ffb13058a0abbc7b2ffa67670d

J2

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 56427d5a86b3fe111384ab442637c8daada6a2db604ff2e6381ab9181a990b66

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/1; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 50c653b87dbc5f272df0718a5d9d24ee65ce9a954c6f09f3d2eb2ebfdc59c384

historical-q2-to-q1-randomized

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 8dc16370729f02eb53b6b726a7ca66f94892caa16267c182ab63678f2fc79343

Other historical q2 identities still require explicit transfers; the q1 d logQ lower no longer depends on such a transfer.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 872112880ca08ba014986d9efa8d0d6c9fea415c373a5155aa40859c8f85090d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs/0; canonical SHA-256: 02d552170c59ae7589e4ae3af9204dd2a679ee69689372df99a84687fb96b8ae

ZO_PROOF_COMPARE_TRANSFER

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs/1; canonical SHA-256: ec48da0f578d5f8d6392345f168150827ad7a683056f89e112fa7c68675bd97b

ZO_PROOF_COMPARE_PACKING_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: 5ee094c693d1bc78c83ea18fdd9bc06782bf8e9360f4f80602e8bf6aefa403f7

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: d46169f5771e7d4d930aaf80b51dcfe1c65fb38e9621d9c3c06705312630c969

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: 5f0846f71310f35a3874c2f807403ad477396d14f115c602322da20c242a0231

SO_ZO_O01__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/1; canonical SHA-256: d880c64ab2dc696daf5cb98c6857443a6081136c4aa629325b7afdc42beff641

SO_ZO_O01__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/2; canonical SHA-256: a1cb37dc60f1fcd15b7e6d6200bb94871ac869aea8d5da8e5cb3ce0e51263f83

SO_ZO_O01__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/3; canonical SHA-256: 21b9f25caf9a4f0f8f6bae2a9c8b2a04b07402ccaf782985768231197b138ff2

SO_ZO_O01__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: 39db3a595dcbc9f7067df9b13e1c2baaeb45d73aeccd1bbaf635d557970911ed

curated-scope-limit-ab3e5d3796

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 764bb28ba2b520da22ee22752c2f5770602765846595335b2865fe8cd1b3913f

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 3069925cfc097fe701f6301b3138e378e9e9f9efda45882abaa6ab532faa7dae

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 8d65311f8a785198e53a1915bb5908b3c4abf1e26623fde6d8d4f09ed2c903fc

/views/1

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: 4b81cab280b1e31c2ea7afa9a416577b7c9c22795698d5d642e0394c36a90edd

/quantities/2

#### Native item 7

Native pointer: /joint_analysis/target/contract_refs/6; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: f18e8cf36d54f3ffe8b7925271411db950281fa054eec9e73faca423a8ca78bf

d in N,d>=1; beta>0,R>0,epsilon>0 (Q>0). Minimax fixed worst-case scalar comparison calls for native global objective-gap optimization, separately deterministic g1 and randomized g1 (success>=2/3).

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 61eeb5625c82ca9e8d18df672be107d928cf5d93588adbc9fb77fcdc3e99978e

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: a9b88fb6e9d64e0ee4ea5ec34523a7363ffa34d508a274b48e2fd74b57ba8a54

SO_ZO_O01_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 596aeda28917f4e6750cdfe9797b83a6448019c16ceeb6d570276492b90116bd

SO_ZO_O01_p_1c5476f952

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: dd785453e5a759626e5171f449beae940732ae89a2a292f9f5e2e40e0d331354

SO_ZO_O01_p_c5d2137706

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: c603c89c2938ceca986c0ad9f518331426e40d9fa3cb7a7f4ad0a1b9c7f5e810

SO_ZO_O01_p_5c322c6737

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4b1f6327738f1a0602d5ec159a23b41efdc6924636ada7f79f20583c854dd01a

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 90b2bfac6ebbe73553261fea0249228f5297988ae042de9f8a09e60ac26b8339

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: c84c339dc0367128acaebec4c0c8771cfaaf1a68c10a96205d78e685a00aebfe

Q=beta R^2/epsilon. Under x=R z and F(z)=f(R z)/(beta R^2), F is 1-smooth, a minimizer lies in B_1 and target gap is 1/Q. Positive scaling preserves comparisons, ties and the scalar-call budget; constants remain uniform in the four native variables.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: 1744242bfb841e3e08438411b0e4e85cf32e3a48a4d580007a416e3805e50a33

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 596aeda28917f4e6750cdfe9797b83a6448019c16ceeb6d570276492b90116bd

SO_ZO_O01_p_1c5476f952

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: dd785453e5a759626e5171f449beae940732ae89a2a292f9f5e2e40e0d331354

SO_ZO_O01_p_c5d2137706

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/2; canonical SHA-256: c603c89c2938ceca986c0ad9f518331426e40d9fa3cb7a7f4ad0a1b9c7f5e810

SO_ZO_O01_p_5c322c6737

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: da53dc5001ef1e872bd575bd38d9fafe75b9a13e995acdefe8bbd13f40e12829

Q

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 61eeb5625c82ca9e8d18df672be107d928cf5d93588adbc9fb77fcdc3e99978e

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: a9b88fb6e9d64e0ee4ea5ec34523a7363ffa34d508a274b48e2fd74b57ba8a54

SO_ZO_O01_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 596aeda28917f4e6750cdfe9797b83a6448019c16ceeb6d570276492b90116bd

SO_ZO_O01_p_1c5476f952

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: dd785453e5a759626e5171f449beae940732ae89a2a292f9f5e2e40e0d331354

SO_ZO_O01_p_c5d2137706

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: c603c89c2938ceca986c0ad9f518331426e40d9fa3cb7a7f4ad0a1b9c7f5e810

SO_ZO_O01_p_5c322c6737

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] Zhang and Li. Comparisons Are All You Need for Optimizing Smooth Functions. arXiv:2405.11454v1, 2024; the specified early version.

https://arxiv.org/html/2405.11454v1

[3] Xia and Yuan. On Global Joint Lower Bounds in Zeroth-Order Nonconvex Optimization. arXiv:2610.19652v1, 2026-10-14.

https://arxiv.org/html/2610.19652v1

[4] Sebastien Bubeck. Convex Optimization: Algorithms and Complexity. arXiv:1405.4980v2, 2015-11-16.

https://arxiv.org/pdf/1405.4980v2

[5] Peter Richtárik; Ammar Mahran. Near-Optimal Smooth Convex Optimization with a Comparison Oracle. 2026. arXiv:2611.29533v1, 2026-11-22.

https://arxiv.org/html/2611.29533v1

[6] Colombo_KIMI_002. Deterministic Full-History Acceleration with Exact Comparison Feedback. Uploaded manuscript, Kimi K3.1 Pro, 2026-11-24.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_002/kimi_002.pdf
