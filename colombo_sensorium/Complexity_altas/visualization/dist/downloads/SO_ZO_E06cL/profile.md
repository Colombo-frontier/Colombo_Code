# Lipschitz convex optimization in a general norm with known convex constraints and exact values

**Setting ID.** `SO_ZO_E06cL`

Single-objective optimization

Minimize $f$ globally over $K$ and return a point with small objective gap.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Logarithmic gap

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Function lipschitz in declared norm; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; query domain: Full space; operation: Function value; feedback quality: Exact

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic algorithms; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $K$ and return a point with small objective gap.

### Admissible model

$B\subset\mathbb{R}^d$ is a known compact, centrally symmetric convex body with nonempty interior. It induces the norm $\|x\|_B=\inf\{t>0:x\in tB\}$. The set $K\subset\mathbb{R}^d$ is known, nonempty, compact and convex.

$f:\mathbb{R}^d\to\mathbb{R}$ is globally convex and satisfies $|f(x)-f(y)|\le L\|x-y\|_B$. Constrained minimization is over $K$; boundary minimizers are allowed.

Ball-geometry subregions are written as $K=B_p(0,R)$ and $B=B_q(0,1)$. The exponents $p$ and $q$ describe domain geometry and the regularity norm, respectively. General convex-body specifications do not require this ball parameterization.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

Projection and the stated proximal operations over known geometry are free.

The public inputs are $d$, $B$, $K$, $L$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in K$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in K}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

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

$B$: Unit ball of the known norm **Domain:** $B\subset\mathbb{R}^d$; compact, convex and centrally symmetric, with nonempty interior.

$\|x\|_B=\inf\{t>0:x\in tB\}$

$K$: Known feasible body or minimizer-localization body **Domain:** $K\subset\mathbb{R}^d$; nonempty, compact and convex.

$L$: Public upper bound on the objective Lipschitz constant **Domain:** $L>0$.

$|f(x)-f(y)|\le L\|x-y\|_B$, $x,y\in\mathbb{R}^d$.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$a_B$: Comparison coefficient between the specified norm and the Euclidean norm **Domain:** $a_B>0$.

$a_B=\max_{\|u\|_2=1}\|u\|_B$

$R_2(K)$: Radius of the supplied Euclidean enclosing ball **Domain:** $R_2(K)\ge0$.

$K\subseteq B_2(c_K,R_2(K))$, with known center $c_K$.

$\widehat{R}$: Combined norm and geometry scale **Domain:** $\widehat{R}\ge0$.

$\widehat{R}=a_BR_2(K)$

$r_m(B,K)$: Radius of the largest Euclidean ball inscribed in the norm-contractive linear image **Domain:** $m\in\{1,\ldots,d\},\ r_m(B,K)\ge0$.

$r_m(B,K)=\sup_{\|P\|_{B\to2}\le1}\sup\{r\ge0:\exists z\in\mathbb{R}^m,\ z+rB_2(0,1)\subseteq PK\}$; $P:\mathbb{R}^d\to\mathbb{R}^m$ is a linear map.

$m$: Dimension index of the linear image in the hard construction **Domain:** $m\in\{1,\ldots,d\}$.

Take the maximum only over integers $m$ satisfying the respective accuracy windows.

$p$: Norm exponent of the feasible or localization ball **Domain:** $1\le p\le\infty$.

$q$: Exponent of the regularity norm **Domain:** $1\le q\le\infty$.

For ball parameterizations, $B=B_q(0,1)$; independent of the domain exponent $p$.

$R$: Localization radius for a global minimizer **Domain:** $R>0$.

$x_*\in B_2(0,R)$

$A_B$: Lipschitz accuracy ratio in the matching ellipsoidal subregime **Domain:** $A_B>0$.

$A_B=LR/\varepsilon$; used only in the subregime $K=c+RB$.

$s$: Proximal-norm exponent chosen by the algorithm **Domain:** $1\le s\le\infty$.

Use a public proximal function $\omega_s$ that is $1$-strongly convex with respect to the $\ell_s$ norm.

$\Theta_s$: Range of the selected proximal function over the feasible body **Domain:** $\Theta_s\ge0$.

$\Theta_s=\sup_{x\in K}\omega_s(x)-\inf_{x\in K}\omega_s(x)$; $\omega_s$ is known and $\ell_s$-strongly convex in the $1$ norm.

$m_0$: Minimum dimension for the linear-image hard construction **Domain:** $m_0>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$\varepsilon_Z$: Normalized accuracy threshold for the randomized exact-value lower bound **Domain:** $\varepsilon_Z>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$c_Z$: Positive multiplicative constant in the randomized exact-value lower bound **Domain:** $c_Z>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$C$: Upper-bound constant or universal threshold for an applicability window **Domain:** $C>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$d_0$: Universal dimension threshold required by the lower bound **Domain:** $d_0>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$c$: Small positive constant defining the accuracy window **Domain:** $c>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$c_1$: Positive constant in the cube accuracy window **Domain:** $c_1>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$c_*$: Positive upper-threshold constant for the cube accuracy window **Domain:** $c_*>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $K$.

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

$f_*=\inf_{x\in K}f(x)$.

$\|\cdot\|_{B,*},\|P\|_{B\to2}$: Dual norm and induced operator norm of a linear map **Domain:** $v\in\mathbb{R}^d,\ P:\mathbb{R}^d\to\mathbb{R}^m$.

$\|v\|_{B,*}=\sup_{x\in B}\langle v,x\rangle$, $\|P\|_{B\to2}=\sup_{x\in B}\|Px\|_2$

$c_K,c,z$: Known centers of the enclosing ball, affine ellipsoid and inscribed ball in the linear image **Domain:** $c_K,c\in\mathbb{R}^d,\ z\in\mathbb{R}^m$.

Used only in the corresponding geometric formula.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=K$ and $\mathcal{X}=K$; the function domain is the region on which the model imposes regularity.

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

### R1 - Parameter regime E06cL.R4

**Region.** $B=B_\infty(0,1)$, $K=B_\infty(0,R)$; $d\ge d_0$, $0<\varepsilon\le c_1LR/\sqrt d$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(d^2/\log(ed))
$$

**Upper bound.** B1

$$
O(d^2\log(ed)\log(e+LR\sqrt d/\varepsilon))
$$

**Gap or comparison.** $O(\log^2(ed)\log(e+LR\sqrt d/\varepsilon))$

### R2 - Parameter regime E06cL.R1

**Region.** $B$ is an ellipsoid, $K=c+RB$, $d\ge d_0$ and $A_B\ge C$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B7

$$
\Omega(d\min\{d,A_B^2\}/\log(e\min\{d,A_B^2\}))
$$

**Upper bound.** B8, B9

$$
O(\min\{dA_B^2,d^2\log(ed)\log(e+A_B)\})
$$

**Gap or comparison.** $O(\log^2(ed)\log(e+A_B))$

### R3 - Parameter regime E06cL.R2

**Region.** $B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Polynomial gap

**Lower bound.** B7

$$
\Omega_c(d)
$$

**Upper bound.** B5

$$
O_c(d^2\log(ed))
$$

**Gap or comparison.** $O_c(d\log(ed))$

### R4 - Parameter regime E06cL.R3

**Region.** $B=B_\infty(0,1)$ and $K=B_\infty(0,R)$; $\varepsilon=cLR$ for a fixed $0<c\le c_*$, with $d\ge d_0$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Polynomial gap

**Lower bound.** B7

$$
\Omega_c(d)
$$

**Upper bound.** B6

$$
O_c(d^2)
$$

**Gap or comparison.** $O_c(d)$

### R5 - Parameter regime E06cL.R4

**Region.** $B=B_\infty(0,1)$, $K=B_\infty(0,R)$; $d\ge d_0$, $0<\varepsilon\le c_1LR/\sqrt d$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B7

$$
\Omega(d^2/\log(ed))
$$

**Upper bound.** B4

$$
O(d^2\log(ed)\log(e+LR\sqrt d/\varepsilon))
$$

**Gap or comparison.** $O(\log^2(ed)\log(e+LR\sqrt d/\varepsilon))$

### R6 - Matching-body zero-query endpoint

**Region.** K=c_K+ρB, ρ≥0, ε≥Lρ; fixed target domain.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B11, B13

$$
0
$$

**Upper bound.** B10, B12

$$
0
$$

**Gap or comparison.** Not applicable: exact zero query complexity; no multiplicative ratio is defined.

## 4. Bounds and supporting evidence

