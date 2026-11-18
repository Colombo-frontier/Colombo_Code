# Smooth convex optimization in a general norm with a known localization body and exact values

**Setting ID.** `SO_ZO_E06cS`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Logarithmic gap

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Gradient lipschitz in declared norm; structure: No additional structure

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

$B\subset\mathbb{R}^d$ is a known compact, centrally symmetric convex body with nonempty interior. It induces the norm $\|x\|_B=\inf\{t>0:x\in tB\}$. The set $K\subset\mathbb{R}^d$ is known, nonempty, compact and convex.

$f:\mathbb{R}^d\to\mathbb{R}$ is globally convex and differentiable, with $\|\nabla f(x)-\nabla f(y)\|_{B,*}\le\beta\|x-y\|_B$ and $\operatorname{argmin}f\cap K\ne\varnothing$. The set $K$ localizes one global minimizer only.

Ball-geometry subregions are written as $K=B_p(0,R)$ and $B=B_q(0,1)$. The exponents $p$ and $q$ describe domain geometry and the regularity norm, respectively. General convex-body specifications do not require this ball parameterization.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

Projection and the stated proximal operations over known geometry are free.

The public inputs are $d$, $B$, $K$, $\beta$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

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

$B$: Unit ball of the known norm **Domain:** $B\subset\mathbb{R}^d$; compact, convex and centrally symmetric, with nonempty interior.

$\|x\|_B=\inf\{t>0:x\in tB\}$

$K$: Known feasible body or minimizer-localization body **Domain:** $K\subset\mathbb{R}^d$; nonempty, compact and convex.

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

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

$Q_B$: Smoothness accuracy ratio in the matching ellipsoidal subregime **Domain:** $Q_B>0$.

$Q_B=\beta R^2/\varepsilon$; used only in the subregime $K=c+RB$.

$c$: Small positive constant defining the accuracy window **Domain:** $c>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

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

$\|\cdot\|_{B,*},\|P\|_{B\to2}$: Dual norm and induced operator norm of a linear map **Domain:** $v\in\mathbb{R}^d,\ P:\mathbb{R}^d\to\mathbb{R}^m$.

$\|v\|_{B,*}=\sup_{x\in B}\langle v,x\rangle$, $\|P\|_{B\to2}=\sup_{x\in B}\|Px\|_2$

$c_K,c,z$: Known centers of the enclosing ball, affine ellipsoid and inscribed ball in the linear image **Domain:** $c_K,c\in\mathbb{R}^d,\ z\in\mathbb{R}^m$.

Used only in the corresponding geometric formula.

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

### R1 - Parameter regime E06cS.R1

**Region.** $B$ is an ellipsoid, $K=c+RB$, and $32\le Q_B\le d^2$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B2, B7

$$
\Omega(d\sqrt{Q_B})
$$

**Upper bound.** B3, B4, B8, B9

$$
O(d\sqrt{Q_B})
$$

**Gap or comparison.** $O(1)$

### R2 - Parameter regime E06cS.R2

**Region.** $B$ is an ellipsoid, $K=c+RB$, and $Q_B\ge32$ with $Q_B>d^2$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(d^2)
$$

**Upper bound.** B3, B4

$$
O(\min\{d\sqrt{Q_B},d^2\log(e+Q_B)\})
$$

**Gap or comparison.** $O(\min\{\sqrt{Q_B}/d,\log(e+Q_B)\})$

### R3 - Parameter regime E06cS.R2

**Region.** $B$ is an ellipsoid, $K=c+RB$, and $Q_B\ge32$ with $Q_B>d^2$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B7

$$
\Omega(d^2)
$$

**Upper bound.** B8, B9

$$
O(\min\{d\sqrt{Q_B},d^2\log(e+Q_B)\})
$$

**Gap or comparison.** $O(\min\{\sqrt{Q_B}/d,\log(e+Q_B)\})$

### R4 - Parameter regime E06cS.R3

**Region.** $B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le1/32$, with $\varepsilon=c\beta R^2/d$ and $d\ge8$.

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
O_c(d^{3/2}\log(ed))
$$

