# Lipschitz strongly convex optimization with exact values

**Setting ID.** `SO_ZO_E02`

Single-objective optimization

Minimize $f$ globally over $B_2(0,R)$ and return a point with small objective gap.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; smoothness: Lipschitz function; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $B_2(0,R)$ and return a point with small objective gap.

### Admissible model

$f:B_2(0,R)\to\mathbb{R}$ is convex and satisfies $|f(x)-f(y)|\le L\|x-y\|_2$ for every $x,y$ in the ball. Neither a definition nor regularity outside the ball is assumed. Continuity on the ball guarantees attainment of the constrained minimum.

Strong convexity is defined in the Euclidean norm: $f((1-t)x+ty)\le(1-t)f(x)+tf(y)-\frac{\mu}{2}t(1-t)\|x-y\|_2^2$ for $x,y$ and $t\in[0,1]$ in the domain.

Fix $0<\theta_0<1$, with budget $0<\mu R\le\theta_0L$. Strong convexity is required only within this ball.

### Oracle interface

At any finite query point $x$ in $B_2(0,R)$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

Projection and the stated proximal operations over known geometry are free.

The public inputs are $d$, $L$, $\mu$, $R$, $\varepsilon$, $\theta_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

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

$\mu$: Public lower bound on the strong-convexity modulus **Domain:** $\mu>0$.

$R$: Feasible-ball radius **Domain:** $R>0$.

The output must belong to $B_2(0,R)$; the query radius is specified separately in the interface.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$A$: Lipschitz accuracy ratio **Domain:** $A>0$.

$A=LR/\varepsilon$

$\theta$: Compatibility ratio of the strong-convexity and Lipschitz budgets **Domain:** $0<\theta\le1$.

$\theta=\mu R/L$

$\Xi$: Saturation scale involving dimension, Lipschitz accuracy, and strongly convex accuracy **Domain:** $\Xi>0$.

$\Xi=\min\{d,A^2,L^2/(\mu\varepsilon)\}$

$\theta_0$: Upper bound on budget-compatibility slack, fixed in advance **Domain:** $0<\theta_0<1$.

$\mu R/L\le\theta_0$

$d_0$: Universal dimension threshold required by the lower bound **Domain:** $d_0>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$c_{\theta_0}$: Accuracy-threshold constant depending only on the fixed compatibility slack **Domain:** $c_{\theta_0}>0$.

The numerical value is determined by the lower-bound theorem and cannot be replaced by an arbitrary unit threshold.

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

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime E02.R1

**Region.** $d\ge d_0,\ 0<\theta=\mu R/L\le\theta_0<1,\ 0<\varepsilon\le\min\{LR/8,c_{\theta_0}\min(LR,L^2/\mu)\},\ \Xi<d$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B3

$$
\Omega_{\theta_0}(d\Xi/\log(e\Xi))
$$

**Upper bound.** B1, B2

$$
O(d\Xi\log(edA))
$$

**Gap or comparison.** $O_{\theta_0}(\log(edA)\log(e\Xi))$

### R2 - Parameter regime E02.R2

**Region.** $d\ge d_0,\ 0<\theta=\mu R/L\le\theta_0<1,\ 0<\varepsilon\le\min\{LR/8,c_{\theta_0}\min(LR,L^2/\mu)\},\ \Xi=d$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B3

$$
\Omega_{\theta_0}(d^2/\log(ed))
$$

**Upper bound.** B1, B2

$$
O(\min\{dA^2\log(edA),dL^2\log(edA)/(\mu\varepsilon),d^2\log(ed)\log(4A)\})
$$

**Gap or comparison.** $O_{\theta_0}(\log^2(ed)\log(4A))$

### R3 - Parameter regime E02.NEW.zero_region

**Region.** $0<\mu R\le L,\ \varepsilon\ge\min\{LR,(L-\mu R)^2/(2\mu)\}$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B5, B11

$$
0
$$

**Upper bound.** B4, B10

$$
0
$$

### R4 - Parameter regime E02.R1

**Region.** $d\ge d_0,\ 0<\theta=\mu R/L\le\theta_0<1,\ 0<\varepsilon\le\min\{LR/8,c_{\theta_0}\min(LR,L^2/\mu)\},\ \Xi<d$.

**Views.** Randomized

**Quantity.** Q2

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B9

$$
\Omega_{\theta_0}(d\Xi/\log(e\Xi))
$$

**Upper bound.** B6, B7, B8

$$
O(d\Xi)
$$

**Gap or comparison.** $O_{\theta_0}(\log(e\Xi))$