### B1 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
U_{L,\det}=O(1+d^2\log(d+1)\log(e+L\widehat{R}/\varepsilon))
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [1](https://arxiv.org/html/2610.00345v1) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $\widehat{R}=a_BR_2(K)$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_BASE

**Source location.** [2](https://arxiv.org/html/2607.16558v2) pdf pages: 12; printed pages: 12; theorem: Proposition 4, with a known distance-penalty reduction

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, with a known distance-penalty reduction

### B2 - Random support functions under a norm-contracting linear image

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max_{m_0\le m\le d:\ 0<\varepsilon\le\varepsilon_Z Lr_m}c_Z\frac{m\min\{m,(Lr_m/\varepsilon)^2\}}{\log(e\min\{m,(Lr_m/\varepsilon)^2\})}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2607.16558v2)

**Conditions.** Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source gives a necessary query count at constant success probability for arbitrary adaptive randomized algorithms. A higher fixed success requirement inherits the same lower bound.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_IMAGE

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 5; printed pages: 5; theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: D26, Theorem 3.3, with zero known regularizer

### B3 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d^2\log(ed)\log(4A_B))
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [1](https://arxiv.org/html/2610.00345v1) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $B\text{ is an ellipsoid},\ K=c+RB,\ A_B>1$

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_BASE

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12

### B4 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
U_{L,\det}=O(1+d^2\log(d+1)\log(e+L\widehat{R}/\varepsilon))
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [1](https://arxiv.org/html/2610.00345v1) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $\widehat{R}=a_BR_2(K)$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_BASE

**Source location.** [2](https://arxiv.org/html/2607.16558v2) pdf pages: 12; printed pages: 12; theorem: Proposition 4, with a known distance-penalty reduction

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, with a known distance-penalty reduction

### B5 - Non-Euclidean randomized two-point mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
U_{L,\mathrm{rand}}=O(1+L^2\Theta_s d^{1+2/\min(q,2)-2/s}/\varepsilon^2)
$$

**Sources.** [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) [6](https://arxiv.org/abs/1802.09022) [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $B=B_q$ and $d\ge3$. The auxiliary prox function is 1-strongly convex in the $\ell _s$ norm, with known range $\Theta_s$. The index s is chosen by the algorithm and need not equal q.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_RANDOM

**Source location.** [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) pdf pages: 4; printed pages: 4; theorem: Theorem 1; Lemmas 1, 3, 4

**Source location.** [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) pdf pages: 6; printed pages: 6; theorem: Theorem 1; Lemmas 1, 3, 4

**Source location.** [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) pdf pages: 8; printed pages: 8; theorem: Theorem 1; Lemmas 1, 3, 4

**Source location.** [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) pdf pages: 7; printed pages: 7; theorem: Theorem 1; Lemmas 1, 3, 4

### B6 - Euclidean randomized two-point mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
U_{L,\mathrm{rand}}=O(1+dL^2\widehat{R}^2/\varepsilon^2)
$$

**Sources.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [1](https://arxiv.org/html/2610.00345v1) [6](https://arxiv.org/abs/1802.09022) [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf)

**Conditions.** Arbitrary B and K; Euclidean prox, with $L_2=a_BL$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_RANDOM

**Source location.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) pdf pages: 4; printed pages: 4; theorem: S17 Theorem 1 / Corollary 2; D26 N.4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: S17 Theorem 1 / Corollary 2; D26 N.4

### B7 - Random support functions under a norm-contracting linear image

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max_{m_0\le m\le d:\ 0<\varepsilon\le\varepsilon_Z Lr_m}c_Z\frac{m\min\{m,(Lr_m/\varepsilon)^2\}}{\log(e\min\{m,(Lr_m/\varepsilon)^2\})}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2607.16558v2)

**Conditions.** Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source gives a necessary query count at constant success probability for arbitrary adaptive randomized algorithms. A higher fixed success requirement inherits the same lower bound.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_IMAGE

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 5; printed pages: 5; theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: D26, Theorem 3.3, with zero known regularizer

### B8 - Geometry-adapted two-point mirror descent or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(dA_B^2)
$$

**Sources.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2607.16558v2) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $B\text{ is an ellipsoid},\ K=c+RB,\ A_B=LR/\varepsilon>1$

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_BASE, ZO_PROOF_PAIRED_UPPER

**Source location.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) pdf pages: 4; printed pages: 4; theorem: Theorem1/Corollary2

### B9 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d^2\log(ed)\log(4A_B))
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [1](https://arxiv.org/html/2610.00345v1) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $B\text{ is an ellipsoid},\ K=c+RB,\ A_B>1$

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_BASE

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12

### B10 - Return the known center without querying

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C^\star\le0
$$

**Conditions.** K=c_K+ρB, ρ≥0, ε≥Lρ; fixed target domain.

**Oracle correspondence.** No objective information is used.

**Guarantee conversion.** The gap is deterministically at most Lρ.

**Output rule.** The known center belongs to K.

**Resource conversion.** Exactly zero scalar objective calls on every execution path.

**Local argument.** ZO_PROOF_MATCHING_BODY_ZERO

### B11 - Nonnegativity of the charged call budget

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
C^\star\ge0
$$

**Conditions.** K=c_K+ρB, ρ≥0, ε≥Lρ; fixed target domain.

**Oracle correspondence.** No additional oracle assumption.

**Guarantee conversion.** Every admissible budget is nonnegative.

**Output rule.** The registered output space is retained.

**Resource conversion.** The infimum of nonnegative call budgets is nonnegative.

**Local argument.** ZO_PROOF_MATCHING_BODY_ZERO

### B12 - Return the known center without querying

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C^\star\le0
$$

**Conditions.** K=c_K+ρB, ρ≥0, ε≥Lρ; fixed target domain.

**Oracle correspondence.** No objective information is used.

**Guarantee conversion.** Deterministic success gives probability one, exceeding 2/3.

**Output rule.** The known center belongs to K.

**Resource conversion.** Exactly zero scalar objective calls on every execution path.

**Local argument.** ZO_PROOF_MATCHING_BODY_ZERO

### B13 - Nonnegativity of the charged call budget

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
C^\star\ge0
$$

**Conditions.** K=c_K+ρB, ρ≥0, ε≥Lρ; fixed target domain.

**Oracle correspondence.** No additional oracle assumption.

**Guarantee conversion.** Every admissible fixed-path budget is nonnegative.

**Output rule.** The registered output space is retained.

**Resource conversion.** The infimum of nonnegative call budgets is nonnegative.

**Local argument.** ZO_PROOF_MATCHING_BODY_ZERO

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: b45828a2b6d2f2166878250af841192a73fb687e846159b2ba06cdb59e2e9503

### Native proof: ZO_PROOF_GEOMETRY_BASE

Native pointer: /proofs/0; canonical SHA-256: d6b8eb7b837b547d07112f9065a4fff7b241625efffba7e56094a8b8f9d6c4fd

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 4468fc6d9bbf4a1ea74651e295f99626443555521dac386c650e090b3f22dbb9

Let $a_B=\max_{\|u\|_2=1}\|u\|_B$ and let $R_2(K)$ be a public Euclidean enclosing radius. Then $\beta_2=a_B^2\beta$, $L_2=a_BL$, and $D_2=a_BR_2(K)$ give the deterministic smooth envelope
$$O\!\left(1+\min\{d\sqrt{\beta D_2^2/\varepsilon},d^2\log(e+\beta D_2^2/\varepsilon)\}\right)$$
and Lipschitz localization $O(1+d^2\log(d+1)\log(e+LD_2/\varepsilon))$.

The norm inequality $\|v\|_B\le a_B\|v\|_2$ and its dual give the stated Euclidean smoothness and Lipschitz constants. Apply the exact-value Euclidean acceleration or smooth localization theorem with those constants and the public radius; each transformed value remains one scalar call. The global-minimizer promise is retained for the smooth localization argument.

For a Lipschitz objective minimized over a known convex set $K$, define $g(x)=f(x)+L_2\operatorname{dist}_2(x,K)$. This is convex and $2L_2$-Lipschitz, $\min g=\min_K f$ on a ball containing $K$, and $f(\Pi_Kx)\le g(x)$. One value of $g$ uses one value of $f$ plus public geometry. The Euclidean ball localization theorem therefore returns a legal point of $K$ after projection. This is a concrete transfer to a general body, not a presumed general-body localization theorem.

If $B=UB_2(1)$ and $K=c+RB$ for a public invertible matrix $U$, set $g(y)=f(c+Uy)$. Then $\|Uv\|_B=\|v\|_2$ and $\|U^\top w\|_2=\|w\|_{B,*}$. Thus both the Lipschitz and smoothness budgets are unchanged, the feasible or localization body becomes $B_2(R)$, and one value plus the inverse output map preserves the exact gap, budget, and guarantee. No condition-number factor appears. Deterministic acceleration/localization and randomized two-point methods keep their original algorithm permissions.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/0/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: e5bf34af7950d8ee2664d09b259b1849e4fa3ae1ee7a4405a616ac92a8ff6664

Globally defined objectives, the declared regularity norm, a public feasible or localization body, and the stated free geometric operations.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: a1795be38e4c9c395f3571ba8859982c16974469de33e616917508807f2842b6

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native item 2

Native pointer: /proofs/0/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 3

Native pointer: /proofs/0/source_refs/2; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 1ab0b833ad81901c161d28bf8c7db1cfbea162415c9eb514997fbae0a1895d3c

Norm conversion, penalized localization, and affine equivalence

### Native proof: ZO_PROOF_GEOMETRY_IMAGE

Native pointer: /proofs/1; canonical SHA-256: 892f66944e9f468111ef70e7b7e06565157e901138bd73bb2fc0740687d59f45

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 1cd2fd44286245db2e01d3873cb88247d0b94a6bed8634b453e4d8636e20dcf0

For an $m$-dimensional Euclidean image radius $r_m(B,K)>0$, smooth and Lipschitz lower bounds may be maximized over the integers $m$ for which their source windows hold.

Define $r_m(B,K)$ as the largest radius of a Euclidean ball contained in $AK$, maximized over maps with $\|A\|_{B\to2}\le1$. Dorn et al., Theorem 3.1, gives
$$T\ge\max\left\{5m/16,\ (m/4096)\min\{m,\sqrt{\beta r_m^2/\varepsilon}\}\right\},\quad0<\varepsilon\le\beta r_m^2/32.$$
Theorem 3.3, with its regularization parameter zero, gives
$$T\ge c_Z\frac{m\min\{m,(Lr_m/\varepsilon)^2\}}{\log(e\min\{m,(Lr_m/\varepsilon)^2\})},\quad m\ge m_Z^\circ,\quad0<\varepsilon\le\varepsilon_ZLr_m.$$
The all-space nonsmooth transfer uses the source's radial penalty for its homogeneous support-function hard family: a target query is simulated by one bounded source query and known arithmetic, and radial decoding preserves the output comparison. This permits the stronger all-space target queries without silently importing a bounded-query lower bound.

For $B=B_q$ and $K=B_p(R)$, put $\theta=(1/2-1/q)_++(1/p-1/2)_+$ and $\gamma=(1/q-1/p)_+$. The source's block certificate is
$$r_m\ge R\lfloor d/m\rfloor^\gamma m^{-\theta},\qquad r_d=Rd^{-\theta}.$$
Insert this certificate into each theorem before maximizing over legal $m$. For $q=2$ and $p\le2$, this is $r_m\ge Rm^{-t}$, $t=1/p-1/2$. Other source certificates, such as constant-radius quotient images, may be added only with their own operator-norm and dimension conditions. An exact geometric radius does not itself prove a matching optimization upper bound.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/1/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: effd57adbd4f2e6b8ac74ca034d0dcd07578cf89617bb46746e94c5feb0022bf

Exact values; the original all-space query/output reduction and all source dimension and accuracy windows are retained.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: b1a6d19e45f290a3e0020b31af423a2cf8268018186490ebf54856d1c7c72f45

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native item 2

Native pointer: /proofs/1/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 0dcb91b1df938d63c713d0645344dd76864094d407e54d2a7a1e71c8b334132e

Image-radius lower bounds and their admissible windows

### Native proof: ZO_PROOF_GEOMETRY_RANDOM

Native pointer: /proofs/2; canonical SHA-256: 9681ed890272028cd769f4d3e770d3cf82f4b4a2854794e610be0370676ef829

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: 3bea1b77967e9979bba854eff9460c14cc442bdb4d30f8ed47a2c86424b0cb99

The applicable randomized upper bounds are
$$O(1+d\sqrt{\eta_{d,s}\beta_2\Theta_s/\varepsilon}),\quad O(1+d\eta_{d,s}\beta_2\Theta_s/\varepsilon),$$
$$O(1+L^2\Theta_s d^{1+2/\min(q,2)-2/s}/\varepsilon^2),\quad O(1+dv_H L_2^2\Theta_H/\varepsilon^2).$$

For the smooth directional methods take $d\ge8$, $1\le s\le2$, $s^*=s/(s-1)$, and $\eta_{d,s}=\min\{s^*-1,16\log d-8\}d^{2/s^*-1}$. Gorbunov, Dvurechensky, and Gasnikov's theorems apply to Euclidean smoothness $\beta_2$ and a prox divergence bounded by $\Theta_s$. Exact noiseless values use batch size one and two scalar values per direction; a finite positive difference scale can be chosen small enough for the fixed budget.

For the Lipschitz method of Akhavan et al., $q$ is the regularity norm and $s$ is the prox norm. Their theorem gives expected gap at most $11.9L\sqrt{\Theta_s d^{1+2/\min(q,2)-2/s}/T}$, with two values per round. Tightening the target by a factor three and applying Markov's inequality gives success probability $2/3$. A usable prox is
$$t_s=\max\{s,1+1/\log(ed)\},\quad a_{s,d}=\frac{d^{2(1/s-1/t_s)}}{t_s-1},\quad\omega_s(x)=a_{s,d}\|x\|_{t_s}^2/2.$$
It is 1-strongly convex in $\ell_s$ and on $B_p(R)$ has range at most $a_{s,d}R^2d^{2(1/t_s-1/p)_+}/2$. In particular, $q=2$, $s=p\le2$ gives the advertised $a_{p,d}d^{2/p^*}(LR/\varepsilon)^2$ term.

For Shamir's general-prox bound let $v_H=(\mathbb E\|U\|_{H,*}^4)^{1/2}$ for a uniform Euclidean sphere direction. Use ball convolution as the smoothed function, with sphere directions in its gradient estimator. The divergence identity belongs to the ball average; this formulation preserves convexity, Lipschitzness, the $O(hL_2)$ smoothing bias, and the source variance proof. All these witnesses are randomized, even when their value oracle is exact and deterministic.

For $B=K=B_1(R)$, Euclidean conversion gives $\beta_2=d\beta$, while the $\ell_1$ prox and directional factor contribute $\Theta_1=O(R^2\log(ed))$ and $\eta_{d,1}=O(\log(ed)/d)$. Substitution yields $O(1+d\log(ed)\sqrt{\beta R^2/\varepsilon})$.

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/2/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 2dd7012e5a43034d8ab19de233e91264d77e296614beac9b70498741bec105aa

The direction distribution, prox norm, regularity norm, query domain, and randomness are distinct parts of the statement.

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: 69e4cc09709afd15b575374fa42764c6d97311a36d4726f2c038a2d3fc2d8dc0

#### Native item 1

Native pointer: /proofs/2/source_refs/0; canonical SHA-256: 2cee8e21b7bc875b704141e0743e94f8f2584df042a10ecb2affee2b910dddf2

SO_SRC_2939e2a45af80e71

#### Native item 2

Native pointer: /proofs/2/source_refs/1; canonical SHA-256: 96834bf80f3bf3ec0a22adf5e62a559ee9bba0f6bbeca157c6b91e15f8b21e04

SO_SRC_72ac6a8c2c1738e3

#### Native item 3

Native pointer: /proofs/2/source_refs/2; canonical SHA-256: 7ec8d4ed8f91c132a1de87534a55d39252f47d06682b98ca5b170368ee0a8388

SO_SRC_072506cc03b2f8a7

#### Native item 4

Native pointer: /proofs/2/source_refs/3; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 5fbacee4c7b340daf764f6a06cd9843993375f5a86b58d10ff50483795d22e87

Randomized directional methods with explicit norm budgets

### Native proof: ZO_PROOF_PAIRED_MOMENT

Native pointer: /proofs/3; canonical SHA-256: 1590ade2e6787fe33d10f650f8ab64ef46bf6350869f6f4f185dad60be780bd6

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: 3ad958d5da6f01b544d353454c3372bc69148946dc23d87a9f02d9c83e87957c

With ball smoothing $f_h(x)=\mathbb E_{U\sim\operatorname{Unif}(B_2)}f(x+hU)$ and a sphere direction $u$,
$$g_h(x)=\frac d{2h}[F(x+hu;Z)-F(x-hu;Z)]u,\quad\mathbb E g_h=\nabla f_h,\quad\mathbb E\|g_h\|^r\le(\sqrt{2d}L)^r.$$
For $r=2$, the bound is $2dL^2$.

For each fixed sample, the scalar difference $a(u)=F(x+hu;Z)-F(x-hu;Z)$ is odd on the sphere, hence has mean zero, and has Lipschitz constant at most $2hG$. Sphere Poincare gives $\mathbb E_u a(u)^2\le4h^2G^2/(d-1)$ for $d\ge2$. Thus $\mathbb E_u\|g_h\|^2\le d^2G^2/(d-1)\le2dG^2$; for $d=1$ the difference quotient is directly bounded by $G$. Apply Jensen only to the direction expectation and then integrate over the sample:
$$\mathbb E_{Z,u}\|g_h\|^r\le\mathbb E_Z(\mathbb E_u\|g_h\|^2)^{r/2}\le(2d)^{r/2}\mathbb E G^r.$$
No second moment of $G$ is needed when $r<2$. The divergence theorem for ball convolution gives the unbiasedness identity. Integrability follows from the Lipschitz difference bound. Convexity gives $f_h\ge f$, and $|f_h-f|\le hL$; mean strong convexity is preserved on the region where every translated point satisfies it. All statements hold conditionally on the past when the next sample and direction are fresh. Reusing an old adaptively explored sample does not automatically preserve this conditional moment calculation.

#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/3/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: 8b49ec7dca2985f462ed168dfff1ed752288e50486b8b7133d5d5ea0e91edc18

A fresh sample each round; the same sample supplies both values; sample Lipschitz modulus $G$ on the stated query neighborhood; $\mathbb E G^r\le L^r$, $1<r\le2$.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: 2b913a5fb0aabb726f77d1aae7fd6ffc8d2d2a43974d8a9a576b6ed5f74e86bc

#### Native item 1

Native pointer: /proofs/3/source_refs/0; canonical SHA-256: 7ec8d4ed8f91c132a1de87534a55d39252f47d06682b98ca5b170368ee0a8388

SO_SRC_072506cc03b2f8a7

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 293f2ab735f268a2ffbfdb19ec489b03f31469acbe264107320d5061ad83ae63

Ball smoothing and the same-sample directional moment

### Native proof: ZO_PROOF_PAIRED_UPPER

Native pointer: /proofs/4; canonical SHA-256: 2e0e54fd584fc5d48d0ce8a9dba241d65ebbaa7375747bcc8134ff73f2fcfc4e

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: 685be49a225f461c5aad1c8f1a5c7d6be838d104f66a8c19ee8e9caada27dac4

For a $\mu$-strongly-convex mean with $\mathbb E G^2\le L^2$, $K$ rounds and $T=2K$ scalar calls give
$$\mathbb E[f(\bar x_K)-f_*]\le\frac{4dL^2}{\mu(K+1)}+2hL.$$
The merely convex branch uses $O(d(LR/\varepsilon)^2)$ values.

Run the paired estimator on $K_h=B_2(R-h)$ and let $x_{h,*}$ minimize $f_h$ there. The shrinkage comparator $y=(1-h/R)x_*$ gives $f_h(y)\le f_*+2hL$. Set $V=2dL^2$, $\eta_t=2/[\mu(t+1)]$, and $D_t=\mathbb E\|x_t-x_{h,*}\|^2$. Projection and strong convexity yield
$$\mathbb E[f_h(x_t)-f_h(x_{h,*})]\le\frac{\mu(t-1)}4D_t-\frac{\mu(t+1)}4D_{t+1}+\frac{V}{\mu(t+1)}.$$
Multiply by $t$, telescope, and average with weights $2t/[K(K+1)]$. The initial distance coefficient is zero and the last is nonpositive, giving $2V/[\mu(K+1)]$. Add the comparator error. For expected accuracy choose, for example, $h=\varepsilon/(8L)$ and $K+1\ge8dL^2/(\mu\varepsilon)$. For success probability $2/3$, use $h=\varepsilon/(12L)$ and $K+1\ge24dL^2/(\mu\varepsilon)$, making the expected nonnegative gap at most $\varepsilon/3$ before Markov.

For convex objectives, the projected averaging recursion with step $R/\sqrt{VK}$ gives expected optimization error at most $R\sqrt{V/K}$, plus the same smoothing/shrinkage error. Uniform component sampling makes the estimator unbiased for the finite-sum mean and costs exactly two selected-component values per round. Neither the oracle nor the components need be stochastic in that case; the algorithm supplies the randomness. These bounds also hold under an almost-sure Lipschitz promise, since it implies the required second moment. The Gaussian lower construction in the separate lower lemma does not acquire that stronger promise.

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

#### Native field: scope

Native pointer: /proofs/4/scope; canonical SHA-256: 1cee90c0ade7a1c76974664107d84323ced5a0094233ab2475673590acf69a2f

Optimization/output in $B_2(R)$; all two-point queries remain in the prescribed ball; mean strong convexity suffices. A uniformly sampled finite-sum component is also a valid fresh sample.

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: e508c27dccb22eb6891bf8af030dc2253349aaf59b1ef7a90b2a3177a1b6408f

Projected optimization with same-sample two-point values

### Native proof: ZO_PROOF_MATCHING_BODY_ZERO

Native pointer: /proofs/5; canonical SHA-256: 4ec2d74319ed348757fa098a0ac1805e2a065d4d36c1795c70295f0f1dd44ef6

#### Native field: baseline_refs

Native pointer: /proofs/5/baseline_refs; canonical SHA-256: 8354be7a3fcdd63335222e734e9b94ba784ba153d64d8584e23a44ccc6305d31

#### Native item 1

Native pointer: /proofs/5/baseline_refs/0; canonical SHA-256: cc81e3798ebc32618496a90480d46151c7b2611cdcb4b0c6aa4ca677ffaf64c4

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/0/sha256; canonical SHA-256: abf1fae15085ad1b3179311d9de64543b05a1f28041dfa986f2483be9e447da1

eb76338084545e3bb4e6499f5de20533d5e758c77e11e1e2c3a80e2a576e90e4

#### Native item 2

Native pointer: /proofs/5/baseline_refs/1; canonical SHA-256: 16e16a91d81ac90006d9de623596fd03825cc127779514310184e9f2f32dbd46

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/1/sha256; canonical SHA-256: 38f974c942511a34d341344c7159095331598aaab36cbd85f1183200916a36f2

583552b3be7cc093f09579c96c8e736b59b3543dcdc921a3dff35916cc233f17

#### Native item 3

Native pointer: /proofs/5/baseline_refs/2; canonical SHA-256: 713042387dabea829b64781565e893cd51bd15e2d130de7281e038eba11701a2

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/2/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/2/sha256; canonical SHA-256: 29b1e254dca764e049b7026212d2dec590ebe7f006854f4cdd10eb0951ddef33

0e6d148192001eff47d2806160019a01d78c8d738539b0e4dd10cc0c879b7fe7

#### Native field: body

Native pointer: /proofs/5/body; canonical SHA-256: 1c436f29f6c136a8144171f723bf998d0273e311dc33aeb46b329916be3b6d5f

Retained premises: the frozen common specification gives global L-Lipschitzness in the B norm, known B,K, output in K, and charges scalar objective values. Both views permit deterministic algorithms; randomized g1 requires success at least 2/3. The q1 quantities minimize a nonnegative call budget. For u∈K=c_K+ρB, ||u-c_K||_B≤ρ, hence f(c_K)-f(u)≤Lρ. Taking the infimum over u proves gap≤Lρ. Returning the known center without objective information therefore succeeds deterministically whenever ε≥Lρ, including equality. If ρ=0, K is a singleton and the gap is zero. Nonnegative costs give C*≥0, proving C*=0 in both views. No global-minimizer promise or extra oracle is used. Sharpness for ρ>0: choose a nonzero vector a and normalize it by max_{b∈B}a·b, positive by compactness, symmetry and nonempty interior. Then max_{b∈B}a·b=1 and |a·v|≤||v||_B by the gauge definition. The global convex functions f_±(x)=±La·(x-c_K) are admissible and have minimum -Lρ on K. Their ε-good sets respectively require a·(x-c_K)≤ε/L-ρ and a·(x-c_K)≥ρ-ε/L. These sets are disjoint for ε<Lρ. A zero-call algorithm has the same output distribution on both objectives, so one success probability is at most 1/2. It cannot satisfy deterministic g1 or randomized success 2/3. This last argument proves only nontriviality below the endpoint, not a main-rate lower bound.

#### Native field: limitations

Native pointer: /proofs/5/limitations; canonical SHA-256: 6b0f1f0a1869fb8936df0e4ed0393b75fa9bae575c903bbce424ee73f83a889f

#### Native item 1

Native pointer: /proofs/5/limitations/0; canonical SHA-256: c281d159b627016d8b56f7be27eaec0b11e8af037ea9808a795baf32cbe2e444

Below Lρ the proof establishes only that zero queries are insufficient.

#### Native item 2

Native pointer: /proofs/5/limitations/1; canonical SHA-256: 1a757e0c1265dcb5c6a832599a3e35dc791c395dd8da355ac554be60cbba8d84

Unchanged external baseline theorems are retained conditionally.

#### Native field: scope

Native pointer: /proofs/5/scope; canonical SHA-256: fa7ce2cf28e484bebc3932c1d8246851f0ade793d2bcf311d0f8b9e74c934b34

Both registered g1 views; known K=c_K+ρB, ρ≥0; fixed-path scalar-value budgets.

#### Native field: source_refs

Native pointer: /proofs/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/5/title; canonical SHA-256: 860938997582bb095dd828732c4f4a8b357c97b816d9443cdf273306ca066580

Exact zero-query threshold for a matching norm body

### Native proof: SO_ZO_E06cL__proof__canonical_bracket_justification_20261116

Native pointer: /proofs/6; canonical SHA-256: 5ba99f5a0e75db27657e999519bd94ab5f69a5829e445ce09cbdd727e02ab0cc

#### Native field: body

Native pointer: /proofs/6/body; canonical SHA-256: 684c665b3c4a236b79d382a25b94eb03fc9570c5fe4b721f3a0d02e3cd7a093a

Use the exact frozen native comparisons, bounds, proof records and joint ledger listed by the current curator's baseline_refs; no new external theorem is assumed. For a fixed comparison predicate and unchanged quantity, view, guarantee and resource, matching upper/lower zero implies exact complexity zero by nonnegativity. Its canonical main state is optimal and a multiplicative ratio is inapplicable. Matching positive-cost upper/lower orders likewise use optimal; saturation is a separate region property. An alias does not establish any new inequality. Aggregate summary counts are the histogram of these actual native states; missing sides are their union; only logarithmic_gap, polynomial_gap and other_quantified_gap belong to gap_classes. Joint-budget-unclosed is its own special state and does not define a scalar ratio. These are definitions of the existing Atlas status contract, not a new claim about unassessed literature. 

#### Native field: comparison_refs

Native pointer: /proofs/6/comparison_refs; canonical SHA-256: a8ea6921a245a2ba99dcb8aaf7b5ec5181288ea28c8116e82c7bc676962c4621

#### Native item 1

Native pointer: /proofs/6/comparison_refs/0; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 2

Native pointer: /proofs/6/comparison_refs/1; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: evidence_basis

Native pointer: /proofs/6/evidence_basis; canonical SHA-256: 46f58402184a9d56ab63bdeb88c6d69e5d38f27b890634b1772adff172da2801

retained_baseline_derivation

#### Native field: source_refs

Native pointer: /proofs/6/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/6/title; canonical SHA-256: 336d0ebff1d6dfa719b832f9eb07ca4dbb207686cf09b2f52a51e286debb6c9b

Canonical state and previously proved region publication

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: edb35168aef7b3bd15b5e8ab897ba72b807ad123250ea017ca93666f909dcd55

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: c5b4a087ea60ecd7f0ce5ac658ac26f6ae746a69d1a4ac5703c1b2ddf66fe3b9

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 149569bbc26cbea242c7d2c383a104ac84c9cf671c25c96cdfa3151d3e514c3a

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 7dc362bd2ec232f744946a1343beac9e90c65f7c3c16b235276f92132c540764

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 6c25379fda6da55a7f741ac0bdb980a5a25cd384ed9c4e7e00b64903e531d7a1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: b1edb5b715f24b7d603487b943ba2d651141174d2f05b8a98744d133cd7a2dc2

Native comparison predicate with original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 3463fbe7607634c3917f1ec97ad50dbdf3ec350e49940b6bcc85ecc311a21c9c

SO_ZO_E06cL__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: bfa764e809800152e2a95de9e5ceb91b5b743bcaef6d32af0ffa0d384885cfe3

Conditional accepted-baseline retention; external premises not recertified.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 9cafd9bef64911132434dc616bc51e63185d4b1cf2e1537ffa6bf012fa151fd5

All B,K; Rhat=a_BR_2(K); retained constrained localization transfer.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 9edece33cfbac61bada6807e1224f1bf4ea87bc81cc46a91784bf20bbdf76af7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: b1edb5b715f24b7d603487b943ba2d651141174d2f05b8a98744d133cd7a2dc2

Native comparison predicate with original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 101619bfbaa31e52ac3e1f1928fc9f373cdacdb0ec99ba50958cf0e2a47fcfc4

m_0≤m≤d, r_m>0, 0<ε≤ε_ZLr_m; maximize only over admissible integers.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 80babb135f537486642340e3741fdbe05be6e47fc468165faa477e37e39f58d6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: d1f58b650ca50fca6d3871c771d913e028c65460d4886722572076b5350e7634

SO_ZO_E06cL__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: ad365ff5cda2c951ff747cb4ec78953c9d7a84c48513e7ac38ee3ce956bff017

Distinct q2 identity; no transfer or merge.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 817f1ac02b3cf5d14425740fdd3d0a2d5f6a693c651160f8978483418c4db37b

Matching ellipsoid, A_B>1; deterministic q2.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: c55dc435510b11321d68f13b06b2a940c1c12ccf0e586f6d02ec094d370903b9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: e62e4fc604b40589a1fb1615f96ea16e1d38981f53efaa905147134281cbfb3d

SO_ZO_E06cL__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 56fd5232e1d63b8e0c0f7cfc52e8500749c1ef8f6eb2b3918214689fc5eaab69

Z is disjoint from the adopted positive lower window: r_m≤ρ and ε_Z<1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: c0f89055ac4df70103351c91840089d46d4c0ad53240c5e4b5977dbefe089eff

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: 3b82935387bf36964e8b641d18b3acc03efe8cb04af9ab1ad54b2c5b85fdc924

SO_ZO_E06cL__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: b44d7c5dd08d59b6f59c6ae95825d38ef43694fe67b90e0ce9e7c13a70dccef1

The zero-endpoint guard is outside this adopted comparison region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: d37b1fc91551b268169e083af18f2cc7e5b909a77a7753ba361138c441c34758

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: a83bf89100d8a6105fe70ad23922a38240a63eef4b20e32c3558b9382761c529

Preserve all source dimension and accuracy guards.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 4abab667faa5a061849ef5cec587fb26f82e107ab257bf3dcf34b5483c38c97a

Precision-independent lower saturation does not establish finite-query exact reconstruction; the upper cost retains logarithmic accuracy dependence.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 9a5e03541de6895f29acfc987c68421d862bdd15c004f682eddc529a70a9beb0

O(log²(ed)log(e+LR√d/ε))

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: feb0dedda3cd4ee5f52cea8ea60a8020007e469b165a9614ee82d57ed83ba31c

Ω(d²/log(ed))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: b5acfb54cafba5da601768bddcb1ee63dd29c6c68681efb54d3835516958ff72

Native logarithmic gap retained conditionally; other regions remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: bc83b13ad72b7de2c3530f2fc3e728c813c125088a7c3051c559df0280779bd5

O(d²log(ed)log(e+LR√d/ε))

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 8c24d97c4fb115f155dc8e95646696d4ac63e333fceb2276141dce4b928d5b7d

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 37e89ae5ceda2adb0441364e69fa2d57ecb769961e6b9ff845367ec299c3673b

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 2b0543a16bb3e5a116dc838098a044a69700b6e262db49e9092a3ae197388a16

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 72d7884fbdeea7db55f8dc4cbed4fba15fa2929e4493f95f96287f53c5f169ec

a_BR_2(K)≥R; affine-invariant b6 is no worse up to universal constants.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 8ddf9ae3988394c6f34c015449d72718bad98d0e553b0e872c0025b1a6df6957

All B,K; Rhat=a_BR_2(K).

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: ed0a0e94328f0b5afb51852f40314aaf13d8305f697d5132308165d7d24a324e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 7a0a7f5ca975573a0b26ab380d4a409aa8d5a5e81107ce42c7ce7b7236e3b961

On the applicable B_2 subcase its optimized retained scale is dA_B², covered by b5. Other ellipsoids fail the native B=B_q condition.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: b487970aa1a009b70c411b29209c6942962c247290101b0d3ddd3e902034943f

B=B_q, d≥3; public ℓ_s prox with known range Θ_s.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 88a99857e1f522cb5435426be748dab83ced42f105c1745115714704a0faec39

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: b86eb3a4d716cb7efc2cb6995ce62d9ce4df7bee98724db08973ee1494a86bf3

a_BR_2(K)≥R, so this conversion cannot improve b5.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 677ffa90bdc86e59b23608d1cc6356c42aa3d4970de1db5196c0c732d4dfe636

All B,K; Euclidean prox, L_2=a_BL.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: 54a1b58fb872422b81da77fa20136daa3a3e02a1e860b40ec4548f53edff325a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: d87c039c7117adba0214e0aa6067b9420575317880b529d4bc069262d93a2cc8

Native ellipsoidal comparison and original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: a50a3b19e057ea8666735da06aee519412a76c03e228c1ae523f1600191602f6

m_0≤m≤d, r_m>0, 0<ε≤ε_ZLr_m; admissible-integer maximum.

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: 463c32743cba5809e83f96f3cdc9e6600e50bf921b9e0cc5bcba684c146fc1e9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: 4b69bec2ba778e83f5d62b14341ea213b348bc27c5f9f882f1ff86f8380732a9

Native comparison with original guard; retain inside the minimum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: d6397c3d74ea4928760aba95ad19f5760e62d8231cc62b1cf3d08d50744297de

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs/1; canonical SHA-256: 35d31d90801dd65b1e9e1658ed7d97bf28b7829088e44457c220c190834be5c0

ZO_PROOF_PAIRED_UPPER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 8e3df867e9deb0af8cb7be0501b3dd48dd3b34273752f7300916b5861cbc74fc

Conditional retained two-point upper branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: f4af8248a9001cc322c513322302ceb6a7d73ae9ff9538b45bed99d3af5e7af3

Matching ellipsoid K=c+RB; A_B>1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: 0afccedbf593c4ac6572fad5412f59dbbfa21fcefeee66fc773973d23f736efe

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: 4b69bec2ba778e83f5d62b14341ea213b348bc27c5f9f882f1ff86f8380732a9

Native comparison with original guard; retain inside the minimum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: 7c07f23f2e8d3d5465ac43d84d6a5ee5cdc9847ffec26d31763abc5a1c616d81

Conditional retained localization branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: f4af8248a9001cc322c513322302ceb6a7d73ae9ff9538b45bed99d3af5e7af3

Matching ellipsoid K=c+RB; A_B>1.

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/bound_uses/6; canonical SHA-256: 55be14db1ce557984a6925d260a29d0714ab2ce06153ebd39da4a7f52c6e7c35

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/reason; canonical SHA-256: 12db5694bf56c21875c0ff358dead3a9f92e6b7dc9845162ac728ffd240ec28c

The adopted nontrivial source window has ε<Lρ.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/1/bound_uses/7; canonical SHA-256: cce564b2a5179aa773d70b35fd2242efd601cff74cf2f6a35956e67ceb090530

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/reason; canonical SHA-256: c7fcf15c08594a03768f08619ecd1879ba3f9784e10eeb41a19ac32f088f9d4b

Outside this adopted nontrivial region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: e778807e771d1fa74a67422f3000eca259a906960082388d72f3dac8df767bb7

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: d78bea4e7a9bed5b8ec36aa56e01dde76584c7079e36e99cc95a2534f83c9f6e

Lower saturation has asymptotic scale A_B²≈d.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 595f9b90472ea4c908a90e733c7066bf347d61cb201f3fcbc098f28f57b5a4e6

The upper crossover instead solves A_B²≈d log(ed)log(e+A_B); this is not an exact activation threshold.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 95102c00e525358114cca9b5bea654c6d0d08150d8ca69950abc8da48d75adb0

A_B≤1 is covered by the new endpoint, outside the adopted nontrivial source window.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: b3b520fd51f18666f50d7c61a036ce88943bc42b8492b9745f1d92d0cca526b7

Retain native O(log²(ed)log(e+A_B)).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: ded3a4df66e2559098f19f6f9acddaa7d2a147a1065900122a428f72f673c814

Ω(d min{d,A_B²}/log(e min{d,A_B²}))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: e1276bd548be8e0acb27bf3177431d18c31d11e8564a29c18afed07db1e3c56c

Native logarithmic gap retained; broader geometry refinements remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: e45bcf5b7b74b4615daa334f5280884ea0f1e7adfe81f4040fa5e56557dea7f2

O(min{dA_B²,d²log(ed)log(e+A_B)})

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 36d53c379a689cec920e744bb4555b217237fde9f8a7e2f2f4e57c4de8091f16

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: b37ff06b92e4cef977c32b884babcfbecc1391b32c1893e7fe95c5eec3b41d95

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: b82a971b6649f1fee2a2a2632fe110f3a406ab6aec65e27208f64e64858bb6d8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 590c65b429d5e645fa38c2179c2449664dbf8a47e03deed08f58cbc5e60e01f7

Fixed-c localization is O_c(d²log²(ed)); recorded b2 is O_c(d²log(ed)).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 8ddf9ae3988394c6f34c015449d72718bad98d0e553b0e872c0025b1a6df6957

All B,K; Rhat=a_BR_2(K).

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 610bbda2c603658ef4927f250aa770b5737cc9965b65f7104991a034a1a8fc9c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: f217ea852a563c16e27126a0a8523e827172e472d8d2f6b96932118405fb9442

Native fixed-c ℓ1 slice and original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 23e2b93a0d0fe9fc290f8081cba400bebb5dcdd84e2a888909f36271edfe5ffd

B=B_q, d≥3; public 1-strongly-convex ℓ_s prox with known Θ_s.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: 2954e65a4bdd9822ee03cf85bb3d406bdd9c785d9270d895c5d59decca9cca25

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 0a6c76464836ae781507e9ef928ddeffc004ddc1d532a9ef7b2ccd3c6c3e2e1a

For B_1, a_B=√d and R_2=R; its O_c(d³) estimate is worse than b2.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 677ffa90bdc86e59b23608d1cc6356c42aa3d4970de1db5196c0c732d4dfe636

All B,K; Euclidean prox, L_2=a_BL.

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: 11ca9bfe0a08aac592bc4e148bbe3fb1a6ada468dfe9faded48f2f8fdc84351e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: 2b4a71d69ff766cc88ae89ccd1fd1e3bf3e7a8ea325be0f4fefb0487bb2e435e

Native fixed-c slice with the original admissible-integer maximum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 151b249f2cc7209feccab45294547850bae556a6ace570d286ef3f57c5690835

m_0≤m≤d, r_m>0, ε≤ε_ZLr_m.

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: 64e02c8bdc1716696699c0672cb18462979e3f32d84a03de060cb5ee5732f039

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 9d74cf7e269a75ca5a8ffc07558da12f4f7544f8f6371acbf06f9d79f3484dd0

The high-dimensional ℓ1 body is not ellipsoidal.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/2/bound_uses/5; canonical SHA-256: 6b907b6ca34a411e19833a3ac4c7de1efd74fe785c0048df046fc88d52f39f7d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/reason; canonical SHA-256: 9d74cf7e269a75ca5a8ffc07558da12f4f7544f8f6371acbf06f9d79f3484dd0

The high-dimensional ℓ1 body is not ellipsoidal.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 7

Native pointer: /joint_analysis/comparisons/2/bound_uses/6; canonical SHA-256: 4bd86f113d1c677df2d352cfc2e0f63ab75c604861e572b6a1713bac634c372a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/reason; canonical SHA-256: 1917d3a6c9cac505c19bcf9881a2907e42bf73d5c2942d169081df0e849a002d

The adopted source window has ε<Lρ.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/2/bound_uses/7; canonical SHA-256: def53d72079e7473ccf0e36931ff233a111765396298faca79cfebf18ba40070

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/reason; canonical SHA-256: 73954283a7e2268ffd96d404b0bb764b519ced276f5cc7c3bd6e81874d597003

Outside this adopted slice.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 7980036e59d13bf38d039eecdc50254e2a1384e73e0798ddfb08f87260798002

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: ebc4ca10d8cff04a281a3eb3c5b07b85f777056053d9b6c04c37f6fdbcd64a1c

c is fixed locally and may enter hidden constants.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 94ae9021749a8db37a734e1155abae76ae48f96c1323ecbebf4f47a8b3231df1

Do not substitute a varying expression for c or infer a uniform joint-accuracy theorem.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/boundary_checks/2; canonical SHA-256: 28f2a02d9aa6eb09ecfbf64be41e86e3f4fe0ec07ffada906a086518a881f335

Retain d≥max{3,m_0} and all source guards.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: fd2079a3096d5abb9bdf54cc5c80262e7b58bac10d524846455474beff760be9

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/constant_dependencies/0; canonical SHA-256: 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d

c

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: fd2079a3096d5abb9bdf54cc5c80262e7b58bac10d524846455474beff760be9

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/fixed_parameters/0; canonical SHA-256: 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d

c

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: b2e9217d2e7aa4235b70e039ab371ae977b51b3923e128bddd3012e8d91c6563

O_c(d log(ed))

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 14f5da8af882bab21f491b3d1542445aab83b51915ceda0c623b676bcd4d8697

Ω_c(d)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 5a5f04795c35a0a8fda8325f220bfb6e666cd89078a3a2da0c07550285d5627c

Native polynomial gap on this slice; the joint accuracy complement is unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 9c454e344a1bfa67bf880314262dbc94129d1d7834801faff09f2f9e89567796

ε=cLR/√d, fixed 0<c≤ε_Z

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: 871f25c61485bb79caa090fef277f45f3912dc0c0c4d6689983de2eb033ecc4e

O_c(d²log(ed))

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 1a2aadf50b3828d1d4e7071e9a5762be7622758b7a2671638e1a318584aa1552

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 1d79a8edf705f2937e1cf23195e82927b33d556ce355387a4ab593768f5bbd2b

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: 092472081e34ee24f457569be673d2bebbfaf6514079abe91898afb4467dd16f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 41497e49974ed35c8eb39dbe5d293652264c3b608ca0b3aaaed1f4e3c9347fca

Localization is O_c(d²log²(ed)), worse than recorded b3.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 8ddf9ae3988394c6f34c015449d72718bad98d0e553b0e872c0025b1a6df6957

All B,K; Rhat=a_BR_2(K).

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: d77648171ff2c4499c05131c860348420347fbcd589bdc4289c4685a18a52358

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: af1a5b236dcbbe4b3330f697cf86e38ce4f66a0a7d58ace0759bcf653a93dd21

On the cube its best retained prox scale is d²(LR/ε)², already supplied by b3.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: b497ae2364fecdd3a34b4f9e7c464b0ad551adda517a144861a1a0780316f309

B=B_q, d≥3; public ℓ_s prox with known Θ_s.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 3bd0b91bb4f75a996cf39db4312f6ba596773c5782f5263cd177b5fbe6ec14b2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 78a2ea64ce53f5cecdfc0cea52adcbcc40e5f1e314407f614eafcaaff627bb71

Native fixed-c cube slice and original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 677ffa90bdc86e59b23608d1cc6356c42aa3d4970de1db5196c0c732d4dfe636

All B,K; Euclidean prox, L_2=a_BL.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 5bb2ce1e1fa9f4646f64adb5dd16a543bcf8d7b973094f1cb2e182a23311d9da

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: 2929ae4baac4726f86a06ce0c46bd4e2703449eecdab49f1af829af540bfb3f7

Native fixed-c slice with original admissible-integer maximum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 151b249f2cc7209feccab45294547850bae556a6ace570d286ef3f57c5690835

m_0≤m≤d, r_m>0, ε≤ε_ZLr_m.

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: 1572abac21bef7208051475d3a040151e63a99f8a023f5937ba2642e8de9fac9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: 716a2f3396413ec0015b749ae63e421f0e28093690689e7456e6b2625292b56a

The adopted high-dimensional cube is not ellipsoidal.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/bound_uses/5; canonical SHA-256: b0204cd117ebd4d8ebf795c205ca29a33d122e9b156814db76f76166c271bde5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/reason; canonical SHA-256: 716a2f3396413ec0015b749ae63e421f0e28093690689e7456e6b2625292b56a

The adopted high-dimensional cube is not ellipsoidal.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 7

Native pointer: /joint_analysis/comparisons/3/bound_uses/6; canonical SHA-256: 55be14db1ce557984a6925d260a29d0714ab2ce06153ebd39da4a7f52c6e7c35

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/reason; canonical SHA-256: 12db5694bf56c21875c0ff358dead3a9f92e6b7dc9845162ac728ffd240ec28c

The adopted nontrivial source window has ε<Lρ.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/3/bound_uses/7; canonical SHA-256: cf2a2ac58f27c67c519002a4b5a81f2c22c5c1c1e4fe019dd970b7ea888c5c59

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/reason; canonical SHA-256: 04fce2c337b76961477c1bcd1e2ffebbe015dcca08d0ad3963400fa432108ede

Outside this adopted nontrivial slice.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: fef95c0620815cae43ab12f4a7a1680f60d56fd2676d359d6c6bc9f11c59ef9c

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: 9cffd20d2d5c0c6acb85330ddd66012b252386ad3d8c49690801a03f9dcce253

Keep c fixed with 0<c≤c_*; constants may depend on c.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: e6f1fc90df4ead0027730361090066464428c70d52526e467c8e95bbe57a297d

Any overlap with the high-accuracy comparison retains both original theorem guards; it does not make O_c uniform in ε.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: fd2079a3096d5abb9bdf54cc5c80262e7b58bac10d524846455474beff760be9

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/0; canonical SHA-256: 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d

c

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: fd2079a3096d5abb9bdf54cc5c80262e7b58bac10d524846455474beff760be9

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/0; canonical SHA-256: 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d

c

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: dcbdf3b13781daddd6c9a07ea313664a7b314dc779caeb397a029adf5d962500

O_c(d)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 14f5da8af882bab21f491b3d1542445aab83b51915ceda0c623b676bcd4d8697

Ω_c(d)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 27ee20d56ee1b1b8c8eb759a83cdf22f976aa9d2aec5664cdb610a1c91d8b5ce

Native polynomial gap on this fixed-c slice; other accuracy regions remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 62b449dbc13ed6b7bb2fbdfffb22ccc371fba1f0a7bc724657906774a3c8cbee

ε=cLR, fixed 0<c≤c_*

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: a1140e5ec2f68bba2b31bbdb0bb583057108ed570279cfde962555b6672a7e10

O_c(d²)

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: 2c8e6e8110b67ef60544cf984b50de5adf5b2bb9035205b71dd4cff07b067d5c

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: a70b71eda4153733f064699a404a501be31424d081e8d23d69e76fc7c86ef030

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: a041ea37b0c3ecf714fe76a09a5c7dbc682386e3e9e7ba9d92b3017a95b02ace

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: 013df455f4eb22c3aa8793d037ab2d6c2b09b6bcdbfa7487655961a8f13ed9ef

Native high-accuracy cube region and original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 8ddf9ae3988394c6f34c015449d72718bad98d0e553b0e872c0025b1a6df6957

All B,K; Rhat=a_BR_2(K).

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: c75cf132ffdc5058da2407004fc57a196d135f2f7b450fbc0cac1629384a75b4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: e95815f6205c3cacba8a3b9023eaf13eb3c46069e94dd05465f34d45ae50b318

The retained cube estimate d²(LR/ε)² is asymptotically larger than localization on this small-error region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: b497ae2364fecdd3a34b4f9e7c464b0ad551adda517a144861a1a0780316f309

B=B_q, d≥3; public ℓ_s prox with known Θ_s.

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: 9fe15bba2f3e899e327f74570216abbad6564dfe166a7f689c4b4feda03578d1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: c2004c6ba7dd6855e7dba779db0784144445b88245112b8ecb74f61d0910cc02

Its cube estimate d²(LR/ε)² is asymptotically larger than localization here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: 677ffa90bdc86e59b23608d1cc6356c42aa3d4970de1db5196c0c732d4dfe636

All B,K; Euclidean prox, L_2=a_BL.

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/bound_uses/3; canonical SHA-256: 18a2b926694ff441644c68b4abd8d45f508b4e1d5a781f3fe29be2d9c9f42b97

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/adopted_region; canonical SHA-256: 9ac0e1e801709a007b7903c43eaf7365482510017b8f64267e1ecbc4d8c50a4f

Native region with original admissible-integer maximum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/validity_region; canonical SHA-256: 151b249f2cc7209feccab45294547850bae556a6ace570d286ef3f57c5690835

m_0≤m≤d, r_m>0, ε≤ε_ZLr_m.

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/bound_uses/4; canonical SHA-256: 1572abac21bef7208051475d3a040151e63a99f8a023f5937ba2642e8de9fac9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/reason; canonical SHA-256: 716a2f3396413ec0015b749ae63e421f0e28093690689e7456e6b2625292b56a

The adopted high-dimensional cube is not ellipsoidal.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/4/bound_uses/5; canonical SHA-256: b0204cd117ebd4d8ebf795c205ca29a33d122e9b156814db76f76166c271bde5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/reason; canonical SHA-256: 716a2f3396413ec0015b749ae63e421f0e28093690689e7456e6b2625292b56a

The adopted high-dimensional cube is not ellipsoidal.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 7

Native pointer: /joint_analysis/comparisons/4/bound_uses/6; canonical SHA-256: 872e54ac303ceb7c942c5b1203fe9aee8df815b65b77535760e7ec85a50d9f14

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/reason; canonical SHA-256: 60dec7cd9df1d9d46b4dfaa2de81fc3babdf1ea18807dea2b3a81483a82b8f9b

r_m≤ρ and ε_Z<1 separate Z from the adopted source window.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/4/bound_uses/7; canonical SHA-256: cce564b2a5179aa773d70b35fd2242efd601cff74cf2f6a35956e67ceb090530

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/reason; canonical SHA-256: c7fcf15c08594a03768f08619ecd1879ba3f9784e10eeb41a19ac32f088f9d4b

Outside this adopted nontrivial region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: c76f1a0aec399322a3e1f1244099111fff0bbe307c89530f2da17d4011d31b8d

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: e0633ac8da714cd58f8bdc2ba16b9ba5fe9fd10d0d76f933ef993ea754f38384

Keep all original source guards and universal thresholds.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/boundary_checks/1; canonical SHA-256: 5579055a222d99c424b32ae6c960bd4a43807fa1e28f66b3d7714f6f8c81b4f4

Precision-independent lower saturation does not certify finite-query exact reconstruction.

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/boundary_checks/2; canonical SHA-256: f9d801bee09418ccaa7f69e9639d58453c10db7a021c4111aa2002f5723d9906

No fixed-c slice statement is substituted into a varying-accuracy bound.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: 9a5e03541de6895f29acfc987c68421d862bdd15c004f682eddc529a70a9beb0

O(log²(ed)log(e+LR√d/ε))

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: feb0dedda3cd4ee5f52cea8ea60a8020007e469b165a9614ee82d57ed83ba31c

Ω(d²/log(ed))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: 53d50fac9792a123524eb234e5d9e857cc0b78f30c959d88830a59871cc6c5c2

Native logarithmic gap retained; remaining accuracy and geometry regions are unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: bc83b13ad72b7de2c3530f2fc3e728c813c125088a7c3051c559df0280779bd5

O(d²log(ed)log(e+LR√d/ε))

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: c5a35c992233b98c32543db7ca54022190760bde8ffe77c2ec3dceff47ab1f38

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: 10d5068897dff07f4aaa322cd293af4571f886fa702ffe4123974ce73a27e9c0

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: c3a258faf247a9312d6589d1f1f5747cee7870db4ce5427daa4b350c93ab487e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: 3463fbe7607634c3917f1ec97ad50dbdf3ec350e49940b6bcc85ecc311a21c9c

SO_ZO_E06cL__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: 3efa30015f124631c7172e46648f5bf2c8f27127f1bbba876ea77595719b4eb1

Its positive upper estimate is superseded by zero calls on Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: 21182f6ea2d30f63ba75be8eac7ad88fc5fa3ac1451958791520395d32001edf

All B,K; retained localization transfer.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: ee8509857a59dccae97876c9b6ffe8b75fb4b80597365a832eb1247f2600463f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: 017663b113fafa50b91ab77f8715cca538f4d51e4db9586b71996af266560977

r_m≤ρ and ε_Z≤1/√8<1 make the source window disjoint from Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: 151b249f2cc7209feccab45294547850bae556a6ace570d286ef3f57c5690835

m_0≤m≤d, r_m>0, ε≤ε_ZLr_m.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: 0f586c8519246e7ba0ee37415ba82e8094109a83ebac48f02bbd762cd8a743a7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: d1f58b650ca50fca6d3871c771d913e028c65460d4886722572076b5350e7634

SO_ZO_E06cL__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: 0aecda2c4cc618ff46dd162c93955171dcf91db02b4a84e374c715c0420bf50d

Separate q2 identity; no transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: b8943b5d8f982801c3678505d4bda728676bad2c958363b2c10d537125d85d4c

Matching ellipsoid, A_B>1; q2.

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/bound_uses/3; canonical SHA-256: bbf3d7026e8c5625e183f895dcb47788d1d0eef0d9278fd77a8250fe3260ecc2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/bound_id; canonical SHA-256: e62e4fc604b40589a1fb1615f96ea16e1d38981f53efaa905147134281cbfb3d

SO_ZO_E06cL__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/reason; canonical SHA-256: 506aa74189375b9ac386663e45a2bef9e224ea0d285ed97885624d5448112367

Return c_K; gap≤Lρ with zero calls.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 5

Native pointer: /joint_analysis/comparisons/5/bound_uses/4; canonical SHA-256: 498ce31dc997ed4f1c764fda67e6ddf8fae5df15becac8c374ac15714b395591

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/bound_id; canonical SHA-256: 3b82935387bf36964e8b641d18b3acc03efe8cb04af9ab1ad54b2c5b85fdc924

SO_ZO_E06cL__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/reason; canonical SHA-256: 64a6ab15c6bc5268e643e197d8ce404cf28205bc78c2e61fc5e7405b3ec9be25

The charged call budget is nonnegative.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: 552b9f73d332a35ec5b9b295044b03bc7d520576d93b906f5b48cfeb8da2cd46

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: 7417ea1ff959726c312a30d2087735604ffccee190c834e657a30a0fd9b9c389

Equality ε=Lρ is included for ρ>0.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/boundary_checks/1; canonical SHA-256: 1f4258f7b041d2a89c7b08f19027453692a4257b4faab824e561f51ac44bda4a

For ρ=0 the feasible set is a singleton and all ε>0 have zero cost.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/boundary_checks/2; canonical SHA-256: cfa652ad3931918b78b2ffb747d3ecbeeb6761564e21a6006aa53dc4ff0236d7

Below Lρ, the opposing affine pair proves only nontriviality, not a main-rate lower bound.

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/boundary_checks/3; canonical SHA-256: 5fc916f3e50b3633080bc27c8505f0858ed41b8774430ba949307e1b20265d04

2610.00345v1 K.3, characters 226890–233390, defines ε_Z≤1/√8.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: 394db0f20e65821b7005ea06d8b181f49203a8099c7813485869fbd2308f0201

Not applicable: exact zero cost.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: 7115dbfebb87564046d0b500c2c266ab04dbe48b4858433b80c8c832860d417f

No gap on Z; the positive-cost complement is only partly assessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native item 7

Native pointer: /joint_analysis/comparisons/6; canonical SHA-256: 23252e7742dbd410996bb7168ecfd1c6cf47c42a1684b4780eb4798a7d30e7a8

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/6/bound_uses; canonical SHA-256: 1082cbb76f8debd246fcdcfed0732cf198b55ecf391158e982f13916af35c7d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0; canonical SHA-256: cd69e8b12870dcc54da99e7d0ffc382583b8555bec026fa93ff6c87f0520bc7e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/reason; canonical SHA-256: e257638519d726914b602049b368936d7d93d25b832566b30ce5f3249d4f3830

Zero calls supersede the positive upper estimate on Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/validity_region; canonical SHA-256: 21182f6ea2d30f63ba75be8eac7ad88fc5fa3ac1451958791520395d32001edf

All B,K; retained localization transfer.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/1; canonical SHA-256: 45051cf9d52798170d29629174e7dbcd4d77bb6e61cd6e9e92cc642d441eb307

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/reason; canonical SHA-256: adaaa69e59c1ac18479a1efbf8ca9a789ba0fdcb5d1635f932e8b0d87b5273ba

Where applicable, its positive upper estimate is superseded by zero calls.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/validity_region; canonical SHA-256: 7d74c54a4a319b79aad075ca4d3383885253c0dbc6a872038f2f04f2620fc1d0

B=B_q, d≥3; known public ℓ_s prox.

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/bound_uses/2; canonical SHA-256: f4f48f1fadb8186c5697e06f14f8e91e9aac6700556342b72aa5afbcaeb5f8b7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/reason; canonical SHA-256: 24f782a0eaa4342e459920613b87abf8fcfa06498fdc320ab5b79682b70be6b2

Zero calls supersede the positive upper estimate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/validity_region; canonical SHA-256: b570add08de74bfb54022ad8b247ed7ac022b9b77b048d7e3ac65d93e669afd7

All B,K; retained Euclidean two-point upper.

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/bound_uses/3; canonical SHA-256: ffcd287a33eae98cdaf57b84703dd6f8462e7a8177b74a7863dbdd2a30d8232d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/reason; canonical SHA-256: 017663b113fafa50b91ab77f8715cca538f4d51e4db9586b71996af266560977

r_m≤ρ and ε_Z≤1/√8<1 make the source window disjoint from Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/validity_region; canonical SHA-256: 151b249f2cc7209feccab45294547850bae556a6ace570d286ef3f57c5690835

m_0≤m≤d, r_m>0, ε≤ε_ZLr_m.

#### Native item 5

Native pointer: /joint_analysis/comparisons/6/bound_uses/4; canonical SHA-256: 8d54f234bb6e8ad31e1a8f66dfcedd88083f473e6c6bd1f9848a7127972d3112

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/reason; canonical SHA-256: 9fe99be676608ad94faf9b76e23aea9b81004d0b3091d88e50ce831dc6b47e4a

On matching ellipsoids Z has A_B≤1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/6/bound_uses/5; canonical SHA-256: 5c5ea7273b28ad3b979a6e597da67933608b1e27d32c217912c3e25eec8660e3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/reason; canonical SHA-256: 9fe99be676608ad94faf9b76e23aea9b81004d0b3091d88e50ce831dc6b47e4a

On matching ellipsoids Z has A_B≤1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 7

Native pointer: /joint_analysis/comparisons/6/bound_uses/6; canonical SHA-256: fee5f6d3dfc6756530117e14ca1717f1cff7f2efae278c25f5ebe12dab2f5ae3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/reason; canonical SHA-256: 5a40ed40497ce66d958c0bd86c0d57cc08f18b911dcf5e6c2d5af561855c5eb1

The deterministic center algorithm succeeds with probability one and uses zero calls.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/6/bound_uses/7; canonical SHA-256: d0514e63bf044bdc28d1617719136a06970480e18681fc230443ac8b6c7c36e6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/reason; canonical SHA-256: 7ff29e6c2a43d607760ee6513f8ddab014711494f9f30acab6e2874dfabbfd1d

The fixed-path call budget is nonnegative.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/7/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/6/boundary_checks; canonical SHA-256: 409d698c722ed6163dd8bb1d3b6e9a6a5f475581d20936c8f5069de1d8326338

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/boundary_checks/0; canonical SHA-256: 05216749f3146bd5c427d388889800e11b53cff47f5bc4729c630b5b568aa946

Equality ε=Lρ is included.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/boundary_checks/1; canonical SHA-256: dec1f1cd2bc3ac2992fb374fa1b75d86d0cde3842c8576df8d0d834918c31dd9

Singleton K has zero cost throughout ε>0.

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/boundary_checks/2; canonical SHA-256: 363804c5e7a67631ced3b1b1a15f018bca3db3bd466d48f940108f0da38b2b47

For ρ>0 and ε<Lρ, a zero-call output law has success at most 1/2 on one of two opposing affine objectives, below the required 2/3.

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/boundary_checks/3; canonical SHA-256: 518fd025a9b331d894c2bd0433ddab072084fedc3a4f092c1c3bda7f717a6cd9

The positive lower-bound source windows are disjoint from Z.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/6/comparison_id; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/6/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/6/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/6/gap; canonical SHA-256: 394db0f20e65821b7005ea06d8b181f49203a8099c7813485869fbd2308f0201

Not applicable: exact zero cost.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/6/lower_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/6/remaining_gap; canonical SHA-256: 7115dbfebb87564046d0b500c2c266ab04dbe48b4858433b80c8c832860d417f

No gap on Z; the positive-cost complement is only partly assessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/6/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/6/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/6/upper_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 8ea4bde4819487a774f3b81c261ea959c6f112a8e5dc5aa135421d5859d3fb0f

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: f53ed3a7ad6a3b7918e94e77e50e39daeba8a5959e1f58adedb5c4448030f71c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 761df97af49117b7076f1fe7f5aec73b93c2da679ca26e4fed90383f12b846ba

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: c217c43a05e328dc38c22e59f500245b6cbe31264f74aa596d751b40023d9b97

zero-endpoint

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: a8ea6921a245a2ba99dcb8aaf7b5ec5181288ea28c8116e82c7bc676962c4621

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 37e061736cb711c56f86110470f69a030f8f78f34b97452744ad194f614214b1

Exact zero cost; the two view/quantity fibers remain separate.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 87be437e4d8e8c0a1668b6bba3e31184088f9902c713c2c222340799a43b50fb

Z, separately in each registered q1 view.

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 67aa351cb6ee3fa2944866ced1a931f558f0daa8ac3a5d4bfdbd232a5034ad0e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 377e1cefae4f2a57400e1e013212249579ea89d84470f98731d63804f804fa72

retained-det-c1

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: e04b768e78dceb8a470bf05e02937c00e17c02051e2b8c10ed9d555ac0d84084

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: e4b5647d8b226a162d649c5b351ac040bd3eda77bfdef669c357cbab65d4b97f

Native bracket retained conditionally.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 6990e89d8c093f7986797756a43a911717997791b51e50dce2c3deeec81d514b

Deterministic q1; B=B_∞(0,1), K=B_∞(0,R), d≥d_0, 0<ε≤c_1LR/√d; retain source guards; subtract Z.

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

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 85fc7782cc82c3c1879e956c6ab1feda7c7e09d32c932dd1fb14e3732c778411

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: dff74ce4a99746c0d996eb5bec6017789adacd61cba78f22be07487f29cb5a73

retained-rand-c1

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 5595ae958132d137164fe0cd5dbaddaa271f923224a5dc609ae105638d0c4211

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: c2cc0736f6b07a4d6564270d845c03d0f802e9b30d79d8ae4f2fe17472012f8a

Source activation and envelope crossover are distinct.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 64cbb3af92873bb41861963d60e137ef70f6950a308cb3b67e0234c46d53f18c

Randomized q1; matching ellipsoid, d≥d_0, A_B≥C; retain source guards; subtract Z.

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

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: 2e9f60128947c88645849af25b171c3bfa26cbdeab7da76528652cb7b90c0e5e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: 41628200523569f9d8750eb1036a7df1617c082bc833ecbd82d56c0147bc8e79

retained-rand-c2

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 6595d5185c49cb433b51ad35784a2e0b1568f6262c57ccaa8943598849ab97c0

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: 12310e7cf2f51329358893caa5e4ea4af6971dd8669895c476148fe421cf3a22

Secondary fixed-c slice; constants may depend on c.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 6a8b34fc91a6b869f9807f29013e3c4f32b5a17364ed7f691240fa5e0339b79e

Randomized q1; B=B_1(0,1), K=B_1(0,R), fixed 0<c≤ε_Z, ε=cLR/√d, d≥max{3,m_0}; retain source guards; subtract earlier same-view cells.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: d7b992fe01684652f8079a4f233068c552e23ad9ed51a4e9d6644d98e3b22516

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: 81aa456a4ac522f15963d0ee465603e7c84f16fcd3b63200eb8a82e3f799e6eb

retained-rand-c4

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: ac42228087c861bf7b8a9ed6f028f9874a3c97d9a009b65404d66c5adc2e75f0

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: e4b5647d8b226a162d649c5b351ac040bd3eda77bfdef669c357cbab65d4b97f

Native bracket retained conditionally.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: 8f98904511cbfc6f1d7ccaa061add35bfbea20228d911904e4bccb07a967126c

Randomized q1; B=B_∞(0,1), K=B_∞(0,R), d≥d_0, 0<ε≤c_1LR/√d; retain source guards; subtract earlier same-view cells.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 6

Native pointer: /joint_analysis/domain_map/cells/5; canonical SHA-256: a16e7e87c0d45df2466fbfebb7f4fe4c1f00e5731551a6b6f4bf75fa49e2db01

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/5/cell_id; canonical SHA-256: 779f7b929b03c068a8ebe645ebda94097462b70a9e0a8098cf4df74e5036ea11

retained-rand-c3

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/5/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids; canonical SHA-256: 17bda35342cb4ec62b598f61baae03ca9e75c52625b72b95969167cf743ec255

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids/0; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/5/note; canonical SHA-256: 85f3c11330650936bbda0b93cec140b933992c10d43843744f7f9de8a86f37c7

Secondary fixed-c slice; its original comparison remains available on overlaps.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/5/predicate; canonical SHA-256: e0611d8e0a7094928b283c55458ed807e44b5294b8761d4c334e34119d034431

Randomized q1; B=B_∞(0,1), K=B_∞(0,R), fixed 0<c≤c_*, ε=cLR, d≥d_0; retain source guards; subtract earlier same-view cells.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/5/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/5/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/5/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 7

Native pointer: /joint_analysis/domain_map/cells/6; canonical SHA-256: 40d4cdf005399afab873083f883d0f079e25fbcdac6b2c3bd6b1e5f555f13724

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/6/cell_id; canonical SHA-256: 394e431a775aa5d3b64866a7227fc91b622fd686eadf02007931f06dab50bd9a

unassessed-complement

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/6/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/6/note; canonical SHA-256: c3ddab50c99f275bf85bc597087289c213a8451bb46efdff3feb43b036108d81

Includes nonmatching geometry, low-dimensional positive-cost branches, and accuracies outside documented windows or slices. Unassessed does not mean proved open.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/6/predicate; canonical SHA-256: 6e8f75e2ffcfb7ebf86df42131ac31dbae94944a783cd1a932e99b9f9ea1ac14

The primary q1 target outside all preceding cells.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/6/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/6/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/6/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 287ff32a99424f723c54320da6f25875bda8fb0d620cdb675cb616b0aec9a3ae

Split by view/q1 fiber. Assign Z first, then the listed old cells after subtracting earlier cells in the same fiber, then the complement. This priority construction is disjoint and exhaustive by set subtraction. It does not alter any native theorem guard or comparison domain.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: f585170ad9d926957272e4d1e057307457675a35c6513995ac45a2675acb1fa9

Exactly the unassessed-complement cell. The separately stored q2 quantity is not transferred into this synthesis.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: f219478e1a1fdb78c1536dc018c93422dead6f2a57a55bcec9002e68841af7d5

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 71f121310a06ed659d9718a8209c18b5b0a6a998afede26badf8037e0a39fd82

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 2bce5cfe27ed84cb82ffc4e83e66933aab95792442a2504e67ced02746de6d3e

The center gap is at most Lρ; query costs are nonnegative. Opposing affine objectives establish failure of zero queries below Lρ for success 2/3. This closes an endpoint, not the positive-cost main rate.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: a8ea6921a245a2ba99dcb8aaf7b5ec5181288ea28c8116e82c7bc676962c4621

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 67aea45085b728d392fd02a44d0e8ac51236dc036f43d1ef99b656827913908a

endpoint-zero

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 997c6c502f9b389426a249678915bd05c3ea57dbd90e6a213c0fd54349abf72a

Z: a missing exact endpoint bracket is filled.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: ccdf4c88a6fb756f2473e77460e154f78636fee11cf280852b6f42e3ba49d773

zero_query_endpoint

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: cf73dd6ab0b5872b058e942b0d6a9120ef1d8127aef6334cb4fdebbc5fc37737

C*det=C*rand=0 on Z.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 7ce3fcc1b1adcfc78ad3877dfced2944d55ba292048491acf63822aa5c60b671

No registered endpoint comparison; generic retained upper estimates are positive.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 48728d15d603110d21bdd8bd3a42aed07f2e6acb3e842b1b510766c86851c096

All five pre-existing brackets and every point outside Z.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 6de3d23b72ab0c41335ffbbc0a7b22e671b032986c5a759585cc088fe64239c9

For any ρ>0 take ε=Lρ and return c_K without querying. For ρ=0 return the sole feasible point.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 04354951f04f5e9770d1ac2220632a808f41cbbcaac1ca991888e68c2bf5567a

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 9d5efb28a738fafcf681762b7f7757ee748c6a207f83556232729db564308d31

Their native predicates already fix c. The annotation does not extend those slices, merge q2 or supply a new scientific inequality.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 1e70140c811b2472123a81216e4175d364c45716740992e2f6ad040ef6b4e59e

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/impact/1/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/impact/1/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 1bd567f1665e3b454393ddae62d2f7b5fe6cff14c69b9a44409f749bb1b520b8

joint-annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 13365766b189166dc490755ad10ad6fcb6f48eb13cbbccb532048dd0a01935b8

none mathematically

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 1408e531386ed2007e2ca3ce7cd01ba1cc12c78d8bdc16aa4e578a674287963d

The same formulas, guards and statuses, with explicit parameter roles, slices and residual-domain accounting.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: b110247219d542de476d0a2c6d8bd9e71b83e60e88650d25ca5345e8241db61d

Five retained native brackets without a resolved joint-domain annotation.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 182eeef3493f9d96f6d187d5313ba585453c86113a0569d03bf3b72fad83bf14

Every pre-existing scientific row, guard, rate and status.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 3abfb8570b58f33ba4ec64e88ee188d08de5e3c1f1594a07bdb68ccc87a42c02

The five existing comparison domains with original guards.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: bdae8e246ea9639390daea130cb24717aa29acc000784258beae36f422873449

The ℓ1 and cube rows retain fixed c and O_c/Ω_c constants.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: bd95f20b20c00c7fe254fa26ce2fe13c36aa6b6a46f2ccb32032dc31bbd80dda

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: d74c561910718775b35f999dc9969bff25400d7f5ee65eb5bf8bf172b91484dd

The read versions predate cutoff and reproduce retained evidence. The smooth-only quadratic route needs a further globally Lipschitz reduction and is not adopted.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 7ac9866301b2a5a6fa31e55e6c6015a53bfd139945ab925b04cf770d47a023b4

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/impact/2/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/impact/2/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/impact/2/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 6

Native pointer: /joint_analysis/impact/2/comparison_ids/5; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 7

Native pointer: /joint_analysis/impact/2/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 584ffb4babd6ea3c218549b6e73c4f766b1e75124d2256809618a6e1350ae311

named-route-check

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 740677a4a07032324273908b90af97aac47d471991d5a56747e12df2e5271cc2

Same main-rate lower envelope; its source activation constants are explicit in the candidate audit.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 9fd9ad2aad01e3ac9533cb841ef4a888ccf3047b4a7cf4e7fb909fbf7c5ef6d3

Retained recent nonsmooth lower envelope.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: f2c0c32145d8ee88ae7b213fede7e5b07d200864183871c007c155ac33986968

All retained main-rate brackets.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 3f5e8d1b75bbb78bdf5e1235d49b0e1c8547a38b2b5c3c38ff629f173a4d260a

2610.00345v1 Theorem 3.3/K.3 windows and the 2607.16558v2 Theorem 5 input.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 56dc80394eeee51dd8a549f9256be11e269394d02f28c7814be179046a524f44

K.3 defines ε_Z=√(a_Z/2), a_Z≤1/4; Theorem 3.3 at λ=0 reproduces the stored image-radius lower bound.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 8496dbb2081aeb81013efc4a9cf6a35aa2d7018c0bdc23241e8e43eee89e7ddf

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 82ad21831e5823d21add25baf8dbc12b0bbe0afc6c9339aedbb1202444ba4cfb

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 7ac9866301b2a5a6fa31e55e6c6015a53bfd139945ab925b04cf770d47a023b4

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/impact/3/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 6

Native pointer: /joint_analysis/impact/3/comparison_ids/5; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 7

Native pointer: /joint_analysis/impact/3/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 4400ec8a3b9113373ed0200553bd60fe06a5de3b35d1673dd1e7e01b5ade2e46

curated_feedback_SO_ZO_E06cL_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 8ac3b850aefa1115a150e653472c5f992cf22de042ffec1212c0c25096dc1d16

For each registered deterministic/randomized g1 q1 quantity: d∈N, d≥1; known compact centrally symmetric convex B with nonempty interior; known nonempty compact convex K; L>0, ε>0; globally convex L-Lipschitz objectives on R^d; unrestricted exact scalar queries, output in K, and the registered fixed-path budget. Geometry varies jointly and its dependence remains explicit. Native p,q,R are conditional ball coordinates. The historical R metadata about a global minimizer cannot override the fixed constrained contract; the new endpoint uses derived ρ. Deterministic q2 remains separate and untransferred. Write Z for K=c_K+ρB, ρ≥0, ε≥Lρ within this domain.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: 2b3a2803badd9459caa71d1be80c9f6039f7526e6483566987238a415f0cd5bd

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 27f13269515265b1342c5f746170f0138e34ac988e3697d1c69e363782cc4706

The exact previously adopted science is conditionally retained. Correct only open-cell closure-publication metadata to the current explicit unassessed convention; no bound, guard, comparison, scientific contract or summary changes. Grouped cross-ID opportunities remain unassessed pending work, without any adopted reduction. This is presentation restructuring, not a new theorem or blind research.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 7ac9866301b2a5a6fa31e55e6c6015a53bfd139945ab925b04cf770d47a023b4

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/impact/4/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/impact/4/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/impact/4/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 6

Native pointer: /joint_analysis/impact/4/comparison_ids/5; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 7

Native pointer: /joint_analysis/impact/4/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: ed65e644f9380ee8e946bfc20e6a2462315e1bc4b35029e62ab6d14fe68723bd

curated_feedback_SO_ZO_E06cL_20261116_42b1a1bbfb

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

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: 8ac3b850aefa1115a150e653472c5f992cf22de042ffec1212c0c25096dc1d16

For each registered deterministic/randomized g1 q1 quantity: d∈N, d≥1; known compact centrally symmetric convex B with nonempty interior; known nonempty compact convex K; L>0, ε>0; globally convex L-Lipschitz objectives on R^d; unrestricted exact scalar queries, output in K, and the registered fixed-path budget. Geometry varies jointly and its dependence remains explicit. Native p,q,R are conditional ball coordinates. The historical R metadata about a global minimizer cannot override the fixed constrained contract; the new endpoint uses derived ρ. Deterministic q2 remains separate and untransferred. Write Z for K=c_K+ρB, ρ≥0, ε≥Lρ within this domain.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 176c473f7d15902e5b0800aa40bd7fbb985fcb849500493a1aed221c8e0f9470

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: ebfd5b79d4099b8c4413bee3322daf4934ccbeca3157fd2ea0e4a6398f5e9333

Complete any desired broader literature search beyond the terminal exact-ID query; this is a supported local update, not exhaustive coverage.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 07bfc0847ea79a80fde426bbc94add0d321d556062cb0a9466e288b23d485b74

Assess 2610.00345v1 Appendix K.4 constant-distortion certificates and further image-radius refinements in other geometry/accuracy regions.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 92f73a35e5110867713a07f6115ace06d941b0b1b53c920762bb335bccc2c73c

Assemble low-dimensional positive-cost branches and the unassessed complement. The affine pair establishes only nontriviality below the matching-body threshold.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: b5873d05c45132dd91af49da8f0c6cd49f6ccfc2e14e888a394e734f8097ffc8

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E06cL__deterministic__b3 to SO_ZO_E06cL__deterministic__c1, SO_ZO_E06cL__deterministic__c2; no transfer is adopted by this metadata inventory.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 233cffeecba2b759215180ad8e60351e56516267865143c8806f24546388efc5

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 50a5c44c01e9c88236b5af962ea7d53d16d17ac046d208a592a02fa5a00ae00f

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 3463fbe7607634c3917f1ec97ad50dbdf3ec350e49940b6bcc85ecc311a21c9c

SO_ZO_E06cL__deterministic__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 87d28495d02917dcdc6a5463a612ede21119ca21f500b030822f9806ef31520a

Unchanged native claim and guards; no fresh recertification.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 48135db74000fdaf5f443b77680e2f4db060a4e8535562a3f844a4e53398fd2a

Frozen /bounds/0 and its original evidence/source dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: cacec765a24d4171d024d12ad6857763441318aa9764334467be1aec98800d91

Original constrained localization validity.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: ebe3e068a90033eb7bc7048c6a18d6b0ec6953a15137ddedeb4862a25d30009b

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 6ca3b0e8e89e178a2e9d03691aaab16642caa3ab5ceca470269f98c2cf78634b

Frozen /bounds/1 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 5638e777c4cdab300f65ee653a8977c963a9dedb2a65ecf059cf929f237093bf

Original admissible image-dimension and accuracy windows.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 5db21b31727bd260d4ec7be41b3f5040da35ea5b200b0b3f20354e8d258b8ba1

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: a2aadf6207b5186b850effbfa5d79eda2b3ea7519e9a71e93b5d6faf846ba8c4

Frozen /bounds/3 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 6b515870705506274bd619d92256f8828652284d6f74ab47cf5f2c5a2631e741

Original localization validity.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 65bfc2467aa17fcc1021f4cf21fd50f1116e6ad80927d6017e0ef5dfdfe842df

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 1b61307dfd1cac4d3cc2370d155a4f71dde64f2b012c2f7868795e171b8870fe

Frozen /bounds/4 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: d05b0b7dc6b8a3897591b5233afcc16d9932005d89bf08f393fee99a0a368cec

Original B_q, dimension and prox guards.

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: bc4bdecb75bfc799ccb1238496b1896b546f03d0f5f63fe85de3391a740a3702

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: d8ee906375e403584989a838e82a6215db2e604fc64ddc8cba10465d78be8a6a

Frozen /bounds/5 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 62429442f9324822993bd4d7ddd015fd5a225087aedcf81406e2ee9430378bd3

Original Euclidean conversion validity.

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: fb072e3397879241171e3711cc0199f7c1af67eb83fc0b44ebeea2a53032f2b0

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: ae47d47a7856ca13a2b1fdb40a8dfd9224b0936b41ec1afe0c86c09c905f006d

Frozen /bounds/6 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 5638e777c4cdab300f65ee653a8977c963a9dedb2a65ecf059cf929f237093bf

Original admissible image-dimension and accuracy windows.

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: eb116405bb8b65c92f23b875983bba520c405051f325639a7276fdd1073906db

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: d6397c3d74ea4928760aba95ad19f5760e62d8231cc62b1cf3d08d50744297de

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native item 2

Native pointer: /joint_analysis/provenance/6/proof_refs/1; canonical SHA-256: 35d31d90801dd65b1e9e1658ed7d97bf28b7829088e44457c220c190834be5c0

ZO_PROOF_PAIRED_UPPER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: 2da1c1a88697fd1330b04ef265b60ad408a0940e542c7762dc005ec56b2d86eb

Frozen /bounds/7 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 8

Native pointer: /joint_analysis/provenance/7; canonical SHA-256: 92aa64d151a4114885b8c24414bc488e7f724896ff4c2339ba93501331e288ab

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/7/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/7/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/7/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/7/proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/provenance/7/proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/7/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/7/source_locator; canonical SHA-256: c62994c25939867ec5e26143124f230dac5918f2fb4cd4525c44e78fa12fb977

Frozen /bounds/8 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/7/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/7/target_domain; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 9

Native pointer: /joint_analysis/provenance/8; canonical SHA-256: 05d565b3ea3635b3945b04f7fcc28e9c611ce798f2f690a7662a4eeacddd0878

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/8/bound_id; canonical SHA-256: e62e4fc604b40589a1fb1615f96ea16e1d38981f53efaa905147134281cbfb3d

SO_ZO_E06cL__deterministic__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/8/mapping; canonical SHA-256: d3d95785f570ec146e04944481f96a85598ed9dfa1cc381448e576e87252df83

Direct center algorithm; no oracle or quantity transfer.

#### Native field: origin

Native pointer: /joint_analysis/provenance/8/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/8/proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/provenance/8/proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/8/source_domain; canonical SHA-256: 2efc2daf450fa24b3c430b4fdb5fca461eb3b0a27fb364025ac336c9223492f8

Global Lipschitz constrained contract.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/8/source_locator; canonical SHA-256: 46e32ab1a600c2830c4b312dabb26933743776cf27f02ec93d4dc138d29d8ce1

Frozen contract/views/quantities hashes in endpoint-zero.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/8/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/8/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 10

Native pointer: /joint_analysis/provenance/9; canonical SHA-256: 4e6b277f6fa5dfedd94c0d796048dc329f19495d043d94c66a8eabde4223bdac

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/9/bound_id; canonical SHA-256: 3b82935387bf36964e8b641d18b3acc03efe8cb04af9ab1ad54b2c5b85fdc924

SO_ZO_E06cL__deterministic__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/9/mapping; canonical SHA-256: 4a83e5803ed0ea0ee405f78652892629a4a0ccb652759adb7d5f720e6c84ee9f

Budget nonnegativity.

#### Native field: origin

Native pointer: /joint_analysis/provenance/9/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/9/proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/provenance/9/proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/9/source_domain; canonical SHA-256: 2952b7b5ce38f388e3d2447adf3935fbf7c9759e9435d4d803df110c26abcd40

Nonnegative charged call budgets.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/9/source_locator; canonical SHA-256: 3ccfc4dd7e2ee5fb196c28af90d1a85cc19b5d06a71b81b982ee8ae3624a77c3

Frozen quantity and resource definitions.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/9/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/9/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 11

Native pointer: /joint_analysis/provenance/10; canonical SHA-256: 3e3ee72256c35220e3dd0b454424154b7f7eaa2d34242e142d4935929475cbf6

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/10/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/10/mapping; canonical SHA-256: 8acab4617a9863764a3b110ef85b40c6386d756e186c8804ac13c0ca09652294

Deterministic center algorithm meets randomized g1 with probability one.

#### Native field: origin

Native pointer: /joint_analysis/provenance/10/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/10/proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/provenance/10/proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/10/source_domain; canonical SHA-256: 2efc2daf450fa24b3c430b4fdb5fca461eb3b0a27fb364025ac336c9223492f8

Global Lipschitz constrained contract.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/10/source_locator; canonical SHA-256: 46e32ab1a600c2830c4b312dabb26933743776cf27f02ec93d4dc138d29d8ce1

Frozen contract/views/quantities hashes in endpoint-zero.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/10/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/10/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 12

Native pointer: /joint_analysis/provenance/11; canonical SHA-256: 1749726df0a25f6938abff3319d7225d72772805589cb5b0ccd891108c7f8f34

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/11/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: mapping

Native pointer: /joint_analysis/provenance/11/mapping; canonical SHA-256: 4a83e5803ed0ea0ee405f78652892629a4a0ccb652759adb7d5f720e6c84ee9f

Budget nonnegativity.

#### Native field: origin

Native pointer: /joint_analysis/provenance/11/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/11/proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/provenance/11/proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/11/source_domain; canonical SHA-256: f0e6a7ccfa32bc96ad9314486b437e66a251647064533430aa98429858f1c82a

Nonnegative fixed-path call budgets.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/11/source_locator; canonical SHA-256: 3ccfc4dd7e2ee5fb196c28af90d1a85cc19b5d06a71b81b982ee8ae3624a77c3

Frozen quantity and resource definitions.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/11/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/11/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 650ed74abc1e61ac3662b413c3210e046e9def16b9957388f6bc7f1f98a02c58

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 5258d1aada2345a64beea83bbd03d3c899f298824b51ab8354907ccf91462e43

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 2a7bf37a557c29bce5ca90118ff0bc6e63784f4f782a2d1554039dd2a4370650

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: abb6cf587973e4b85068b31e20d77b516f64ba7348bdff9bc9fd010c1e08d19d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 3c0fef27e7705ea9dc20997f75f0474ca7df6f780f8adb867dca12723a391486

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 3463fbe7607634c3917f1ec97ad50dbdf3ec350e49940b6bcc85ecc311a21c9c

SO_ZO_E06cL__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: e62e4fc604b40589a1fb1615f96ea16e1d38981f53efaa905147134281cbfb3d

SO_ZO_E06cL__deterministic__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: 3b82935387bf36964e8b641d18b3acc03efe8cb04af9ab1ad54b2c5b85fdc924

SO_ZO_E06cL__deterministic__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: e04b768e78dceb8a470bf05e02937c00e17c02051e2b8c10ed9d555ac0d84084

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 7977aaad05402497a0ba67383d64b8f7e0108da535cdaad2a7ba9b6e0a06f52e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 3c0fef27e7705ea9dc20997f75f0474ca7df6f780f8adb867dca12723a391486

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 3463fbe7607634c3917f1ec97ad50dbdf3ec350e49940b6bcc85ecc311a21c9c

SO_ZO_E06cL__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: e62e4fc604b40589a1fb1615f96ea16e1d38981f53efaa905147134281cbfb3d

SO_ZO_E06cL__deterministic__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: 3b82935387bf36964e8b641d18b3acc03efe8cb04af9ab1ad54b2c5b85fdc924

SO_ZO_E06cL__deterministic__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 1ca3b819c4a540efeb55df39458dc0b7d1af02bf24f7f93f4578d26bbd3ea913

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 8a02f06c64b6955c12c0ed1c24c4310841da3c65c46574b2e3330b41092c0a94

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 1c163815a3606320ba2975c04f550e45ba5564c47dc7807d2ad91b27a4f63bf4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/5; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/6; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/7; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 5595ae958132d137164fe0cd5dbaddaa271f923224a5dc609ae105638d0c4211

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 1dd46d48764c2d73959f8c32106103806948bd818de147f71a186fe69f0356e9

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 1c163815a3606320ba2975c04f550e45ba5564c47dc7807d2ad91b27a4f63bf4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/4; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/5; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/6; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/7; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 6595d5185c49cb433b51ad35784a2e0b1568f6262c57ccaa8943598849ab97c0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 770ed6278f18bbe6ed3d68c3bd1d758aeeab6e82a571a87ad8bc34bc0961a03c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 1c163815a3606320ba2975c04f550e45ba5564c47dc7807d2ad91b27a4f63bf4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/4; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/5; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/6; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/7; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 17bda35342cb4ec62b598f61baae03ca9e75c52625b72b95969167cf743ec255

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 069a1c02fde261f6bc9882d66c3a20d44c6bb72312e90144febb6c3e634b0bf6

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 1c163815a3606320ba2975c04f550e45ba5564c47dc7807d2ad91b27a4f63bf4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/0; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/1; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/2; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/4; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/5; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/6; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/7; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: ac42228087c861bf7b8a9ed6f028f9874a3c97d9a009b65404d66c5adc2e75f0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 13e96797fad7158a4ac28671aaf3b2f7d0da737f74557f5771d9ad198fdd2801

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 1c163815a3606320ba2975c04f550e45ba5564c47dc7807d2ad91b27a4f63bf4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/0; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/1; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/2; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/4; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/5; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/6; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/7; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: edf74a5372a7b6da3c1c6aad7a9fe617f6f7179312b96693eaccf00fd68a91ac

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 75d7e32ce5a7729ca1ed5c8f61320e908ae91f86332ebb9407e1a4f17cca1945

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 7ac9866301b2a5a6fa31e55e6c6015a53bfd139945ab925b04cf770d47a023b4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/5; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: ebfd5b79d4099b8c4413bee3322daf4934ccbeca3157fd2ea0e4a6398f5e9333

Complete any desired broader literature search beyond the terminal exact-ID query; this is a supported local update, not exhaustive coverage.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: 03659c238b3ac9d2908bd625e2b2e010fd63483b412bd9c211a0cfd656e2119a

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 7ac9866301b2a5a6fa31e55e6c6015a53bfd139945ab925b04cf770d47a023b4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/5; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 07bfc0847ea79a80fde426bbc94add0d321d556062cb0a9466e288b23d485b74

Assess 2610.00345v1 Appendix K.4 constant-distortion certificates and further image-radius refinements in other geometry/accuracy regions.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 1b5b7e4dfc0cb3c8cc300ef484c4a61b7368807118901144ab84b17f12cf81cc

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 7ac9866301b2a5a6fa31e55e6c6015a53bfd139945ab925b04cf770d47a023b4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/5; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 92f73a35e5110867713a07f6115ace06d941b0b1b53c920762bb335bccc2c73c

Assemble low-dimensional positive-cost branches and the unassessed complement. The affine pair establishes only nontriviality below the matching-body threshold.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: d86c8611b153e4ee64064f39b751832daa892c54de592221c20e9e780fd04341

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 7ac9866301b2a5a6fa31e55e6c6015a53bfd139945ab925b04cf770d47a023b4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/5; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: e36473a72f7e5a47aa561c467755b5a12e6b74ea5aada1753ab74f45e577da83

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: cea5e89e9c80db181f33dfd893f68205bb696429eab4016255f6d4fd8852750f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs/0; canonical SHA-256: d1f58b650ca50fca6d3871c771d913e028c65460d4886722572076b5350e7634

SO_ZO_E06cL__deterministic__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: 206654a4e3e7eb59e0a47f85d69c7b21465de5ccc61082110216839cef5ffc48

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/1; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: d41735e638c9de1fe43fcad7600c2a277f6e3a71428b42f4a9c4fe04652e0aaa

possible-projection-455ddb5d1dae

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: b5873d05c45132dd91af49da8f0c6cd49f6ccfc2e14e888a394e734f8097ffc8

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E06cL__deterministic__b3 to SO_ZO_E06cL__deterministic__c1, SO_ZO_E06cL__deterministic__c2; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/obligations/12; canonical SHA-256: f136d13747854ba3e6d576e26341bbdcf93f65ec7fee494c792ac6750d157ee1

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs; canonical SHA-256: cea5e89e9c80db181f33dfd893f68205bb696429eab4016255f6d4fd8852750f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs/0; canonical SHA-256: d1f58b650ca50fca6d3871c771d913e028c65460d4886722572076b5350e7634

SO_ZO_E06cL__deterministic__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids; canonical SHA-256: 206654a4e3e7eb59e0a47f85d69c7b21465de5ccc61082110216839cef5ffc48

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/1; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/id; canonical SHA-256: c1190c998c57c9c3af21b675846c348e2a77873c4893b05d7c760c796c7a422b

possible-projection-455ddb5d1dae-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/lead; canonical SHA-256: b5873d05c45132dd91af49da8f0c6cd49f6ccfc2e14e888a394e734f8097ffc8

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E06cL__deterministic__b3 to SO_ZO_E06cL__deterministic__c1, SO_ZO_E06cL__deterministic__c2; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 6e0670178e7fd2bc65bfdfbae5d1fd8e042bf1a4e17d0fc603025110751471d8

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: d84419e2c49b554448ee9a1f2df3cdbaeaa46b29f6e3bdca005f96d33a20b57c

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 4b81cab280b1e31c2ea7afa9a416577b7c9c22795698d5d642e0394c36a90edd

/quantities/2

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 8ac3b850aefa1115a150e653472c5f992cf22de042ffec1212c0c25096dc1d16

For each registered deterministic/randomized g1 q1 quantity: d∈N, d≥1; known compact centrally symmetric convex B with nonempty interior; known nonempty compact convex K; L>0, ε>0; globally convex L-Lipschitz objectives on R^d; unrestricted exact scalar queries, output in K, and the registered fixed-path budget. Geometry varies jointly and its dependence remains explicit. Native p,q,R are conditional ball coordinates. The historical R metadata about a global minimizer cannot override the fixed constrained contract; the new endpoint uses derived ρ. Deterministic q2 remains separate and untransferred. Write Z for K=c_K+ρB, ρ≥0, ε≥Lρ within this domain.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: a6af48a092bc0ea9e1d1a2ca1e8a9a80c14982ada4e5098d2d4e60ff7eeb2be5

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 87d22f5899dba09d228f9a2ee4c52c4620fde18e6da59a7030fca371918f56a5

SO_ZO_E06cL_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 14c926c9d28b13570cc6649c35a25bcca11749a5e701b7107d22f70c3db13c49

SO_ZO_E06cL_p_4729bcfd1c

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 984ad179be4dd155621ff8b9f27d12e918e3e4681c1c37d59b82622207ad9b0e

SO_ZO_E06cL_p_73a0c205b0

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: d57e31d119d7067bc51944d2672f31f9f59b887f71088772300cf27efdbe3528

SO_ZO_E06cL_p_daa4cf7d79

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 4e935b9b80575efb7da0fd7e2bc527fe87ceb76bcabc0fc12d806e654d6ed8a1

SO_ZO_E06cL_p_5c322c6737

#### Native item 6

Native pointer: /joint_analysis/target/joint_variables/5; canonical SHA-256: 3e8a6aa7f2792d7437470daff2dad637353c60e95f4b4b9ab8a99630041006b0

SO_ZO_E06cL_p_5530ee35cd

#### Native item 7

Native pointer: /joint_analysis/target/joint_variables/6; canonical SHA-256: 1a7c8e01a0c47200e802891f35b6ac47cb3e6089dfab6a77d8a93232ded5c055

SO_ZO_E06cL_p_16b7e5563d

#### Native item 8

Native pointer: /joint_analysis/target/joint_variables/7; canonical SHA-256: a873f1739d43a0722fb91b46c8e56859fa58fcc063e0cd719a75ccbe5d7c34a9

SO_ZO_E06cL_p_15881069d1

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 345d036fe524b63fd42eed4459ad68204ad1803866440459d00d4907f0506e49

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: b19e86d22aadd8d449bf802dc411ee67f7758c0bfa8ad27a9a17e203ee45a6bc

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: c9d11b84453f62d8fdb37e7174f0a30adb32e8aa64733504864d027ca24e6005

On matching bodies K=c_K+ρB, ρ≥0 is the unique homothety scale derived from B,K; c_K is the known symmetry center, or the sole point when ρ=0. For ρ>0, g(u)=f(c_K+ρu)/(Lρ) is 1-Lipschitz, so ε/(Lρ) is dimensionless accuracy. No global-minimizer promise is used.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: dfb6a76147c56882a49e51a5aa535d081adb406ed4faf0ff7e7b8bedfd58d4b0

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 14c926c9d28b13570cc6649c35a25bcca11749a5e701b7107d22f70c3db13c49

SO_ZO_E06cL_p_4729bcfd1c

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 984ad179be4dd155621ff8b9f27d12e918e3e4681c1c37d59b82622207ad9b0e

SO_ZO_E06cL_p_73a0c205b0

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 5d499343e09566f397417cb372cc43b2de03f43a5be8446a059f17f6e681818b

ρ

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1; canonical SHA-256: efbb2e34ffb833da2e2d148e038443f627dd8426273f75c744219f1cc8668d49

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/1/expression; canonical SHA-256: d3096427570ff87542cab18e02c769a8c39ed6bec95fc1910e7097b4ca682c69

Retain native A_B=LR/ε only on the existing matching ellipsoidal regime, where R is its stated body radius. Rescaling f(c+Ru)/(LR) justifies this coordinate; it is not defined for arbitrary K.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs; canonical SHA-256: 87622ffd1b7c57e4dca2ff1998a750f15784269323bfd117275e43e274326062

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/0; canonical SHA-256: d57e31d119d7067bc51944d2672f31f9f59b887f71088772300cf27efdbe3528

SO_ZO_E06cL_p_daa4cf7d79

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/1; canonical SHA-256: a873f1739d43a0722fb91b46c8e56859fa58fcc063e0cd719a75ccbe5d7c34a9

SO_ZO_E06cL_p_15881069d1

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/2; canonical SHA-256: 4e935b9b80575efb7da0fd7e2bc527fe87ceb76bcabc0fc12d806e654d6ed8a1

SO_ZO_E06cL_p_5c322c6737

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/1/symbol; canonical SHA-256: ee342de3ddaa6ddbf5e1a9daac41fa2b4b30d17a9c965e236c324ff9f956e0af

A_B

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: a6af48a092bc0ea9e1d1a2ca1e8a9a80c14982ada4e5098d2d4e60ff7eeb2be5

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 87d22f5899dba09d228f9a2ee4c52c4620fde18e6da59a7030fca371918f56a5

SO_ZO_E06cL_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 14c926c9d28b13570cc6649c35a25bcca11749a5e701b7107d22f70c3db13c49

SO_ZO_E06cL_p_4729bcfd1c

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 984ad179be4dd155621ff8b9f27d12e918e3e4681c1c37d59b82622207ad9b0e

SO_ZO_E06cL_p_73a0c205b0

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: d57e31d119d7067bc51944d2672f31f9f59b887f71088772300cf27efdbe3528

SO_ZO_E06cL_p_daa4cf7d79

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 4e935b9b80575efb7da0fd7e2bc527fe87ceb76bcabc0fc12d806e654d6ed8a1

SO_ZO_E06cL_p_5c322c6737

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: 3e8a6aa7f2792d7437470daff2dad637353c60e95f4b4b9ab8a99630041006b0

SO_ZO_E06cL_p_5530ee35cd

#### Native item 7

Native pointer: /joint_analysis/target/uniform_in/6; canonical SHA-256: 1a7c8e01a0c47200e802891f35b6ac47cb3e6089dfab6a77d8a93232ded5c055

SO_ZO_E06cL_p_16b7e5563d

#### Native item 8

Native pointer: /joint_analysis/target/uniform_in/7; canonical SHA-256: a873f1739d43a0722fb91b46c8e56859fa58fcc063e0cd719a75ccbe5d7c34a9

SO_ZO_E06cL_p_15881069d1

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] Haihan Zhang, Chenheng Zhang, Zhiquan Qi and Zhouchen Lin. Near-Optimal Lower Bounds for Randomized Algorithms in Exact Value Zeroth-Order Convex Optimization. arXiv:2607.16558v2, 2026-07-30.

https://arxiv.org/html/2607.16558v2

[3] Arya Akhavan, Evgenii Chzhen, Massimiliano Pontil and Alexandre B. Tsybakov. A gradient estimator via L1-randomization for online zero-order optimization with two point feedback. NeurIPS 2022.

https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf

[4] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. JMLR 18(52):1--11, 2017.

https://jmlr.org/papers/volume18/16-632/16-632.pdf

[5] V. Yu. Protasov. Algorithms for approximate calculation of the minimum of a convex function from its values. Mathematical Notes 59(1):69--74, 1996.

https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper

[6] Gorbunov, Dvurechensky and Gasnikov. An Accelerated Method for Derivative-Free Smooth Stochastic Convex Optimization. SIAM Journal on Optimization 32(2):1210--1238, 2022.

https://arxiv.org/abs/1802.09022
