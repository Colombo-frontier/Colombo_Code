# Smooth PL optimization with exact full-objective values

**Setting ID.** `SO_ZO_E08`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; growth: Polyak lojasiewicz; smoothness: Lipschitz gradient; structure: No additional structure

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

$f_*:=\inf_{x\in\mathbb{R}^d}f(x)>-\infty$, and the given initial point $x_0$ satisfies $f(x_0)-f_*\le\Delta$.

The population objective satisfies the Polyak–Łojasiewicz condition $\|\nabla f(x)\|_2^2\ge2\mu(f(x)-f_*)$ for every $x\in\mathbb{R}^d$; convexity is not required.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

The public inputs are $d$, $\beta$, $\mu$, $\Delta$, $x_0$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

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

$\mu$: PL constant **Domain:** $\mu>0$.

$\|\nabla f(x)\|_2^2\ge2\mu(f(x)-f_*)$

$\Delta$: Known upper bound on the initial objective gap **Domain:** $\Delta\ge0$.

$f(x_0)-\inf_{x\in\mathbb{R}^d}f(x)\le\Delta$

$x_0$: Known initial point **Domain:** $x_0\in\mathbb{R}^d$.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$\kappa$: Ratio of the known smoothness and strong-convexity bounds **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu$

$c_\varepsilon$: Relative-accuracy constant in the finite-sum hard construction **Domain:** $c_\varepsilon>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$C_{\mathrm{dim}}$: Dimension constant in the finite-sum hard construction **Domain:** $C_{\mathrm{dim}}>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$Q_\Delta$: Normalized ratio of the initial objective gap to the target accuracy **Domain:** $Q_\Delta\ge0$.

$Q_\Delta=2\Delta/\varepsilon$

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

### R1 - Parameter regime E08.R1

**Region.** $\kappa\ge3,\ 0<\varepsilon\le\min\{c_\varepsilon\Delta,\Delta/16\},\ d\ge C_{\rm dim}(1+\kappa\log(\Delta/\varepsilon))\log(2+\kappa\log(\Delta/\varepsilon))$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Other quantified gap

**Lower bound.** B3, B4, B5

$$
\begin{cases}\Omega(\max\{\kappa\log(\Delta/\varepsilon),d\min(d,\sqrt\kappa,\sqrt{Q_\Delta})\}),&Q_\Delta<128^2,\\\Omega(\max\{\kappa\log(\Delta/\varepsilon),d\min(d,\sqrt\kappa,\sqrt{Q_\Delta}),d\log Q_\Delta\}),&Q_\Delta\ge128^2.\end{cases}
$$

**Upper bound.** B1

$$
O(d\kappa\log(\Delta/\varepsilon))
$$

**Gap or comparison.** $O\!\left(\frac{d\kappa\log(\Delta/\varepsilon)}{\max\{\kappa\log(\Delta/\varepsilon),\,d\min(d,\sqrt\kappa,\sqrt{Q_\Delta}),\,d\log Q_\Delta\ {\rm if}\ Q_\Delta\ge128^2\}}\right)$

### R2 - Parameter regime E08.NEW.zero_region

**Region.** $\varepsilon\ge\Delta$.

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

### R3 - Parameter regime E08.NEW.kappa1_small_accuracy

**Region.** $\kappa=1,\ 0<\varepsilon\le\Delta/16$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B3, B11

$$
\Omega(d\min\{d,\sqrt\kappa,\sqrt{Q_\Delta}\})
$$

**Upper bound.** B8, B16

$$
d+1
$$

**Gap or comparison.** $O(1)$

### R4 - Parameter regime E08.R1

**Region.** $\kappa\ge3,\ 0<\varepsilon\le\min\{c_\varepsilon\Delta,\Delta/16\},\ d\ge C_{\rm dim}(1+\kappa\log(\Delta/\varepsilon))\log(2+\kappa\log(\Delta/\varepsilon))$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Other quantified gap

**Lower bound.** B11, B12, B13

$$
\begin{cases}\Omega(\max\{\kappa\log(\Delta/\varepsilon),d\min(d,\sqrt\kappa,\sqrt{Q_\Delta})\}),&Q_\Delta<128^2,\\\Omega(\max\{\kappa\log(\Delta/\varepsilon),d\min(d,\sqrt\kappa,\sqrt{Q_\Delta}),d\log Q_\Delta\}),&Q_\Delta\ge128^2.\end{cases}
$$

**Upper bound.** B9

$$
O(d\kappa\log(\Delta/\varepsilon))
$$

**Gap or comparison.** $O\!\left(\frac{d\kappa\log(\Delta/\varepsilon)}{\max\{\kappa\log(\Delta/\varepsilon),\,d\min(d,\sqrt\kappa,\sqrt{Q_\Delta}),\,d\log Q_\Delta\ {\rm if}\ Q_\Delta\ge128^2\}}\right)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Finite-difference gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
(d+1)\lceil\kappa\log(2\Delta/\varepsilon)\rceil
$$