### R5 - Parameter regime E02.R2

**Region.** $d\ge d_0,\ 0<\theta=\mu R/L\le\theta_0<1,\ 0<\varepsilon\le\min\{LR/8,c_{\theta_0}\min(LR,L^2/\mu)\},\ \Xi=d$.

**Views.** Randomized

**Quantity.** Q2

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B9

$$
\Omega_{\theta_0}(d^2/\log(ed))
$$

**Upper bound.** B6, B7, B8

$$
O(\min\{dA^2,dL^2/(\mu\varepsilon),d^2\log(ed)\log(4A)\})
$$

**Gap or comparison.** $O_{\theta_0}(\log^2(ed)\log(4A))$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
\mathrm{Det}:\quad O(d^2\log(d+1)\log(4A))
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Localization algorithm for the original convex class.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Z26 Proposition 4

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Z26 Proposition 4; pdf pages: 12; printed pages: 12

**Source location.** [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) theorem: Z26 Proposition 4

### B2 - Deterministic subgradient extraction with strongly convex restarts

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C\min\{dA^2\log(edA),dL^2\log(edA)/(\mu\varepsilon),d^2\log(ed)\log(4A)\}
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $0<\varepsilon\le LR/8$ and $\mu R\le L$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

**Source location.** [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) theorem: Convex value-localization theorem, as normalized in the cited Proposition 4

### B3 - Random support-function hard family with a strongly convex perturbation

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_{\theta_0}(d\Xi/\log(e\Xi))
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $d\ge d_0,\varepsilon\le c_{\theta_0}\min\{LR,L^2/\mu\}$.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary K.14; Theorem K.2 provides explicit slack

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary K.14; Theorem K.2 provides explicit slack

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary K.14; Theorem K.2 provides explicit slack; pdf pages: 64; printed pages: 64

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary K.14; Theorem K.2 provides explicit slack; pdf pages: 71; printed pages: 71

### B4 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $0<\mu R\le L,\ \varepsilon\ge\min\{LR,(L-\mu R)^2/(2\mu)\}$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2, A3

### B5 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $0<\mu R\le L,\ \varepsilon\ge\min\{LR,(L-\mu R)^2/(2\mu)\}$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2, A3

### B6 - Two-point smoothing with strongly convex restarts, or convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
\mathrm{Rand}:\quad O\!\left(\min\{dA^2,dL^2/(\mu\varepsilon),d^2\log(d+1)\log(4A)\}\right)
$$

