# Lipschitz strongly convex optimization with exact values

**Setting ID.** `SO_ZO_E02`

Single-objective optimization

Minimize $f$ globally over $B_2(0,R)$ and return a point with small objective gap.

**Status.** Logarithmic gap; Other quantified gap; Bounds missing

**Gap classes present.** Logarithmic gap; Other quantified gap

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; smoothness: Lipschitz function; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

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

#### Randomized / Expected loss / Full slack range

Queries, stopping decisions, and the output are measurable functions of the preceding transcript and an instance-independent private random seed. The unknown instance is fixed before the seed is realized. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage using public inputs and received information are uncharged. The stated budget must hold on every execution path.

$$
\forall f:\ \mathbb E[f(\widehat x)-\min_{B_2(0,R)}f]\le\varepsilon
$$

Expectation is only over the independent private seed after the objective is fixed. Every execution has the same worst-case scalar-query cap.

Model: The hidden objective $f:B_2(0,R)\to\mathbb R$ is continuous, $f(x)-\mu\|x\|_2^2/2$ is convex, and $|f(x)-f(y)|\le L\|x-y\|_2$ for every pair in the ball. Here $L$ bounds the whole objective, not only a residual. Differentiability and an interior minimizer are not assumed.

Model: The admissible nonempty parameter range is $L\ge\mu R>0$, with no fixed separation from equality. No definition or regularity outside the ball is assumed. The gap from the feasibility boundary is $\Delta=L-\mu R\ge0$.

Model: For $\Delta=0$, every objective is $f(x)=f(0)+\mu\|x\|_2^2/2$. For $\Delta>0$, define $$S_\Delta=\max_{0\le r\le R}\{\Delta r-\mu r^2/2\}=\begin{cases}\Delta^2/(2\mu),&0\le\Delta\le\mu R,\\ \Delta R-\mu R^2/2,&\Delta>\mu R.\end{cases}$$

Oracle: At a feasible point $x\in B_2(0,R)$, the oracle returns only the exact scalar $f(x)$. The unknown function is fixed before an independent private seed is drawn. No values outside the ball, derivatives, or hidden minimizers are supplied.

Oracle: The public inputs are $d,L,\mu,R,\varepsilon$ and the ball. All scalar values, including the two values of a paired estimate, are charged. Projection and operations on the known ball are free.

**Budget convention.** fixed_worst_case

#### Randomized / 1/2 success / Full slack range

Queries, stopping decisions, and the output are measurable functions of the preceding transcript and an instance-independent private random seed. The unknown instance is fixed before the seed is realized. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage using public inputs and received information are uncharged. The stated budget must hold on every execution path.

$$
\forall f:\ \Pr(f(\widehat x)-\min_{B_2(0,R)}f>\varepsilon)\le1/2
$$

The fixed success level is exactly the manuscript convention, at least one half on each instance. The call budget is pathwise, and only the private seed is randomized.

Model: The hidden objective $f:B_2(0,R)\to\mathbb R$ is continuous, $f(x)-\mu\|x\|_2^2/2$ is convex, and $|f(x)-f(y)|\le L\|x-y\|_2$ for every pair in the ball. Here $L$ bounds the whole objective, not only a residual. Differentiability and an interior minimizer are not assumed.

Model: The admissible nonempty parameter range is $L\ge\mu R>0$, with no fixed separation from equality. No definition or regularity outside the ball is assumed. The gap from the feasibility boundary is $\Delta=L-\mu R\ge0$.

Model: For $\Delta=0$, every objective is $f(x)=f(0)+\mu\|x\|_2^2/2$. For $\Delta>0$, define $$S_\Delta=\max_{0\le r\le R}\{\Delta r-\mu r^2/2\}=\begin{cases}\Delta^2/(2\mu),&0\le\Delta\le\mu R,\\ \Delta R-\mu R^2/2,&\Delta>\mu R.\end{cases}$$

Oracle: At a feasible point $x\in B_2(0,R)$, the oracle returns only the exact scalar $f(x)$. The unknown function is fixed before an independent private seed is drawn. No values outside the ball, derivatives, or hidden minimizers are supplied.

Oracle: The public inputs are $d,L,\mu,R,\varepsilon$ and the ball. All scalar values, including the two values of a paired estimate, are charged. Projection and operations on the known ball are free.

**Budget convention.** fixed_worst_case

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

$\Xi$: Lipschitz-based saturation scale used in the parameter-separated comparisons. **Domain:** $\Xi>0$.

$\Xi=\min\{d,(LR/\varepsilon)^2,L^2/(\mu\varepsilon)\}$ in views deterministic and randomized. The full-slack comparisons use $m_\varepsilon$ instead.