**Sources.** [3](https://proceedings.mlr.press/v195/yue23a/yue23a.pdf)

**Conditions.** Take $h^2\le4\mu\varepsilon/(d\beta ^2)$. When $\kappa=1$, one step suffices; the simplified logarithmic expression is not used to classify optimality at this endpoint.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [3](https://proceedings.mlr.press/v195/yue23a/yue23a.pdf) theorem: Finite-difference PL descent argument

### B2 - Strongly convex subclass or hidden finite-sum hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\kappa\log(\Delta/\varepsilon))
$$

**Sources.** [2](https://arxiv.org/html/2609.00045v3) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\kappa\ge3$ and $\varepsilon\le c\Delta$, in sufficiently large dimension. A full objective-value query to the hard finite sum can be simulated through component-value and gradient access, charging all required component calls.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

**Source location.** [2](https://arxiv.org/html/2609.00045v3) theorem: Theorem 3.3, with full-value simulation at fixed $n=1024$

**Source location.** [2](https://arxiv.org/html/2609.00045v3) theorem: Theorem 3.3, with full-value simulation at fixed $n=1024$; pdf pages: 5; printed pages: 5

### B3 - Strongly convex subclass or hidden finite-sum hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt\kappa,\sqrt{Q_\Delta}\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2609.00045v3)

**Conditions.** $1\le\kappa,\ Q_\Delta=2\Delta/\varepsilon\ge32$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A2

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary2.4; pdf pages: 4; printed pages: 4

### B4 - Strongly convex subclass or hidden finite-sum hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log Q_\Delta)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2609.00045v3)

**Conditions.** $\kappa\ge2,\ Q_\Delta\ge128^2$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A2

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem2.5; pdf pages: 4; printed pages: 4

### B5 - Strongly convex subclass or hidden finite-sum hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\kappa\log(\Delta/\varepsilon))
$$

**Sources.** [2](https://arxiv.org/html/2609.00045v3) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\kappa\ge3,\ 0<\varepsilon\le c_\varepsilon\Delta,\ d\ge C_{\rm dim}(1+\kappa\log(\Delta/\varepsilon))\log(2+\kappa\log(\Delta/\varepsilon))$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

**Source location.** [2](https://arxiv.org/html/2609.00045v3) theorem: Theorem3.3; pdf pages: 5; printed pages: 5

**Source location.** [2](https://arxiv.org/html/2609.00045v3) theorem: Equations283–284; pdf pages: 47; printed pages: 47

**Source location.** [2](https://arxiv.org/html/2609.00045v3) theorem: IFO definition Eq313; pdf pages: 52; printed pages: 52

### B6 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge\Delta$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

### B7 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge\Delta$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

### B8 - Finite-difference gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
d+1
$$

**Conditions.** $\kappa=1,\varepsilon>0$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

### B9 - Finite-difference gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
(d+1)\lceil\kappa\log(2\Delta/\varepsilon)\rceil
$$

**Sources.** [3](https://proceedings.mlr.press/v195/yue23a/yue23a.pdf)

**Conditions.** Take $h^2\le4\mu\varepsilon/(d\beta ^2)$. When $\kappa=1$, one step suffices; the simplified logarithmic expression is not used to classify optimality at this endpoint.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [3](https://proceedings.mlr.press/v195/yue23a/yue23a.pdf) theorem: Finite-difference PL descent argument

### B10 - Strongly convex subclass or hidden finite-sum hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\kappa\log(\Delta/\varepsilon))
$$

**Sources.** [2](https://arxiv.org/html/2609.00045v3) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\kappa\ge3$ and $\varepsilon\le c\Delta$, in sufficiently large dimension. A full objective-value query to the hard finite sum can be simulated through component-value and gradient access, charging all required component calls.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

**Source location.** [2](https://arxiv.org/html/2609.00045v3) theorem: Theorem 3.3, with full-value simulation at fixed $n=1024$

**Source location.** [2](https://arxiv.org/html/2609.00045v3) theorem: Theorem 3.3, with full-value simulation at fixed $n=1024$; pdf pages: 5; printed pages: 5

### B11 - Strongly convex subclass or hidden finite-sum hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt\kappa,\sqrt{Q_\Delta}\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2609.00045v3)

**Conditions.** $1\le\kappa,\ Q_\Delta=2\Delta/\varepsilon\ge32$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A2

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary2.4; pdf pages: 4; printed pages: 4

### B12 - Strongly convex subclass or hidden finite-sum hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\log Q_\Delta)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2609.00045v3)

**Conditions.** $\kappa\ge2,\ Q_\Delta\ge128^2$

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A2

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem2.5; pdf pages: 4; printed pages: 4

### B13 - Strongly convex subclass or hidden finite-sum hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\kappa\log(\Delta/\varepsilon))
$$

**Sources.** [2](https://arxiv.org/html/2609.00045v3) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\kappa\ge3,\ 0<\varepsilon\le c_\varepsilon\Delta,\ d\ge C_{\rm dim}(1+\kappa\log(\Delta/\varepsilon))\log(2+\kappa\log(\Delta/\varepsilon))$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

**Source location.** [2](https://arxiv.org/html/2609.00045v3) theorem: Theorem3.3; pdf pages: 5; printed pages: 5

**Source location.** [2](https://arxiv.org/html/2609.00045v3) theorem: Equations283–284; pdf pages: 47; printed pages: 47

**Source location.** [2](https://arxiv.org/html/2609.00045v3) theorem: IFO definition Eq313; pdf pages: 52; printed pages: 52

### B14 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge\Delta$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

### B15 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge\Delta$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

### B16 - Finite-difference gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
d+1
$$

**Conditions.** $\kappa=1,\varepsilon>0$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

## 5. Local arguments

### A1 - Finite-difference descent for a smooth PL objective

**Scope.** Global $\beta$-smoothness and the $\mu$-PL inequality, initial gap at most $\Delta$, exact all-space values; convexity is unnecessary.

For $\kappa=\beta/\mu\ge1$, a valid bound is $(d+1)\lceil\kappa\log(2\Delta/\varepsilon)\rceil$ on the nontrivial accuracy range. At $\kappa=1$, $d+1$ calls suffice for every positive target.

Forward differences at a finite positive scale $h$ have error $e$ with $\|e\|^2\le d\beta^2h^2/4$. Smoothness of a step $x^+=x-(\nabla f(x)+e)/\beta$ gives
$$f(x^+)-f_*\le(1-\mu/\beta)[f(x)-f_*]+\|e\|^2/(2\beta).$$
Choose $h^2\le4\mu\varepsilon/(d\beta^2)$. The accumulated error floor is at most $\varepsilon/2$, and the displayed number of iterations makes the initial term at most $\varepsilon/2$. Each step uses $d+1$ exact values. At $\mu=\beta$, the initial term vanishes after one step and the gap is at most $\|e\|^2/(2\beta)$; choose $h^2\le8\varepsilon/(\beta d)$. Return the initial point for $\varepsilon\ge\Delta$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A2 - Strongly convex and finite-sum lower subclasses of the PL model

**Scope.** The PL model has public $\beta,\mu,\Delta,x_0$ and no additional public localization radius. Every source dimension and accuracy restriction is retained.

With the proof-only radius $R_\Delta=\sqrt{2\Delta/\beta}$ and $Q_\Delta=2\Delta/\varepsilon$, the smooth strongly convex source lower gives $\Omega(d\min\{d,\sqrt\kappa,\sqrt{Q_\Delta}\})$. A separate high-dimensional finite-sum reduction gives $\Omega(\kappa\log(\Delta/\varepsilon))$.

A globally $\mu$-strongly-convex, $\beta$-smooth function with minimizer in $B(x_0,R_\Delta)$ satisfies $f(x_0)-f_*\le\Delta$. Minimizing its strong-convexity lower model over all points gives $\|\nabla f(x)\|^2\ge2\mu[f(x)-f_*]$. It therefore belongs to the target PL class without supplying the algorithm any additional public parameter. Apply Dorn et al., Corollary 2.4, for $Q_\Delta\ge32$. For $\kappa\ge2$, the $\beta/2$-strongly-convex subclass and Theorem 2.5 give $\Omega(d\log Q_\Delta)$ when $Q_\Delta\ge128^2$.

For the separate finite-sum lower, fix the source component count at $n=1024$. Exactly 1024 incremental value-and-gradient calls simulate one average value, discarding gradients. The individual-smoothness branch of Dense26 Theorem 3.3, divided by this fixed cost, is $\Omega(\kappa\ell)$ for $\kappa\ge3$, $\ell=\log(\Delta/\varepsilon)$. On $3\le\kappa\le32$, the source denominator $1+\log(32/\kappa)$ is uniformly bounded; on $\kappa\ge32$, its linear-$\kappa$ branch gives the same rate. Source equations (283)–(284) give the sufficient dimension
$$d\ge C_{\rm dim}(1+\kappa\ell)\log(2+\kappa\ell),\qquad\varepsilon\le c_\varepsilon\Delta.$$
The constants remain symbolic. Inactive-coordinate padding preserves PL, smoothness, gap, and the oracle simulation for every larger dimension. The source permits unqueried outputs and has failure lower $11/16$, sufficient to rule out success $2/3$. This is a lower bound from a stronger oracle; it does not multiply unrelated dimension and condition-number lower bounds.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2609.00045v3)

### A3 - Zero-query certificates

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

[2] Peng, Tang and Jia. Dense Weak Hiding: Closing Complexity Gaps in Nonconvex and PL Finite-Sum Optimization under Individual Smoothness. arXiv:2609.00045v3, 2026-10-10.

https://arxiv.org/html/2609.00045v3

[3] Yue, Fang and Lin. On the Lower Bound of Minimizing Polyak-Lojasiewicz Functions. COLT 2023, PMLR 195:2948--2968.

https://proceedings.mlr.press/v195/yue23a/yue23a.pdf