**Sources.** [5](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [4](https://arxiv.org/pdf/1006.2425) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2)

**Conditions.** The objective is convex and $L$-Lipschitz on the ball, and $\mu$-strongly convex in the Euclidean norm. The two-point estimator has second moment $O(dL^2)$. Staged strongly convex restarts give the middle branch; the other branches use convex optimization and localization, respectively.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A5, A6

**Source location.** [5](https://jmlr.org/papers/volume18/16-632/16-632.pdf) theorem: Symmetric ball smoothing combined with epoch SGD; a localization bound

**Source location.** [4](https://arxiv.org/pdf/1006.2425) theorem: Symmetric ball smoothing combined with epoch SGD; a localization bound

**Source location.** [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) theorem: Symmetric ball smoothing combined with epoch SGD; a localization bound

### B7 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
\mathrm{Det}:\quad O(d^2\log(d+1)\log(4A))
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Localization algorithm for the original convex class.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Z26 Proposition 4

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Z26 Proposition 4; pdf pages: 12; printed pages: 12

**Source location.** [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) theorem: Z26 Proposition 4

### B8 - Deterministic subgradient extraction with strongly convex restarts

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C\min\{dA^2\log(edA),dL^2\log(edA)/(\mu\varepsilon),d^2\log(ed)\log(4A)\}
$$

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $0<\varepsilon\le LR/8$ and $\mu R\le L$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

**Source location.** [3](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

**Source location.** [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) theorem: Convex value-localization theorem, as normalized in the cited Proposition 4

### B9 - Random support-function hard family with a strongly convex perturbation

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_{\theta_0}(d\Xi/\log(e\Xi))
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $d\ge d_0,\varepsilon\le c_{\theta_0}\min\{LR,L^2/\mu\}$.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary K.14; Theorem K.2 provides explicit slack

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary K.14; Theorem K.2 provides explicit slack

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary K.14; Theorem K.2 provides explicit slack; pdf pages: 64; printed pages: 64

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary K.14; Theorem K.2 provides explicit slack; pdf pages: 71; printed pages: 71

### B10 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $0<\mu R\le L,\ \varepsilon\ge\min\{LR,(L-\mu R)^2/(2\mu)\}$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2, A3

### B11 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $0<\mu R\le L,\ \varepsilon\ge\min\{LR,(L-\mu R)^2/(2\mu)\}$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2, A3

## 5. Local arguments

### A1 - Deterministic extraction of an approximate subgradient

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

**Sources.** [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

### A2 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A3 - The center certificate for a strongly convex Lipschitz function

**Scope.** A convex function on $B_2(R)$, $\mu$-strongly convex and $L$-Lipschitz; interior subgradients are taken without an artificial boundary normal cone.

The class is nonempty only if $\mu R\le L$, and
$$f(0)-\min_{B_2(R)} f\le\min\{LR,(L-\mu R)^2/(2\mu)\}.$$
In particular, the center is optimal when $\mu R=L$.

Let $g_0\in\partial f(0)$. If $g_0\ne0$, put $u=g_0/\|g_0\|$ and choose $g_t\in\partial f(tu)$ for $0<t<R$. Strong monotonicity gives $\langle g_t,u\rangle\ge\|g_0\|+\mu t$. Interior subgradients have norm at most $L$, hence $\|g_0\|\le L-\mu R$ by letting $t\uparrow R$. If $g_0=0$, the same inequality along any direction gives the feasibility condition $\mu R\le L$.

Strong convexity implies $f(z)\ge f(0)+\langle g_0,z\rangle+\mu\|z\|^2/2\ge f(0)-\|g_0\|^2/(2\mu)$. Combine this with the independent Lipschitz center bound $LR$. The argument uses only the mean function, so it also applies when a finite-sum mean is strongly convex only on the feasible ball.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A4 - Ball smoothing and the same-sample directional moment

**Scope.** A fresh sample each round; the same sample supplies both values; sample Lipschitz modulus $G$ on the stated query neighborhood; $\mathbb E G^r\le L^r$, $1<r\le2$.

With ball smoothing $f_h(x)=\mathbb E_{U\sim\operatorname{Unif}(B_2)}f(x+hU)$ and a sphere direction $u$,
$$g_h(x)=\frac d{2h}[F(x+hu;Z)-F(x-hu;Z)]u,\quad\mathbb E g_h=\nabla f_h,\quad\mathbb E\|g_h\|^r\le(\sqrt{2d}L)^r.$$
For $r=2$, the bound is $2dL^2$.

For each fixed sample, the scalar difference $a(u)=F(x+hu;Z)-F(x-hu;Z)$ is odd on the sphere, hence has mean zero, and has Lipschitz constant at most $2hG$. Sphere Poincare gives $\mathbb E_u a(u)^2\le4h^2G^2/(d-1)$ for $d\ge2$. Thus $\mathbb E_u\|g_h\|^2\le d^2G^2/(d-1)\le2dG^2$; for $d=1$ the difference quotient is directly bounded by $G$. Apply Jensen only to the direction expectation and then integrate over the sample:
$$\mathbb E_{Z,u}\|g_h\|^r\le\mathbb E_Z(\mathbb E_u\|g_h\|^2)^{r/2}\le(2d)^{r/2}\mathbb E G^r.$$
No second moment of $G$ is needed when $r<2$. The divergence theorem for ball convolution gives the unbiasedness identity. Integrability follows from the Lipschitz difference bound. Convexity gives $f_h\ge f$, and $|f_h-f|\le hL$; mean strong convexity is preserved on the region where every translated point satisfies it. All statements hold conditionally on the past when the next sample and direction are fresh. Reusing an old adaptively explored sample does not automatically preserve this conditional moment calculation.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [5](https://jmlr.org/papers/volume18/16-632/16-632.pdf)

### A5 - Projected optimization with same-sample two-point values

**Scope.** Optimization/output in $B_2(R)$; all two-point queries remain in the prescribed ball; mean strong convexity suffices. A uniformly sampled finite-sum component is also a valid fresh sample.

For a $\mu$-strongly-convex mean with $\mathbb E G^2\le L^2$, $K$ rounds and $T=2K$ scalar calls give
$$\mathbb E[f(\bar x_K)-f_*]\le\frac{4dL^2}{\mu(K+1)}+2hL.$$
The merely convex branch uses $O(d(LR/\varepsilon)^2)$ values.

Run the paired estimator on $K_h=B_2(R-h)$ and let $x_{h,*}$ minimize $f_h$ there. The shrinkage comparator $y=(1-h/R)x_*$ gives $f_h(y)\le f_*+2hL$. Set $V=2dL^2$, $\eta_t=2/[\mu(t+1)]$, and $D_t=\mathbb E\|x_t-x_{h,*}\|^2$. Projection and strong convexity yield
$$\mathbb E[f_h(x_t)-f_h(x_{h,*})]\le\frac{\mu(t-1)}4D_t-\frac{\mu(t+1)}4D_{t+1}+\frac{V}{\mu(t+1)}.$$
Multiply by $t$, telescope, and average with weights $2t/[K(K+1)]$. The initial distance coefficient is zero and the last is nonpositive, giving $2V/[\mu(K+1)]$. Add the comparator error. For expected accuracy choose, for example, $h=\varepsilon/(8L)$ and $K+1\ge8dL^2/(\mu\varepsilon)$. For success probability $2/3$, use $h=\varepsilon/(12L)$ and $K+1\ge24dL^2/(\mu\varepsilon)$, making the expected nonnegative gap at most $\varepsilon/3$ before Markov.

For convex objectives, the projected averaging recursion with step $R/\sqrt{VK}$ gives expected optimization error at most $R\sqrt{V/K}$, plus the same smoothing/shrinkage error. Uniform component sampling makes the estimator unbiased for the finite-sum mean and costs exactly two selected-component values per round. Neither the oracle nor the components need be stochastic in that case; the algorithm supplies the randomness. These bounds also hold under an almost-sure Lipschitz promise, since it implies the required second moment. The Gaussian lower construction in the separate lower lemma does not acquire that stronger promise.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A6 - Norm conversion, penalized localization, and affine equivalence

**Scope.** Globally defined objectives, the declared regularity norm, a public feasible or localization body, and the stated free geometric operations.

Let $a_B=\max_{\|u\|_2=1}\|u\|_B$ and let $R_2(K)$ be a public Euclidean enclosing radius. Then $\beta_2=a_B^2\beta$, $L_2=a_BL$, and $D_2=a_BR_2(K)$ give the deterministic smooth envelope
$$O\!\left(1+\min\{d\sqrt{\beta D_2^2/\varepsilon},d^2\log(e+\beta D_2^2/\varepsilon)\}\right)$$
and Lipschitz localization $O(1+d^2\log(d+1)\log(e+LD_2/\varepsilon))$.

The norm inequality $\|v\|_B\le a_B\|v\|_2$ and its dual give the stated Euclidean smoothness and Lipschitz constants. Apply the exact-value Euclidean acceleration or smooth localization theorem with those constants and the public radius; each transformed value remains one scalar call. The global-minimizer promise is retained for the smooth localization argument.

For a Lipschitz objective minimized over a known convex set $K$, define $g(x)=f(x)+L_2\operatorname{dist}_2(x,K)$. This is convex and $2L_2$-Lipschitz, $\min g=\min_K f$ on a ball containing $K$, and $f(\Pi_Kx)\le g(x)$. One value of $g$ uses one value of $f$ plus public geometry. The Euclidean ball localization theorem therefore returns a legal point of $K$ after projection. This is a concrete transfer to a general body, not a presumed general-body localization theorem.

If $B=UB_2(1)$ and $K=c+RB$ for a public invertible matrix $U$, set $g(y)=f(c+Uy)$. Then $\|Uv\|_B=\|v\|_2$ and $\|U^\top w\|_2=\|w\|_{B,*}$. Thus both the Lipschitz and smoothness budgets are unchanged, the feasible or localization body becomes $B_2(R)$, and one value plus the inverse output map preserves the exact gap, budget, and guarantee. No condition-number factor appears. Deterministic acceleration/localization and randomized two-point methods keep their original algorithm permissions.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [2](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] V. Yu. Protasov. Algorithms for approximate calculation of the minimum of a convex function from its values. Mathematical Notes 59(1):69--74, 1996.

https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper

[3] Haihan Zhang, Chenheng Zhang, Zhiquan Qi and Zhouchen Lin. Near-Optimal Lower Bounds for Randomized Algorithms in Exact Value Zeroth-Order Convex Optimization. arXiv:2607.16558v2, 2026-07-30.

https://arxiv.org/html/2607.16558v2

[4] Hazan and Kale. Beyond the regret minimization barrier: an optimal algorithm for stochastic strongly-convex optimization. COLT 2011, PMLR 19:421-436; proof checked against arXiv:1006.2425v1 (2010, shorter-title version).

https://arxiv.org/pdf/1006.2425

[5] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. JMLR 18(52):1--11, 2017.

https://jmlr.org/papers/volume18/16-632/16-632.pdf