$\theta_0$: Fixed separation parameter used only in the parameter-separated deterministic and randomized comparisons. **Domain:** $0<\theta_0<1$.

In views deterministic and randomized only: $0<\theta_0<1$ is fixed and $\mu R/L\le\theta_0$. The full-slack views impose no such separation.

$d_0$: Universal sufficient-dimension threshold in the parameter-separated lower-bound comparisons. **Domain:** $d_0>0$.

The threshold is determined by the applicable parameter-separated theorem and pertains only to views deterministic and randomized.

$c_{\theta_0}$: Accuracy-threshold constant for the parameter-separated lower-bound comparisons. **Domain:** $c_{\theta_0}>0$.

The positive constant depends only on the fixed $\theta_0$ in views deterministic and randomized; it is not a restriction in the full-slack views.

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

$\Delta$: Total-Lipschitz slack **Domain:** $\Delta\ge0$.

$\Delta=L-\mu R$

$S_\Delta$: Exact minimax zero-query expected risk **Domain:** $S_\Delta\ge0$.

$S_\Delta=\Delta^2/(2\mu)$ if $0\le\Delta\le\mu R$, and $S_\Delta=\Delta R-\mu R^2/2$ otherwise.

$a_\varepsilon$: Radius branch scale **Domain:** $a_\varepsilon\ge0$.

$a_\varepsilon=(\Delta R/\varepsilon)^2$

$b_\varepsilon$: Strong-convexity branch scale **Domain:** $b_\varepsilon\ge0$.

$b_\varepsilon=\Delta^2/(\mu\varepsilon)$

$m_\varepsilon$: Active polynomial branch **Domain:** $m_\varepsilon\ge0$.

$m_\varepsilon=\min\{d,a_\varepsilon,b_\varepsilon\}$

$c_0$: Universal relative-accuracy threshold **Domain:** $0<c_0<1$.

A sufficiently small universal constant in Theorem thm:main.

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

#### Q3 - minimax metric resource quantity

**View.** Randomized / Expected loss / Full slack range

$$
T_\varepsilon^{\rm exp}(d,L,\mu,R)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{exact\ scalar\ value}}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

#### Q4 - minimax metric resource quantity

**View.** Randomized / 1/2 success / Full slack range

$$
T_\varepsilon^{\rm prob(1/2)}(d,L,\mu,R)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{exact\ scalar\ value}}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

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

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B5

$$
0
$$

**Upper bound.** B4

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

### R6 - Parameter regime E02.NEW.zero_region

**Region.** $0<\mu R\le L,\ \varepsilon\ge\min\{LR,(L-\mu R)^2/(2\mu)\}$.

**Views.** Randomized

**Quantity.** Q2

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B11

$$
0
$$

**Upper bound.** B10

$$
0
$$

### R7 - Radius branch / Expected loss