**Gap or comparison.** $O_c(\sqrt d\log(ed))$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Geometry-adapted finite-difference acceleration or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
U_S=O(1+\min\{d\sqrt{\beta\widehat{R}^2/\varepsilon},d^2\log(e+\beta\widehat{R}^2/\varepsilon)\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $a_B=\max_{\|u\|_2=1}\|u\|_B$ and $\widehat{R}=a_BR_2(K)$; R2(K) is a public Euclidean enclosing radius.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2 / N.4; pdf pages: 29; printed pages: 29

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2 / N.4

### B2 - Quadratic hard family under a norm-contracting linear image

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max_{1\le m\le d:\ 0<\varepsilon\le\beta r_m^2/32}\max\{5m/16,(m/4096)\min\{m,\sqrt{\beta r_m^2/\varepsilon}\}\}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Arbitrary randomized adaptive algorithms; take the maximum only over integers m satisfying the displayed accuracy window.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; pdf pages: 5; printed pages: 5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1

### B3 - Geometry-adapted finite-difference acceleration or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d\sqrt{Q_B})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $B\text{ is an ellipsoid},\ K=c+RB,\ Q_B=\beta R^2/\varepsilon\ge1$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: AppendixC.2; pdf pages: 29; printed pages: 29

### B4 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d^2\log(e+Q_B))
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $B\text{ is an ellipsoid},\ K=c+RB,\ Q_B\ge1$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: AppendixC.2; pdf pages: 29; printed pages: 29

### B5 - Geometry-adapted finite-difference acceleration or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
U_S=O(1+\min\{d\sqrt{\beta\widehat{R}^2/\varepsilon},d^2\log(e+\beta\widehat{R}^2/\varepsilon)\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $a_B=\max_{\|u\|_2=1}\|u\|_B$ and $\widehat{R}=a_BR_2(K)$; R2(K) is a public Euclidean enclosing radius.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2 / N.4; pdf pages: 29; printed pages: 29

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2 / N.4

### B6 - Geometry-adapted finite-difference acceleration or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
U_{S,\mathrm{rand}}=O(1+d\log(ed)\sqrt{\beta R^2/\varepsilon})
$$

**Sources.** [2](https://arxiv.org/abs/1802.09022) [1](https://arxiv.org/html/2610.00345v1) [5](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) [6](https://jmlr.org/papers/volume18/16-632/16-632.pdf)

**Conditions.** Here the specification is $B=B_1,K=B_1(R)$ and $d\ge8$; $\beta$ is the $\ell 1\to \ell \infty$ smoothness constant.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

**Source location.** [2](https://arxiv.org/abs/1802.09022) theorem: GDG22 Theorem 2.2 + D26 Lemma K.13 / N.4; pdf pages: 7

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: GDG22 Theorem 2.2 + D26 Lemma K.13 / N.4; pdf pages: 70; printed pages: 70

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: GDG22 Theorem 2.2 + D26 Lemma K.13 / N.4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: GDG22 Theorem 2.2 + D26 Lemma K.13 / N.4

### B7 - Quadratic hard family under a norm-contracting linear image

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max_{1\le m\le d:\ 0<\varepsilon\le\beta r_m^2/32}\max\{5m/16,(m/4096)\min\{m,\sqrt{\beta r_m^2/\varepsilon}\}\}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Arbitrary randomized adaptive algorithms; take the maximum only over integers m satisfying the displayed accuracy window.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; pdf pages: 5; printed pages: 5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1

### B8 - Geometry-adapted finite-difference acceleration or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d\sqrt{Q_B})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $B\text{ is an ellipsoid},\ K=c+RB,\ Q_B=\beta R^2/\varepsilon\ge1$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: AppendixC.2; pdf pages: 29; printed pages: 29

### B9 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d^2\log(e+Q_B))
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $B\text{ is an ellipsoid},\ K=c+RB,\ Q_B\ge1$

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: AppendixC.2; pdf pages: 29; printed pages: 29

## 5. Local arguments

### A1 - Norm conversion, penalized localization, and affine equivalence

**Scope.** Globally defined objectives, the declared regularity norm, a public feasible or localization body, and the stated free geometric operations.

Let $a_B=\max_{\|u\|_2=1}\|u\|_B$ and let $R_2(K)$ be a public Euclidean enclosing radius. Then $\beta_2=a_B^2\beta$, $L_2=a_BL$, and $D_2=a_BR_2(K)$ give the deterministic smooth envelope
$$O\!\left(1+\min\{d\sqrt{\beta D_2^2/\varepsilon},d^2\log(e+\beta D_2^2/\varepsilon)\}\right)$$
and Lipschitz localization $O(1+d^2\log(d+1)\log(e+LD_2/\varepsilon))$.

The norm inequality $\|v\|_B\le a_B\|v\|_2$ and its dual give the stated Euclidean smoothness and Lipschitz constants. Apply the exact-value Euclidean acceleration or smooth localization theorem with those constants and the public radius; each transformed value remains one scalar call. The global-minimizer promise is retained for the smooth localization argument.

For a Lipschitz objective minimized over a known convex set $K$, define $g(x)=f(x)+L_2\operatorname{dist}_2(x,K)$. This is convex and $2L_2$-Lipschitz, $\min g=\min_K f$ on a ball containing $K$, and $f(\Pi_Kx)\le g(x)$. One value of $g$ uses one value of $f$ plus public geometry. The Euclidean ball localization theorem therefore returns a legal point of $K$ after projection. This is a concrete transfer to a general body, not a presumed general-body localization theorem.

If $B=UB_2(1)$ and $K=c+RB$ for a public invertible matrix $U$, set $g(y)=f(c+Uy)$. Then $\|Uv\|_B=\|v\|_2$ and $\|U^\top w\|_2=\|w\|_{B,*}$. Thus both the Lipschitz and smoothness budgets are unchanged, the feasible or localization body becomes $B_2(R)$, and one value plus the inverse output map preserves the exact gap, budget, and guarantee. No condition-number factor appears. Deterministic acceleration/localization and randomized two-point methods keep their original algorithm permissions.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [3](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

### A2 - Randomized directional methods with explicit norm budgets

**Scope.** The direction distribution, prox norm, regularity norm, query domain, and randomness are distinct parts of the statement.

The applicable randomized upper bounds are
$$O(1+d\sqrt{\eta_{d,s}\beta_2\Theta_s/\varepsilon}),\quad O(1+d\eta_{d,s}\beta_2\Theta_s/\varepsilon),$$
$$O(1+L^2\Theta_s d^{1+2/\min(q,2)-2/s}/\varepsilon^2),\quad O(1+dv_H L_2^2\Theta_H/\varepsilon^2).$$

For the smooth directional methods take $d\ge8$, $1\le s\le2$, $s^*=s/(s-1)$, and $\eta_{d,s}=\min\{s^*-1,16\log d-8\}d^{2/s^*-1}$. Gorbunov, Dvurechensky, and Gasnikov's theorems apply to Euclidean smoothness $\beta_2$ and a prox divergence bounded by $\Theta_s$. Exact noiseless values use batch size one and two scalar values per direction; a finite positive difference scale can be chosen small enough for the fixed budget.

For the Lipschitz method of Akhavan et al., $q$ is the regularity norm and $s$ is the prox norm. Their theorem gives expected gap at most $11.9L\sqrt{\Theta_s d^{1+2/\min(q,2)-2/s}/T}$, with two values per round. Tightening the target by a factor three and applying Markov's inequality gives success probability $2/3$. A usable prox is
$$t_s=\max\{s,1+1/\log(ed)\},\quad a_{s,d}=\frac{d^{2(1/s-1/t_s)}}{t_s-1},\quad\omega_s(x)=a_{s,d}\|x\|_{t_s}^2/2.$$
It is 1-strongly convex in $\ell_s$ and on $B_p(R)$ has range at most $a_{s,d}R^2d^{2(1/t_s-1/p)_+}/2$. In particular, $q=2$, $s=p\le2$ gives the advertised $a_{p,d}d^{2/p^*}(LR/\varepsilon)^2$ term.

For Shamir's general-prox bound let $v_H=(\mathbb E\|U\|_{H,*}^4)^{1/2}$ for a uniform Euclidean sphere direction. Use ball convolution as the smoothed function, with sphere directions in its gradient estimator. The divergence identity belongs to the ball average; this formulation preserves convexity, Lipschitzness, the $O(hL_2)$ smoothing bias, and the source variance proof. All these witnesses are randomized, even when their value oracle is exact and deterministic.

For $B=K=B_1(R)$, Euclidean conversion gives $\beta_2=d\beta$, while the $\ell_1$ prox and directional factor contribute $\Theta_1=O(R^2\log(ed))$ and $\eta_{d,1}=O(\log(ed)/d)$. Substitution yields $O(1+d\log(ed)\sqrt{\beta R^2/\varepsilon})$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [2](https://arxiv.org/abs/1802.09022) [5](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) [6](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [1](https://arxiv.org/html/2610.00345v1)

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] Gorbunov, Dvurechensky and Gasnikov. An Accelerated Method for Derivative-Free Smooth Stochastic Convex Optimization. SIAM Journal on Optimization 32(2):1210--1238, 2022.

https://arxiv.org/abs/1802.09022

[3] Haihan Zhang, Chenheng Zhang, Zhiquan Qi and Zhouchen Lin. Near-Optimal Lower Bounds for Randomized Algorithms in Exact Value Zeroth-Order Convex Optimization. arXiv:2607.16558v2, 2026-07-30.

https://arxiv.org/html/2607.16558v2

[4] V. Yu. Protasov. Algorithms for approximate calculation of the minimum of a convex function from its values. Mathematical Notes 59(1):69--74, 1996.

https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper

[5] Arya Akhavan, Evgenii Chzhen, Massimiliano Pontil and Alexandre B. Tsybakov. A gradient estimator via L1-randomization for online zero-order optimization with two point feedback. NeurIPS 2022.

https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf

[6] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. JMLR 18(52):1--11, 2017.

https://jmlr.org/papers/volume18/16-632/16-632.pdf