**Region.** $\varepsilon\ge\max\{\mu R^2,\Delta R/\sqrt d\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$. All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously. For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row. The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Views.** Randomized / Expected loss / Full slack range

**Quantity.** Q3

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B13

$$
\Omega(da_\varepsilon/\log(ea_\varepsilon))
$$

**Upper bound.** B12

$$
O(da_\varepsilon)
$$

**Gap or comparison.**

$$
O(\log(ea_\varepsilon))
$$

### R8 - Strong-convexity branch, including small positive slack / Expected loss

**Region.** $\Delta^2/(\mu d)\le\varepsilon\le\mu R^2$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$. All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously. For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row. The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Views.** Randomized / Expected loss / Full slack range

**Quantity.** Q3

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B15

$$
\Omega(db_\varepsilon/\log(eb_\varepsilon))
$$

**Upper bound.** B14

$$
O(db_\varepsilon)
$$

**Gap or comparison.**

$$
O(\log(eb_\varepsilon))
$$

### R9 - Dimension-limited branch / Expected loss

**Region.** $\varepsilon\le\min\{\Delta R/\sqrt d,\Delta^2/(\mu d)\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$. All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously. For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row. The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Views.** Randomized / Expected loss / Full slack range

**Quantity.** Q3

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B17

$$
\Omega(d^2/\log(ed))
$$

**Upper bound.** B16

$$
O\!\left(d^2\log(d+1)\log(128S_\Delta/\varepsilon)\right)
$$

**Gap or comparison.**

$$
O\!\left(\log(ed)\log(d+1)\log(128S_\Delta/\varepsilon)\right)
$$

### R10 - Relative-accuracy transition without a matching polynomial bracket

**Region.** $d\ge1$, $L>\mu R>0$, and $c_0S_\Delta<\varepsilon<S_\Delta$. All d>=1. The exact zero-query risk assertion is an expected-loss statement and is not used as a sharp zero-query probability threshold.

**Views.** Randomized / Expected loss / Full slack range

**Quantity.** Q3

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Other quantified gap

**Lower bound.** B19

$$
1
$$

**Upper bound.** B18

$$
C\min\left\{da_\varepsilon,db_\varepsilon,d^2\log(d+1)\log(128S_\Delta/\varepsilon)\right\}
$$

**Gap or comparison.** Upper-to-lower ratio at most the displayed upper expression; no nontrivial matching rate is established.

### R11 - Zero-query range, including the degenerate boundary

**Region.** $d\ge1$, $L\ge\mu R>0$, and $\varepsilon\ge S_\Delta$. In particular, every $\varepsilon>0$ is included when $L=\mu R$. All d>=1. At $\Delta=0$ the minimizer is known to be the origin. For expected loss the zero-query minimax error is exactly $S_\Delta$; a converse zero-query threshold is not asserted for the 1/2-success view.

**Views.** Randomized / Expected loss / Full slack range

**Quantity.** Q3

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B21

$$
0
$$

**Upper bound.** B20

$$
0
$$

**Gap or comparison.** Exact zero calls in the displayed range.

### R12 - Radius branch / 1/2 success

**Region.** $\varepsilon\ge\max\{\mu R^2,\Delta R/\sqrt d\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$. All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously. For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row. The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Views.** Randomized / 1/2 success / Full slack range

**Quantity.** Q4

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B23

$$
\Omega(da_\varepsilon/\log(ea_\varepsilon))
$$

**Upper bound.** B22

$$
O(da_\varepsilon)
$$

**Gap or comparison.**

$$
O(\log(ea_\varepsilon))
$$

### R13 - Strong-convexity branch, including small positive slack / 1/2 success

**Region.** $\Delta^2/(\mu d)\le\varepsilon\le\mu R^2$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$. All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously. For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row. The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Views.** Randomized / 1/2 success / Full slack range

**Quantity.** Q4

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B25

$$
\Omega(db_\varepsilon/\log(eb_\varepsilon))
$$

**Upper bound.** B24

$$
O(db_\varepsilon)
$$

**Gap or comparison.**

$$
O(\log(eb_\varepsilon))
$$

### R14 - Dimension-limited branch / 1/2 success

**Region.** $\varepsilon\le\min\{\Delta R/\sqrt d,\Delta^2/(\mu d)\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$. All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously. For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row. The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Views.** Randomized / 1/2 success / Full slack range

**Quantity.** Q4

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B27

$$
\Omega(d^2/\log(ed))
$$

**Upper bound.** B26

$$
O\!\left(d^2\log(d+1)\log(128S_\Delta/\varepsilon)\right)
$$

**Gap or comparison.**

$$
O\!\left(\log(ed)\log(d+1)\log(128S_\Delta/\varepsilon)\right)
$$

### R15 - Relative-accuracy transition without a matching polynomial bracket

**Region.** $d\ge1$, $L>\mu R>0$, and $c_0S_\Delta<\varepsilon<S_\Delta$. All d>=1. The exact zero-query risk assertion is an expected-loss statement and is not used as a sharp zero-query probability threshold.

**Views.** Randomized / 1/2 success / Full slack range

**Quantity.** Q4

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B28

$$
C\min\left\{da_\varepsilon,db_\varepsilon,d^2\log(d+1)\log(128S_\Delta/\varepsilon)\right\}
$$

**Gap or comparison.** The manuscript does not give a matching lower direction for this probability window.

### R16 - Zero-query range, including the degenerate boundary

**Region.** $d\ge1$, $L\ge\mu R>0$, and $\varepsilon\ge S_\Delta$. In particular, every $\varepsilon>0$ is included when $L=\mu R$. All d>=1. At $\Delta=0$ the minimizer is known to be the origin. For expected loss the zero-query minimax error is exactly $S_\Delta$; a converse zero-query threshold is not asserted for the 1/2-success view.

**Views.** Randomized / 1/2 success / Full slack range

**Quantity.** Q4

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B30

$$
0
$$

**Upper bound.** B29

$$
0
$$

**Gap or comparison.** Exact zero calls in the displayed range.

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

**Conditions.** Localization algorithm for the original convex class.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_DET_SUBGRAD

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_ZERO, ZO_PROOF_SLACK_CENTER

### B5 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $0<\mu R\le L,\ \varepsilon\ge\min\{LR,(L-\mu R)^2/(2\mu)\}$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_ZERO, ZO_PROOF_SLACK_CENTER

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_PAIRED_UPPER, ZO_PROOF_GEOMETRY_BASE

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_DET_SUBGRAD

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

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

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_ZERO, ZO_PROOF_SLACK_CENTER

### B11 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $0<\mu R\le L,\ \varepsilon\ge\min\{LR,(L-\mu R)^2/(2\mu)\}$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_ZERO, ZO_PROOF_SLACK_CENTER

### B12 - Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss / Full slack range

**Witness or lower-bound scope.** randomized_or_deterministic

$$
O(da_\varepsilon)
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\varepsilon\ge\max\{\mu R^2,\Delta R/\sqrt d\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main, eq:main-two-sided; Table tab:regimes; Theorem thm:upper

Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization. Unrestricted randomized algorithms

### B13 - Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss / Full slack range

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(da_\varepsilon/\log(ea_\varepsilon))
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\varepsilon\ge\max\{\mu R^2,\Delta R/\sqrt d\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorems thm:main, thm:expected-lower, thm:prob-lower; Table tab:regimes

Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families. All adaptive randomized algorithms with arbitrary feasible outputs

### B14 - Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss / Full slack range

**Witness or lower-bound scope.** randomized_or_deterministic

$$
O(db_\varepsilon)
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\Delta^2/(\mu d)\le\varepsilon\le\mu R^2$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main, eq:main-two-sided; Table tab:regimes; Theorem thm:upper

Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization. Unrestricted randomized algorithms

### B15 - Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss / Full slack range

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(db_\varepsilon/\log(eb_\varepsilon))
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\Delta^2/(\mu d)\le\varepsilon\le\mu R^2$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorems thm:main, thm:expected-lower, thm:prob-lower; Table tab:regimes

Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families. All adaptive randomized algorithms with arbitrary feasible outputs

### B16 - Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss / Full slack range

**Witness or lower-bound scope.** randomized_or_deterministic

$$
O\!\left(d^2\log(d+1)\log(128S_\Delta/\varepsilon)\right)
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\varepsilon\le\min\{\Delta R/\sqrt d,\Delta^2/(\mu d)\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main, eq:main-two-sided; Table tab:regimes; Theorem thm:upper

Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization. Unrestricted randomized algorithms

### B17 - Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss / Full slack range

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(d^2/\log(ed))
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\varepsilon\le\min\{\Delta R/\sqrt d,\Delta^2/(\mu d)\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorems thm:main, thm:expected-lower, thm:prob-lower; Table tab:regimes

Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families. All adaptive randomized algorithms with arbitrary feasible outputs

### B18 - Localized upper-envelope algorithm

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss / Full slack range

**Witness or lower-bound scope.** randomized_or_deterministic

$$
C\min\left\{da_\varepsilon,db_\varepsilon,d^2\log(d+1)\log(128S_\Delta/\varepsilon)\right\}
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $d\ge1$, $L>\mu R>0$, and $c_0S_\Delta<\varepsilon<S_\Delta$.; The exact zero-query risk assertion is an expected-loss statement and is not used as a sharp zero-query probability threshold.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** Universal upper constant.

**Logarithmic factors.** Only the displayed upper logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:upper, eq:upper-envelope

Localized upper-envelope algorithm. Unrestricted randomized algorithms

### B19 - Any zero-query randomized output has worst-instance expected error at least S_Delta

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss / Full slack range

**Witness or lower-bound scope.** elementary

$$
1
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $d\ge1$, $L>\mu R>0$, and $c_0S_\Delta<\varepsilon<S_\Delta$.; The exact zero-query risk assertion is an expected-loss statement and is not used as a sharp zero-query probability threshold.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** Universal upper constant.

**Logarithmic factors.** Only the displayed upper logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main, exact zero-query expected risk assertion

Any zero-query randomized output has worst-instance expected error at least S_Delta. All randomized algorithms

### B20 - Return the center of the known ball

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss / Full slack range

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $d\ge1$, $L\ge\mu R>0$, and $\varepsilon\ge S_\Delta$. In particular, every $\varepsilon>0$ is included when $L=\mu R$.; At $\Delta=0$ the minimizer is known to be the origin. For expected loss the zero-query minimax error is exactly $S_\Delta$; a converse zero-query threshold is not asserted for the 1/2-success view.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main; Theorem thm:slack-geometry

Return the center of the known ball. Deterministic algorithm

### B21 - Nonnegative query count

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss / Full slack range

**Witness or lower-bound scope.** elementary

$$
0
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $d\ge1$, $L\ge\mu R>0$, and $\varepsilon\ge S_\Delta$. In particular, every $\varepsilon>0$ is included when $L=\mu R$.; At $\Delta=0$ the minimizer is known to be the origin. For expected loss the zero-query minimax error is exactly $S_\Delta$; a converse zero-query threshold is not asserted for the 1/2-success view.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main

Nonnegative query count. All algorithms

### B22 - Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / 1/2 success / Full slack range

**Witness or lower-bound scope.** randomized_or_deterministic

$$
O(da_\varepsilon)
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\varepsilon\ge\max\{\mu R^2,\Delta R/\sqrt d\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main, eq:main-two-sided; Table tab:regimes; Theorem thm:upper

Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization. Unrestricted randomized algorithms

### B23 - Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / 1/2 success / Full slack range

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(da_\varepsilon/\log(ea_\varepsilon))
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\varepsilon\ge\max\{\mu R^2,\Delta R/\sqrt d\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorems thm:main, thm:expected-lower, thm:prob-lower; Table tab:regimes

Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families. All adaptive randomized algorithms with arbitrary feasible outputs

### B24 - Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / 1/2 success / Full slack range

**Witness or lower-bound scope.** randomized_or_deterministic

$$
O(db_\varepsilon)
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\Delta^2/(\mu d)\le\varepsilon\le\mu R^2$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main, eq:main-two-sided; Table tab:regimes; Theorem thm:upper

Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization. Unrestricted randomized algorithms

### B25 - Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / 1/2 success / Full slack range

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(db_\varepsilon/\log(eb_\varepsilon))
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\Delta^2/(\mu d)\le\varepsilon\le\mu R^2$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorems thm:main, thm:expected-lower, thm:prob-lower; Table tab:regimes

Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families. All adaptive randomized algorithms with arbitrary feasible outputs

### B26 - Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / 1/2 success / Full slack range

**Witness or lower-bound scope.** randomized_or_deterministic

$$
O\!\left(d^2\log(d+1)\log(128S_\Delta/\varepsilon)\right)
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\varepsilon\le\min\{\Delta R/\sqrt d,\Delta^2/(\mu d)\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main, eq:main-two-sided; Table tab:regimes; Theorem thm:upper

Localize the unknown convex residual, then select two-point estimation or value-oracle convex localization. Unrestricted randomized algorithms

### B27 - Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / 1/2 success / Full slack range

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(d^2/\log(ed))
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $\varepsilon\le\min\{\Delta R/\sqrt d,\Delta^2/(\mu d)\}$; additionally $d\ge1$, $L>\mu R>0$, and $0<\varepsilon\le c_0S_\Delta$.; For $0<\Delta\le\mu R$, $S_\Delta=\Delta^2/(2\mu)$, so the strong-convexity row is nonempty only when $\Delta^2/(\mu d)\le c_0\Delta^2/(2\mu)$. This enforces $d\ge2/c_0$ for that near-boundary row.; The constant-width transition $c_0S_\Delta<\varepsilon<S_\Delta$ is excluded from every two-sided near-optimal claim. Boundary equalities may be assigned to either adjacent active branch.

**Dimension conditions.** All integer dimensions d>=1, including d=1; a row can be empty because all its predicates must hold simultaneously.

**Constants.** All constants are universal; none depend on the positive slack Delta.

**Logarithmic factors.** Only the displayed logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorems thm:main, thm:expected-lower, thm:prob-lower; Table tab:regimes

Quadratic regularization of a fixed support-function prior, plus spherical and one-dimensional endpoint families. All adaptive randomized algorithms with arbitrary feasible outputs

### B28 - Localized upper-envelope algorithm

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / 1/2 success / Full slack range

**Witness or lower-bound scope.** randomized_or_deterministic

$$
C\min\left\{da_\varepsilon,db_\varepsilon,d^2\log(d+1)\log(128S_\Delta/\varepsilon)\right\}
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $d\ge1$, $L>\mu R>0$, and $c_0S_\Delta<\varepsilon<S_\Delta$.; The exact zero-query risk assertion is an expected-loss statement and is not used as a sharp zero-query probability threshold.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** Universal upper constant.

**Logarithmic factors.** Only the displayed upper logarithms.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:upper, eq:upper-envelope

Localized upper-envelope algorithm. Unrestricted randomized algorithms

### B29 - Return the center of the known ball

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / 1/2 success / Full slack range

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $d\ge1$, $L\ge\mu R>0$, and $\varepsilon\ge S_\Delta$. In particular, every $\varepsilon>0$ is included when $L=\mu R$.; At $\Delta=0$ the minimizer is known to be the origin. For expected loss the zero-query minimax error is exactly $S_\Delta$; a converse zero-query threshold is not asserted for the 1/2-success view.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main; Theorem thm:slack-geometry

Return the center of the known ball. Deterministic algorithm

### B30 - Nonnegative query count

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / 1/2 success / Full slack range

**Witness or lower-bound scope.** elementary

$$
0
$$

**Sources.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf)

**Conditions.** $d\ge1$, $L\ge\mu R>0$, and $\varepsilon\ge S_\Delta$. In particular, every $\varepsilon>0$ is included when $L=\mu R$.; At $\Delta=0$ the minimizer is known to be the origin. For expected loss the zero-query minimax error is exactly $S_\Delta$; a converse zero-query threshold is not asserted for the 1/2-success view.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [6](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf) Theorem thm:main

Nonnegative query count. All algorithms

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 8b02250d017cc357f0365c337f3c6c6e6adb00d488ed00a18b1051a374ab0fea

### Native proof: ZO_PROOF_DET_SUBGRAD

Native pointer: /proofs/0; canonical SHA-256: 407c5df5e344384419290b1738e9bef775ee3cb0a66626433c2cb6decdf4fe2c

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 9b122cc20ebbcbb8c7d338e1124a537a201bd66352037e20d3c520fe88f01dba

Deterministic extraction of an approximate subgradient

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

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 877cdb9cd795caed0e13c33ad2863f0ada58ec1582a858a422039d398b8d6202

Exact real scalar values; finite positive probe scales; free real arithmetic and no bit-precision charge. Ball-restricted variants keep all probes inside the ball; global variants allow all-space probes.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/0/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: afe187f3be4db81d4b193c8a2c5076055a0f310fb0d5c7839d30f66b59332f42

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 2

Native pointer: /proofs/0/source_refs/1; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

### Native proof: ZO_PROOF_ZERO

Native pointer: /proofs/1; canonical SHA-256: 1d6580814630c8e2805d1bef988f17262747efcfe8580ea0d6eaace3086f220c

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: a1c4db43e97db238b9e152f2d0f29dccb6ee901b91806fdf8840d239abdee28f

Zero-query certificates

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: e337fe1bbdc7a8471c27bff8578ac9695fda39f5bd738324501658aee12cbc83

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 1415baad26ae3bdb7a7f19af0ab941587cafa672fc7447677224c888ab47c12b

The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/1/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

### Native proof: ZO_PROOF_SLACK_CENTER

Native pointer: /proofs/2; canonical SHA-256: 55bf69c4febf9a9281d7fbfa7e458a6c239ad3559fc0df66180b690cb3acfc6f

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 517ecf32e097a6c5a437bd5f95f826436c8351a973b941b1fc798fdebbb3704d

The center certificate for a strongly convex Lipschitz function

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: 34a1fe8db0e58b6f2746f5a9669ebbeb033cfda43a4f2202dbee4246c97709d8

The class is nonempty only if $\mu R\le L$, and
$$f(0)-\min_{B_2(R)} f\le\min\{LR,(L-\mu R)^2/(2\mu)\}.$$
In particular, the center is optimal when $\mu R=L$.

Let $g_0\in\partial f(0)$. If $g_0\ne0$, put $u=g_0/\|g_0\|$ and choose $g_t\in\partial f(tu)$ for $0<t<R$. Strong monotonicity gives $\langle g_t,u\rangle\ge\|g_0\|+\mu t$. Interior subgradients have norm at most $L$, hence $\|g_0\|\le L-\mu R$ by letting $t\uparrow R$. If $g_0=0$, the same inequality along any direction gives the feasibility condition $\mu R\le L$.

Strong convexity implies $f(z)\ge f(0)+\langle g_0,z\rangle+\mu\|z\|^2/2\ge f(0)-\|g_0\|^2/(2\mu)$. Combine this with the independent Lipschitz center bound $LR$. The argument uses only the mean function, so it also applies when a finite-sum mean is strongly convex only on the feasible ball.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 46a98e0c8f04c6d71b8a1f1bb47a703040db3484c023f1f81cc43470b1ec87f2

A convex function on $B_2(R)$, $\mu$-strongly convex and $L$-Lipschitz; interior subgradients are taken without an artificial boundary normal cone.

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/2/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: module_dependencies

Native pointer: /proofs/2/module_dependencies; canonical SHA-256: c342637a4b1efcd5b0aad863488ba6e59d8020114eddab59351d9b9336fb523b

#### Native item 1

Native pointer: /proofs/2/module_dependencies/0; canonical SHA-256: b0a31a9c3978e4f0bd22d685df94eae34b1086bfebe92c4f0dbcb3e63bdfca0b

ZO_PROOF_ZERO

### Native proof: ZO_PROOF_PAIRED_MOMENT

Native pointer: /proofs/3; canonical SHA-256: 1590ade2e6787fe33d10f650f8ab64ef46bf6350869f6f4f185dad60be780bd6

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 293f2ab735f268a2ffbfdb19ec489b03f31469acbe264107320d5061ad83ae63

Ball smoothing and the same-sample directional moment

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: 3ad958d5da6f01b544d353454c3372bc69148946dc23d87a9f02d9c83e87957c

With ball smoothing $f_h(x)=\mathbb E_{U\sim\operatorname{Unif}(B_2)}f(x+hU)$ and a sphere direction $u$,
$$g_h(x)=\frac d{2h}[F(x+hu;Z)-F(x-hu;Z)]u,\quad\mathbb E g_h=\nabla f_h,\quad\mathbb E\|g_h\|^r\le(\sqrt{2d}L)^r.$$
For $r=2$, the bound is $2dL^2$.

For each fixed sample, the scalar difference $a(u)=F(x+hu;Z)-F(x-hu;Z)$ is odd on the sphere, hence has mean zero, and has Lipschitz constant at most $2hG$. Sphere Poincare gives $\mathbb E_u a(u)^2\le4h^2G^2/(d-1)$ for $d\ge2$. Thus $\mathbb E_u\|g_h\|^2\le d^2G^2/(d-1)\le2dG^2$; for $d=1$ the difference quotient is directly bounded by $G$. Apply Jensen only to the direction expectation and then integrate over the sample:
$$\mathbb E_{Z,u}\|g_h\|^r\le\mathbb E_Z(\mathbb E_u\|g_h\|^2)^{r/2}\le(2d)^{r/2}\mathbb E G^r.$$
No second moment of $G$ is needed when $r<2$. The divergence theorem for ball convolution gives the unbiasedness identity. Integrability follows from the Lipschitz difference bound. Convexity gives $f_h\ge f$, and $|f_h-f|\le hL$; mean strong convexity is preserved on the region where every translated point satisfies it. All statements hold conditionally on the past when the next sample and direction are fresh. Reusing an old adaptively explored sample does not automatically preserve this conditional moment calculation.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: 8b49ec7dca2985f462ed168dfff1ed752288e50486b8b7133d5d5ea0e91edc18

A fresh sample each round; the same sample supplies both values; sample Lipschitz modulus $G$ on the stated query neighborhood; $\mathbb E G^r\le L^r$, $1<r\le2$.

#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/3/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: 2b913a5fb0aabb726f77d1aae7fd6ffc8d2d2a43974d8a9a576b6ed5f74e86bc

#### Native item 1

Native pointer: /proofs/3/source_refs/0; canonical SHA-256: 7ec8d4ed8f91c132a1de87534a55d39252f47d06682b98ca5b170368ee0a8388

SO_SRC_072506cc03b2f8a7

### Native proof: ZO_PROOF_PAIRED_UPPER

Native pointer: /proofs/4; canonical SHA-256: 2e0e54fd584fc5d48d0ce8a9dba241d65ebbaa7375747bcc8134ff73f2fcfc4e

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: e508c27dccb22eb6891bf8af030dc2253349aaf59b1ef7a90b2a3177a1b6408f

Projected optimization with same-sample two-point values

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: 685be49a225f461c5aad1c8f1a5c7d6be838d104f66a8c19ee8e9caada27dac4

For a $\mu$-strongly-convex mean with $\mathbb E G^2\le L^2$, $K$ rounds and $T=2K$ scalar calls give
$$\mathbb E[f(\bar x_K)-f_*]\le\frac{4dL^2}{\mu(K+1)}+2hL.$$
The merely convex branch uses $O(d(LR/\varepsilon)^2)$ values.

Run the paired estimator on $K_h=B_2(R-h)$ and let $x_{h,*}$ minimize $f_h$ there. The shrinkage comparator $y=(1-h/R)x_*$ gives $f_h(y)\le f_*+2hL$. Set $V=2dL^2$, $\eta_t=2/[\mu(t+1)]$, and $D_t=\mathbb E\|x_t-x_{h,*}\|^2$. Projection and strong convexity yield
$$\mathbb E[f_h(x_t)-f_h(x_{h,*})]\le\frac{\mu(t-1)}4D_t-\frac{\mu(t+1)}4D_{t+1}+\frac{V}{\mu(t+1)}.$$
Multiply by $t$, telescope, and average with weights $2t/[K(K+1)]$. The initial distance coefficient is zero and the last is nonpositive, giving $2V/[\mu(K+1)]$. Add the comparator error. For expected accuracy choose, for example, $h=\varepsilon/(8L)$ and $K+1\ge8dL^2/(\mu\varepsilon)$. For success probability $2/3$, use $h=\varepsilon/(12L)$ and $K+1\ge24dL^2/(\mu\varepsilon)$, making the expected nonnegative gap at most $\varepsilon/3$ before Markov.

For convex objectives, the projected averaging recursion with step $R/\sqrt{VK}$ gives expected optimization error at most $R\sqrt{V/K}$, plus the same smoothing/shrinkage error. Uniform component sampling makes the estimator unbiased for the finite-sum mean and costs exactly two selected-component values per round. Neither the oracle nor the components need be stochastic in that case; the algorithm supplies the randomness. These bounds also hold under an almost-sure Lipschitz promise, since it implies the required second moment. The Gaussian lower construction in the separate lower lemma does not acquire that stronger promise.

#### Native field: scope

Native pointer: /proofs/4/scope; canonical SHA-256: 1cee90c0ade7a1c76974664107d84323ced5a0094233ab2475673590acf69a2f

Optimization/output in $B_2(R)$; all two-point queries remain in the prescribed ball; mean strong convexity suffices. A uniformly sampled finite-sum component is also a valid fresh sample.

#### Native field: limitations

Native pointer: /proofs/4/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/4/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: module_dependencies

Native pointer: /proofs/4/module_dependencies; canonical SHA-256: 0f93027dd13c1fc76f53eafc5f7af337161f3e067e9523895d0587c084c781f1

#### Native item 1

Native pointer: /proofs/4/module_dependencies/0; canonical SHA-256: 89f132536e860e550967b3b720a81cd0588e96be63dd5faf8219129f756df13e

ZO_PROOF_PAIRED_MOMENT

### Native proof: ZO_PROOF_GEOMETRY_BASE

Native pointer: /proofs/5; canonical SHA-256: d6b8eb7b837b547d07112f9065a4fff7b241625efffba7e56094a8b8f9d6c4fd

#### Native field: title

Native pointer: /proofs/5/title; canonical SHA-256: 1ab0b833ad81901c161d28bf8c7db1cfbea162415c9eb514997fbae0a1895d3c

Norm conversion, penalized localization, and affine equivalence

#### Native field: body

Native pointer: /proofs/5/body; canonical SHA-256: 4468fc6d9bbf4a1ea74651e295f99626443555521dac386c650e090b3f22dbb9

Let $a_B=\max_{\|u\|_2=1}\|u\|_B$ and let $R_2(K)$ be a public Euclidean enclosing radius. Then $\beta_2=a_B^2\beta$, $L_2=a_BL$, and $D_2=a_BR_2(K)$ give the deterministic smooth envelope
$$O\!\left(1+\min\{d\sqrt{\beta D_2^2/\varepsilon},d^2\log(e+\beta D_2^2/\varepsilon)\}\right)$$
and Lipschitz localization $O(1+d^2\log(d+1)\log(e+LD_2/\varepsilon))$.

The norm inequality $\|v\|_B\le a_B\|v\|_2$ and its dual give the stated Euclidean smoothness and Lipschitz constants. Apply the exact-value Euclidean acceleration or smooth localization theorem with those constants and the public radius; each transformed value remains one scalar call. The global-minimizer promise is retained for the smooth localization argument.

For a Lipschitz objective minimized over a known convex set $K$, define $g(x)=f(x)+L_2\operatorname{dist}_2(x,K)$. This is convex and $2L_2$-Lipschitz, $\min g=\min_K f$ on a ball containing $K$, and $f(\Pi_Kx)\le g(x)$. One value of $g$ uses one value of $f$ plus public geometry. The Euclidean ball localization theorem therefore returns a legal point of $K$ after projection. This is a concrete transfer to a general body, not a presumed general-body localization theorem.

If $B=UB_2(1)$ and $K=c+RB$ for a public invertible matrix $U$, set $g(y)=f(c+Uy)$. Then $\|Uv\|_B=\|v\|_2$ and $\|U^\top w\|_2=\|w\|_{B,*}$. Thus both the Lipschitz and smoothness budgets are unchanged, the feasible or localization body becomes $B_2(R)$, and one value plus the inverse output map preserves the exact gap, budget, and guarantee. No condition-number factor appears. Deterministic acceleration/localization and randomized two-point methods keep their original algorithm permissions.

#### Native field: scope

Native pointer: /proofs/5/scope; canonical SHA-256: e5bf34af7950d8ee2664d09b259b1849e4fa3ae1ee7a4405a616ac92a8ff6664

Globally defined objectives, the declared regularity norm, a public feasible or localization body, and the stated free geometric operations.

#### Native field: limitations

Native pointer: /proofs/5/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/5/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: source_refs

Native pointer: /proofs/5/source_refs; canonical SHA-256: a1795be38e4c9c395f3571ba8859982c16974469de33e616917508807f2842b6

#### Native item 1

Native pointer: /proofs/5/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native item 2

Native pointer: /proofs/5/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 3

Native pointer: /proofs/5/source_refs/2; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

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

[6] Colombo_U10. Exact-Value Complexity of Nonsmooth Strongly Convex Optimization: Uniform Bounds and Boundary Geometry. strongly_convex_exact_value.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U10/manuscript.pdf
